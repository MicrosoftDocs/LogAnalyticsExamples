## Usage of specific computers today
#### #contains #sort
<!-- article_id: 3107‎2017‏‎03827032 -->

This example retrieves Usage data, if the computer name contains the string "ApplicationServer"
"TimeGenerated" is at most a day old, and sorted by "TimeGenerated"

```OQL
//
Usage
| where TimeGenerated > ago(1d)
| where  Computer contains "ApplicationServer" 
| sort by TimeGenerated desc nulls last
```