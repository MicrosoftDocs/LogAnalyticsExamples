## Usage of specific computers today
#### #contains #sort
<!-- article_id: 3107‎2017‏‎03827032 -->

This example retrieves Usage data from the last day for computer names that contains the string "ContosoFile".
The results are sorted by "TimeGenerated".

```OQL
Usage
| where TimeGenerated > ago(1d)
| where  Computer contains "ContosoFile" 
| sort by TimeGenerated desc nulls last
```