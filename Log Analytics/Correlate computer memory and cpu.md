## Join computer perf records to correlate memory and CPU
#### #let #datetime #project #join #inner #avg #max
<!-- article_id: 3107‎2017‏‎03827015 -->

This example correlates a given computer's perf records, and creates 2 time charts: the average CPU and maximum memory, in 30-minute bins.

```OQL
let StartTime = now()-5d;
let EndTime = now()-4d;
Perf
| where CounterName == "% Processor Time"  
| where TimeGenerated > StartTime and TimeGenerated < EndTime
and TimeGenerated < EndTime
| project TimeGenerated, Computer, cpu=CounterValue 
| join kind= inner (
   Perf
    | where CounterName == "% Used Memory"  
    | where TimeGenerated > StartTime and TimeGenerated < EndTime
    | project TimeGenerated , Computer, mem=CounterValue 
) on TimeGenerated, Computer
| summarize avgCpu=avg(cpu), maxMem=max(mem) by TimeGenerated bin=30m  
| render timechart
```