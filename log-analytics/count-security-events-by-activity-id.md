## Count security events by activity ID
#### #project #parse #count
<!-- article_id: 3107‎2017‏‎03827017 -->

This example relies on the fixed structure of the Activity column: <ID>-<Name>.
It parses the Activity value into 2 new columns, and counts the occurrence of each activity ID
```OQL
SecurityEvent
| where TimeGenerated > ago(30m) 
| project Activity 
| parse Activity with activityID " - " activityDesc
| summarize count() by activityID
```