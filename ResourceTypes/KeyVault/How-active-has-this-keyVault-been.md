// Author: someone@somewhere.com
// Display name: How active has this KeyVault been?
// Description: Line chart showing trend of KeyVault requests volume, per operation over time.
// Category: Azure Resources
// Topic: General
// ResourceType: KeyVault
// Keywords: #render

```
// KeyVault diagnostic currently stores logs in AzureDiagnostics table which stores logs for multiple services. 
// Filter on ResourceProvider for logs specific to a service.
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.KEYVAULT" 
| summarize count() by bin(TimeGenerated, 1h), OperationName // Aggregate by hour
| render timechart
```
