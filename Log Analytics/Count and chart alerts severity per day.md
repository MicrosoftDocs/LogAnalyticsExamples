## Count and chart alerts severity, per day
#### #count #render #barchart #bin

The following example creates an unstacked bar chart of alert count by severity, per day:
```OQL
Alert 
| where TimeGenerated > ago(7d)
| summarize count() by AlertSeverity, bin(TimeGenerated, 1d)
| render barchart kind=unstacked
```