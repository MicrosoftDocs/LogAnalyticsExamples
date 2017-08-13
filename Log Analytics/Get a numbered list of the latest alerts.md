## Get a numbered list of the latest alerts
#### #let #top #serialize #extend #project
<!-- article_id: 3107‎2017‏‎03827021 -->

This example gets the 100 latest alerts, adds the row number column to each row, and projects 5 interesting fields
```OQL
let maxRows = 100;
Alert
| top maxRows by TimeGenerated
| serialize 
| extend Id = row_number()
| project Id, TimeGenerated , AlertName , AlertDescription , AlertSeverity
```