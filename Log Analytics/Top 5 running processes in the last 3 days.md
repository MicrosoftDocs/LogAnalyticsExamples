## Top 5 running processes in the last 3 days
#### #let #count #render #timechart #in
<!-- article_id: 3107‎2017‏‎03827031 -->

The following example shows a time line of activity for the 5 most common processes, over the last 3 days.
```OQL
// Find all processes that started in the last 3 days. ID 4688: A new process has been created.
let RunProcesses = 
    SecurityEvent
    | where TimeGenerated > ago(3d)
    | where EventID == "4688";
// Find the 5 processes that were run the most
let Top5Processes =
RunProcesses
| summarize count() by Process
| top 5 by count_;
// Create a time chart of these 5 processes - hour by hour
RunProcesses 
| where Process in (Top5Processes) 
| summarize count() by bin (TimeGenerated, 1h), Process
| render timechart
```