## server Availability rate
#### #any
<!-- article_id: 2502‎2018‏‎03827037 -->

Calculate server availability rate based on heartbeat records.
The availability rate is defined as the % of uptime of a given server during a certain period of time. So, if a server was up 98 of a total 100 hours, the availability rate for that period is 98%.

```OQL
let start_time=startofday(datetime("2017-01-01"));
let end_time=endofday(datetime("2017-01-31"));
Heartbeat
| where TimeGenerated > start_time and TimeGenerated < end_time
| summarize heartbeat_per_hour=count() by bin_at(TimeGenerated, 1h, start_time), Computer
| extend available_per_hour=iff(heartbeat_per_hour>0, true, false)
| summarize total_available_hours=countif(available_per_hour==true) by Computer 
| extend total_number_of_buckets=round((end_time-start_time)/1h)
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
<p><img src="~/examples/images/availability_hours.png" alt="server availability hours"></p>

So we know each computer was alive 11 hours in the select time range. But what does it mean? how many hours were there altogether? is this 11 out of 11 hours (100% availability) or out of 110 hours (only 10% availability)?

Here's how we can calculate the total number of hours in the selected time range:
```
... | extend total_number_of_buckets=round((end_time-start_time)/1h)+1
```

(There could be a better way to calculate the number of buckets, but this will do for the sake of the example)

Finally we calculate the ratio between available hours and total hours:
```
... | extend availability_rate=total_available_hours*100/total_number_of_buckets

and get this:
```
<p><img src="~/examples/images/availability_rate.png" alt="server availability rate"></p>

