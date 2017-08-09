## Top 5 running processes in the last 3 days
#### #let #count #render #timechart #in

The following example shows a pie chart of processes that used explicit credenetials in the last week
```OQL
// Find all processes that started in the last 3 days. ID 4688: A new process has been created.
let RunProcesses = 
    SecurityEvent
    | where TimeGenerated > ago(3d)
    | where EventID == "4688";

// Find the 5 processes that were run the most time
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