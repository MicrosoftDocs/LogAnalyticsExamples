## Count Azure diagnostics records per category
#### #count
<!-- article_id: 2012‎2017‏‎03827035 -->

Count Azure diagnostics records for each unique category.

```OQL
AzureDiagnostics 
| where TimeGenerated > ago(1d)
| summarize count() by Category
```