## Bar chart unstacked
#### #count #render #barchart #unstacked
<!-- article_id: 3107‎2017‏‎03827008 -->

The following example count alerts severity, per day, and creates a bar chart 
```OQL
Alert 
| where TimeGenerated > ago(7d)
| summarize count() by AlertSeverity, bin(TimeGenerated, 1d)
| render barchart kind=unstacked
```