## Count all logs collected over the last hour, per type
#### #search #count #barchart
<!-- article_id: 3107‎2017‏‎03827033 -->

The following example search everything reported in the last hour and counts the records of each table using the system column $table.
The results are displayed in a bar chart.

```OQL
search *
| where TimeGenerated > ago(1h) 
| summarize CountOfRecords = count() by $table
| render barchart
```