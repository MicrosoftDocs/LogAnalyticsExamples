## Server availability rate
#### #let #bin_at #countif #round
<!-- article_id: 2502‎2018‏‎03827037 -->

Calculate server availability rate based on heartbeat records. Availability is defined as "at least 1 heartbeat per hour".
So, if a server was available 98 of 100 hours, the availability rate is 98%.

```OQL
let start_time=startofday(datetime("2018-03-01"));
let end_time=now();
Heartbeat
| where TimeGenerated > start_time and TimeGenerated < end_time
| summarize heartbeat_per_hour=count() by bin_at(TimeGenerated, 1h, start_time), Computer
| extend available_per_hour=iff(heartbeat_per_hour>0, true, false)
| summarize total_available_hours=countif(available_per_hour==true) by Computer 
| extend total_number_of_buckets=round((end_time-start_time)/1h)+1
| extend availability_rate=total_available_hours*100/total_number_of_buckets
```


Let's review each part in this example:
The first 2 lines define variables, set to the desired start and end times.
We then use these variables to limit the query to that time range:
```
... | where TimeGenerated > start_time and TimeGenerated < end_time
```

Then we count the heartbeats reported by each computer, in buckets (bins) of 1 hour, starting at the start time: 
```
... | summarize heartbeat_per_hour=count() by bin_at(TimeGenerated, 1h, start_time), Computer
```

Now we can see how many heartbeats were reported by each computer each hour. If the number is  0 we understand the computer was probably offline at that time.
We use a new column to mark if a computer was available or not each hour:
```
... | extend available_per_hour=iff(heartbeat_per_hour>0, true, false)
```
and then count the number of hours each computer was indeed "alive": 
```
... | summarize total_available_hours=countif(available_per_hour==true) by Computer
```

Note that this way we give a little leeway for missing heartbeat reports each hour.
Instead of expecting a report every 5 or 10 minutes, we only mark a computer as "unavailable" if we didn't get any report from it during a full hour.

At this point we get a number for each computer, something like this:
<p><img src="~/examples/images/availability-hours.png" alt="server availability hours"></p>

So we know the number of hours each computer was available during the set time range. But what does it mean? how many hours were there altogether?

Here's how we can calculate the total number of hours in the selected time range:
```
... | extend total_number_of_buckets=round((end_time-start_time)/1h)+1
```

(There could be a better way to calculate the number of buckets, but this will do for the sake of the example)

Finally we calculate the ratio between available hours and total hours:
```
... | extend availability_rate=total_available_hours*100/total_number_of_buckets
```
and get this:

<p><img src="~/examples/images/availability-rate.png" alt="server availability rate"></p>

