## Computers with unhealthy latency
#### #distinct

The following example creates a list of distinct computers with unhealthy latency.
```OQL
NetworkMonitoring 
| where LatencyHealthState <> "Healthy" 
| where Computer != "" 
| distinct Computer
```