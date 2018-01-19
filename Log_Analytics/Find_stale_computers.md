## Find stale computers
#### #max #isnotempty
<!-- article_id: 3107‎2017‏‎03827020 -->

The following example finds computers that were active in the last day but did not send heartbeats in the last hour.

```OQL
Heartbeat
| where TimeGenerated > ago(1d)
| summarize LastHeartbeat = max(TimeGenerated) by Computer
| where isnotempty(Computer)
| where LastHeartbeat < ago(1h)
```