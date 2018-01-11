## Is my security data available
#### #count
<!-- article_id: 3107‎2017‏‎03827023 -->

Starting data exploration often starts with data availability check.
This example shows the number of SecurityEvent records in the last 30 minutes:
```OQL
SecurityEvent 
| where TimeGenerated  > ago(30m) 
| count
```