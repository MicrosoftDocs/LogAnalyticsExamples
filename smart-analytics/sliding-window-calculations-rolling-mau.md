## Rolling MAU (Monthly Active Users)
#### #make-series #fir #zip #mvexpand

This example uses time-series analysis with the *fir* function (Finite Impulse Response), which is the basic for sliding window computations.

Let's assume our app is an online store that tracks users' activity through custom events. Specifically, We track two types of user activities: AddToCart and Checkout. 

We define "active users" as only those that performed check-out at least once in a given day.
The technique below allows you to set the criteria to the desired level of engagement using the "min_activity" value.

```AIQL
let endtime = endofday(datetime(2017-03-01T00:00:00Z));
let window = 60d;
let starttime = endtime-window;
let interval = 1d;
let user_bins_to_analyze = 28;

// Create an array of filters coefficients for fir(). A list of '1' in our case will produce a simple sum.
let moving_sum_filter = toscalar(range x from 1 to user_bins_to_analyze step 1 | extend v=1 | summarize makelist(v)); 

// Level of engagement. Users will be counted as engaged if they performed at least this number of activities.
let min_activity = 1;

customEvents
| where timestamp > starttime  
| where customDimensions["sourceapp"] == "ai-loganalyticsui-prod"

// We want to analyze users who actually checked-out in our web site
| where (name == "Checkout") and user_AuthenticatedId <> ""

// Create a series of activities per user
| make-series UserClicks=count() default=0 on timestamp 
	in range(starttime, endtime-1s, interval) by user_AuthenticatedId

// Create a new column containing a sliding sum. 
// Passing 'false' as the last parameter to fir() prevents normalization of the calculation by the size of the window.
// For each time bin in the *RollingUserClicks* column, the value is the aggregation of the user activities in the 
// 28 days that preceded the bin. For example, if a user was active once on 2016-12-31 and then inactive throughout 
// January, then the value will be 1 between 2016-12-31 -> 2017-01-28 and then 0s. 
| extend RollingUserClicks=fir(UserClicks, moving_sum_filter, false)

// Use the zip() operator to pack the timestamp with the user activities per time bin
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

// render as timechart
| render timechart
```

The output will look like this:
<p><img src="~/examples/images/rolling-mau.png" alt="rolling mau"></p>