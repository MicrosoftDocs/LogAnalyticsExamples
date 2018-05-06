## Get the latest record per category
#### #arg_max
<!-- article_id: 2012‎2017‏‎03827037 -->

Get the latest AzureDiagnostics' record in each unique category

```OQL
AzureDiagnostics
| where TimeGenerated > ago(1d) 
| summarize arg_max(TimeGenerated, *) by Category
```