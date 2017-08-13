## Chart the record-count per table in the last 5 hours
#### #union #withsource #count #timechart
<!-- article_id: 3107‎2017‏‎03827011 -->

The following example collects all records of all tables from the last 5 hours, and counts how many records were in each table, in each point in time.
The results are shown in a timechart.

```OQL
union withsource=sourceTable *
| where TimeGenerated > ago(5h) 
| summarize count() by bin(TimeGenerated,10m), sourceTable
| render timechart
```