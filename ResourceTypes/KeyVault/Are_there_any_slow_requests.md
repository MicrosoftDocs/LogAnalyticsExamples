// Author: someone@somewhere.com
// Display name: Are there any slow requests?
// Description: List of KeyVault requests that took longer than 1sec.
// Category: Azure Resources
// Topic: General
// ResourceType: KeyVault	// may no be needed, support for smart saving, helps if saved in solutions folder
// Keywords:

```
let threshold=1000; // let operator defines a constant that can be further used in the query
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.KEYVAULT" 
| where DurationMs > threshold
| summarize count() by OperationName
```