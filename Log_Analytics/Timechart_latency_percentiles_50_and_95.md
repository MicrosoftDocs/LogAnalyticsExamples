## Timechart latency percentiles 50 and 95
#### #percentiles #timechart
<!-- article_id: 3107‎2017‏‎03827030 -->

This example calculates and charts the 50th and 95th percentiles of reporteed avgLatency, hour by hour, during the last 24 hours.

```OQL
Usage
| where TimeGenerated > ago(24h)
| summarize percentiles(AvgLatencyInSeconds, 50, 95) by bin(TimeGenerated, 1h) 
| render timechart
```