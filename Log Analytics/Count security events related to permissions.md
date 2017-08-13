## Count security events related to permissions
#### #countif #has
<!-- article_id: 3107‎2017‏‎03827018 -->

This example show the number of securityEvent records, in which the Activity column contains the whole term "Permissions".
The query applies to records created over the last 30m.
```OQL
SecurityEvent
| where TimeGenerated > ago(30m)
| summarize EventCount = countif(Activity has "Permissions")
```