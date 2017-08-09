## Get a numbered list of the latest alerts
#### #let #top #serialize #extend #project

This example gets the 100 latest alerts, adds the row number column to each row, and projects 5 interesting fields
```OQL
let maxRows = 100;
Alert
| top maxRows by TimeGenerated
| serialize 
| extend Id = row_number()
| project Id, TimeGenerated , AlertName , AlertDescription , AlertSeverity
```