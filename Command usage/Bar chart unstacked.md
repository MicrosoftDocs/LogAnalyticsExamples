## Bar chart unstacked
#### #count #render #barchart #unstacked

The following example count alerts severity, per day, and creates a bar chart 
```OQL
Alert 
| where TimeGenerated > ago(7d)
| summarize count() by AlertSeverity, bin(TimeGenerated, 1d)
| render barchart kind=unstacked
```