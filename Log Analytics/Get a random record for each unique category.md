## Get a random record for each unique category
#### #any
<!-- article_id: 2012‎2017‏‎03827036 -->

Get a single random AzureDiagnostics' record for each unique category

```OQL
AzureDiagnostics
| where TimeGenerated > ago(1d) 
| summarize any(*) by Category
```