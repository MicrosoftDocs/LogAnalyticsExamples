# Analyze Usage Metrics with Sliding Window Calculations
#### (30 min to read)

<br/>
> [!Note]
> Before you start...<br/>
> If you haven't completed the [Profile Application Flow Performance](~/examples/new/app_flow_performance.md) tutorial yet, we recommend that you do so.

In this tutorial we review how to calculate standard usage metrics such as rolling MAU (Monthly Active Users), user stickiness reflected as MAU/DAU and basic cohort analysis.
To this end, we employ time-series analysis with the fir() function (Finite Impulse Response), which is the basic for sliding window computations.

For this walkthrough, let's assume our app is an online store that tracks users' activity through custom events. Specifically, we track two types of user activities: AddToCart and Checkout. 

## Rolling MAU (Monthly Active Users)
To calculate the rolling MAU (Monthly Active Users), we will define "active users" as only those who checked-out at least once in a given day.
The technique below allows you to set the criteria to the desired level of engagement using the "min_activity" value.

```AIQL
let endtime = endofday(datetime(2017-03-01T00:00:00Z));
let window = 60d;
let starttime = endtime-window;
let interval = 1d;
let user_bins_to_analyze = 28;
// Create an array of filters coefficients for fir(). A list of '1' in our case will produce a simple sum.
let moving_sum_filter = toscalar(range x from 1 to user_bins_to_analyze step 1 | extend v=1 | summarize makelist(v)); 
// Level of engagement. Users will be counted as engaged if they performed at least the number of activities set in min_activity. 
let min_activity = 1;

customEvents
| where timestamp > starttime  
| where customDimensions["sourceapp"] == "ai-loganalyticsui-prod"
// We want to analyze users who actually checked-out in our web site
| where (name == "Checkout") and user_AuthenticatedId <> ""
// Create a series of activities per user
| make-series UserClicks=count() default=0 on timestamp in range(starttime, endtime-1s, interval) by user_AuthenticatedId
// Create a new column containing a sliding sum. Passing 'false' as the last parameter to fir() prevents normalization of the calculation by the size of the window.
// For each time bin in the RollingUserClicks column the value is the aggregation of the user activities in the 28 days that preceded the bin.
// For example, if a user was active once on 2016-12-31 and then inactive throughout January, then the value will be 1 between 2016-12-31 -> 2017-01-28 and then 0s. 
| extend RollingUserClicks=fir(UserClicks, moving_sum_filter, false)
// Using zip operator to pack the timestamp with the user activities per time bin
| project User_AuthenticatedId=user_AuthenticatedId , RollingUserClicksByDay=zip(timestamp, RollingUserClicks)
// Transpose the table and create a separate row for each combination of user and time bin (1 day)
| mvexpand RollingUserClicksByDay
| extend Timestamp=todatetime(RollingUserClicksByDay[0])
// Mark the users that qualify according to min_activity
| extend RollingActiveUsersByDay=iff(toint(RollingUserClicksByDay[1]) >= min_activity, 1, 0)
// And finally, count the number of users per time bin.
| summarize sum(RollingActiveUsersByDay) by Timestamp
// First 28 days contain partial data, so we filter them out.
| where Timestamp > starttime + 28d
| render timechart
```

## User stickiness (MAU/DAU)
Lets turn the query above into a reusable function, and use it to calculate rolling user stickiness, defined as DAU/MAU. (Comments were dropped for brevity).

Parameters:
* sliding_window_size - number of days in the sliding window
* event_name - restrict to user activities by events with a specific name

```AIQL
let rollingDcount = (sliding_window_size: int, event_name:string)
{
    let endtime = endofday(datetime(2017-03-01T00:00:00Z));
    let window = 90d;
    let starttime = endtime-window;
    let interval = 1d;
    let moving_sum_filter = toscalar(range x from 1 to sliding_window_size step 1 | extend v=1| summarize makelist(v));    
    let min_activity = 1;
    customEvents
    | where timestamp > starttime
    | where customDimensions["sourceapp"]=="ai-loganalyticsui-prod"
    | where (name == event_name)
    | where user_AuthenticatedId <> ""
    | make-series UserClicks=count() default=0 on timestamp in range(starttime, endtime-1s, interval) by user_AuthenticatedId
    | extend RollingUserClicks=fir(UserClicks, moving_sum_filter, false)
    | project User_AuthenticatedId=user_AuthenticatedId , RollingUserClicksByDay=zip(timestamp, RollingUserClicks)
    | mvexpand RollingUserClicksByDay
    | extend Timestamp=todatetime(RollingUserClicksByDay[0])
    | extend RollingActiveUsersByDay=iff(toint(RollingUserClicksByDay[1]) >= min_activity, 1, 0)
    | summarize sum(RollingActiveUsersByDay) by Timestamp
    | where Timestamp > starttime + 28d
};
// Use the moving_sum_filter with bin size of 28 to count MAU.
rollingDcount(28, "Checkout")
| join
(
    // Use the moving_sum_filter with bin size of 1 to count DAU.
    rollingDcount(1, "Checkout")
)
on Timestamp
| project sum_RollingActiveUsersByDay1 *1.0 / sum_RollingActiveUsersByDay, Timestamp
| render timechart
```

## Cohorts analysis

### What is "cohorts analysis"?
Cohort analysis tracks the activity of specific groups of users (AKA "Cohorts"). The users are grouped by the time they first used the service, e.g. "October 2017".
Cohorts analysis attempts to measure how appealing the application or service is for returning users.
In the following example we analyze the number of users' activities over the course of 5 weeks, after we they used the service for the first time. 
When analyzing cohorts, it is expected to find a decreese in activity over the first tracked periods.
A cohort is titled by the week in which its members were observed for the first time.

### Cohort analysis example - 5 weeks
Labels:
* r0 - the distinct count of members of the cohort in the first week when they were observed
* r1 - the distinct count of members of the cohort that were active also in the week after then were observed (or after)
* r2 - ... in the following week

```AIQL
let startDate = startofweek(bin(datetime(2017-01-20T00:00:00Z), 1d));
let week = range Cohort from startDate to datetime(2017-03-01T00:00:00Z) step 7d;
// For each user we find the first and last timestamp of activity
let FirstAndLastUserActivity = (end:datetime) 
{
    customEvents
    | where customDimensions["sourceapp"]=="ai-loganalyticsui-prod"
    // Check 30 days back to see first time activity
    | where timestamp > startDate - 30d
    | where timestamp < end      
    | summarize min=min(timestamp), max=max(timestamp) by user_AuthenticatedId
};
let DistinctUsers = (cohortPeriod:datetime, evaluatePeriod:datetime) {
    toscalar (
    FirstAndLastUserActivity(evaluatePeriod)
    // Find members of the cohort: only users that were observed in this period for the first time
    | where min >= cohortPeriod and min < cohortPeriod + 7d  
    // Pick only the members that were active during the evaluated period or after
    | where max > evaluatePeriod - 7d
    | summarize dcount(user_AuthenticatedId)) 
};
week 
| where Cohort == startDate 
// Finally, calculate the desired metric for each cohort. In this sample we calculate distinct users but you can change
// this to any other metric that would measure the engagement of the cohort members.
| extend 
    r0 = DistinctUsers (startDate, startDate+7d),
    r1 = DistinctUsers (startDate, startDate+14d),
    r2 = DistinctUsers (startDate, startDate+21d),
    r3 = DistinctUsers (startDate, startDate+28d),
    r4 = DistinctUsers (startDate, startDate+35d)
| union (week | where Cohort == startDate + 7d 
| extend 
    r0 = DistinctUsers (startDate+7d, startDate+14d),
    r1 = DistinctUsers (startDate+7d, startDate+21d),
    r2 = DistinctUsers (startDate+7d, startDate+28d),
    r3 = DistinctUsers (startDate+7d, startDate+35d) )
| union (week | where Cohort == startDate + 14d 
| extend 
    r0 = DistinctUsers (startDate+14d, startDate+21d),
    r1 = DistinctUsers(startDate+14d, startDate+28d),
    r2 = DistinctUsers (startDate+14d, startDate+35d) )
| union (week | where Cohort == startDate + 21d 
| extend 
    r0 = DistinctUsers (startDate+21d, startDate+28d),
    r1 = DistinctUsers (startDate+21d, startDate+35d) ) 
| union (week | where Cohort == startDate + 28d 
| extend 
    r0 = DistinctUsers (startDate+28d, startDate+35d) )
// Calculate the retention percentage for each cohort by weeks
| project Cohort, r0, r1, r2, r3, r4,
          p0 = r0/r0*100,
          p1 = todouble(r1)/todouble (r0)*100,
          p2 = todouble(r2)/todouble(r0)*100,
          p3 = todouble(r3)/todouble(r0)*100,
          p4 = todouble(r4)/todouble(r0)*100 
| sort by Cohort asc
```
