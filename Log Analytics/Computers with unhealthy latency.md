## Computers with unhealthy latency
#### #distinct
<!-- article_id: 3107‎2017‏‎03827014 -->

The following example creates a list of distinct computers with unhealthy latency.
```OQL
NetworkMonitoring 
| where LatencyHealthState <> "Healthy" 
| where Computer != "" 
| distinct Computer
```