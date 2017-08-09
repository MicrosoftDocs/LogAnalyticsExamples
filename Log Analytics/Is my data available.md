## Is my data available
#### #count

Starting data exploration often starts with data availability check.
This example shows the number of SecurityEvent records in the last 30 minutes:
```OQL
SecurityEvent 
| where TimeGenerated  > ago(30m) 
| count
```