## User stickiness (daily/monthly active users)
#### #make-series #fir #range #zip #mvexpand

This example uses time-series analysis with the fir() function (Finite Impulse Response), which is the basic for sliding window computations.

Let's assume our app is an online store that tracks users' activity through custom events. Specifically, We track two types of user activities: AddToCart and Checkout. 

Lets turn the query above into a reusable function, and use it to calculate rolling user stickiness, defined as DAU/MAU. (Comments were dropped for brevity).
We define "active users" as only those that performed check-out at least once in a given day.

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
    | make-series UserClicks=count() default=0 on timestamp 
		in range(starttime, endtime-1s, interval) by user_AuthenticatedId
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

The output will look like this:
<p><img src="~/examples/images/user-stickiness.png" alt="user stickiness"></p>