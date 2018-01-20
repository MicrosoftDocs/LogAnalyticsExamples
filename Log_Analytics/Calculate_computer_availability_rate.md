## Calculate computer availability rate
#### #bin_at #countif #hourofday
<!-- article_id: 1601‎201803827040 -->

For each computer, calculate the availability rate calculated since midnight. Availability is defined as "at least 1 heartbeat per hour".

```OQL
let midnight=startofday(now());
Heartbeat
| where TimeGenerated>midnight
| summarize heartbeat_per_hour=count() by bin_at(TimeGenerated, 1h, midnight), Computer
| extend available_per_hour=iff(heartbeat_per_hour>0, true, false)
| summarize total_available_hours=countif(available_per_hour==true) by Computer 
| extend number_of_buckets=hourofday(now())+1
| extend availability_rate=total_available_hours*100/number_of_buckets
```
