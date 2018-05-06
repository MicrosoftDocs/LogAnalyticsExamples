## Get the latest heartbeat record per computer IP
#### #arg_max
<!-- article_id: 3107‎2017‏‎03827022 -->

This example returns the last heartbeat record for each computer IP.
```OQL
Heartbeat
| summarize arg_max(TimeGenerated, *) by ComputerIP
```