## Get lateset heartbeat record per computer IP
#### #arg_max

This example returns the last heartbeat record for each computer IP.
```OQL
Heartbeat
| summarize arg_max(TimeGenerated, *) by ComputerIP
```