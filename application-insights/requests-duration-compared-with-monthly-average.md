## Daily request duration compared with monthly average
#### #count #make-series #timechart #summarize


The following query calculates and charts the current (last day) and monthly average request duration.

```
let response_last_month = toscalar(
    requests
    | where timestamp between(ago(7d) .. ago(1d))
    | summarize value=avg(duration) 
);
requests
| where timestamp >= ago(1d)
| make-series avg_duration = avg(duration) default=0 on timestamp in range(ago(1d), now(), 15m) 
| extend monthly_avg = repeat(response_last_month, array_length(avg_duration))
| render timechart
```

The output will look like this:
<p><img src="~/examples/images/current-duration-vs-monthly-average.png" alt="Request duration over the last day compared with the monthly average"></p>