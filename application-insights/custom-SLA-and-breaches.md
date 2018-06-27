## Defining a custom SLA, and adherence to it
#### #count #render #timechart #summarize
<!-- article_id: 3107‎2017‏‎03827004 -->

The following query defines a custom Service Level Agreement (SLA): a request is considered as meeting SLA if it completes in under 3 seconds. The query then adds a static SLA target of 99.9% of requests needing to meet the SLA. The two are plotted on a time chart. 

```AIQL
requests
| where timestamp > ago(7d)
| summarize slaMet = count(duration < 3000), slaBreached = count(duration >= 3000), totalCount = count() by bin(timestamp, 1h)
| extend SLAIndex = slaMet * 100.0 / totalCount 
| extend SLA = 99.9
| project SLAIndex, timestamp, SLA 
| render timechart 
```

The output will look like this:
<p><img src="~/examples/images/SLA.png" alt="a custom SLA metric definition and its trend over time compared to SLA target"></p>