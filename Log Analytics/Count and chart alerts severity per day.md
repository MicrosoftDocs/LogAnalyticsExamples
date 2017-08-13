## Count and chart alerts severity, per day
#### #count #render #barchart #bin
<!-- article_id: 3107‎2017‏‎03827016 -->

The following example creates an unstacked bar chart of alert count by severity, per day:
```OQL
Alert 
| where TimeGenerated > ago(7d)
| summarize count() by AlertSeverity, bin(TimeGenerated, 1d)
| render barchart kind=unstacked
```