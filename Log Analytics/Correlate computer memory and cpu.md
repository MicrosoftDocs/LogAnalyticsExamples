## Join computer perf records to corrolate memory and cpu
#### #let #datetime #project #join #inner #avg #max

This example correlates a given computer's perf records, and creates 2 time charts: the average CPU and maximum memory, in 30-minute bins.

```OQL
let StartTime = datetime(2016-07-01 19:30);
let EndTime = datetime(2017-07-02 00:30);
Perf
| where Computer == "ContosoAzLnx1" 
| where CounterName == "% Processor Time"  
| where TimeGenerated > StartTime and TimeGenerated < EndTime
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