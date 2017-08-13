## Calculate multiple percentiles timechart
#### #percentiles #render #timechart #bin
<!-- article_id: 3107‎2017‏‎03827007 -->

The following example calculates the 50th, 90th, and 95th percentiles of request duration, in the past 24 hours:

```AIQL
requests 
  | where timestamp > ago(24h) 
  | summarize percentiles(duration, 50, 90, 95) by bin(timestamp, 1h) 
  | render timechart
```

The output will look like this:
<p><img src="~/examples/images/percentiles.png" alt="percentiles"></p>