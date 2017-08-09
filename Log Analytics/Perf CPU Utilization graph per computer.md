## Perf CPU Utilization graph per computer
#### #startswith #avg #timechart

This example calculates and charts the CPU utilization of computers that start with "Store0".

```OQL
Perf
| where TimeGenerated > ago(4h)
| where Computer startswith "Store0" 
| where CounterName == @"% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 15m) 
| render timechart
```