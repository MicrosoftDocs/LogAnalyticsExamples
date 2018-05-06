## Pie chart explicit credentials processes
#### #count #render #piechart
<!-- article_id: 3107‎2017‏‎03827027 -->

The following example shows a pie chart of processes that used explicit credentials in the last week
```OQL
SecurityEvent
| where TimeGenerated > ago(7d)
// filter by id 4648 ("A logon was attempted using explicit credentials")
| where EventID == 4648
| summarize count() by Process
| render piechart 
```