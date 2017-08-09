## What are the data types I have
#### #search #count #barchart

The following example search everything reported in the last hour and counts the records of each table using the system column $table.
The results are displayed in a bar chart.

```OQL
search *
| where TimeGenerated > ago(1h) 
| summarize CountOfRecords = count() by $table
| render barchart
```