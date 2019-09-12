// Author: someone@somewhere.com
// Display name: What changes occurred last month?
// Description: Lists all update and patch requests from the last 30 days
// Category: Azure Resources, Audit
// Topic: General
// ResourceType: KeyVault	// may no be needed, support for smart saving, helps if saved in solutions folder
// Keywords:

```
// KeyVault diagnostic currently stores logs in AzureDiagnostics table which stores logs for multiple services. 
// Filter on ResourceProvider for logs specific to a service.
AzureDiagnostics
| where TimeGenerated > ago(30d) // Time range specified in the query. Overrides time picker in portal.
| where ResourceProvider =="MICROSOFT.KEYVAULT" 
| where OperationName == "VaultPut" or OperationName == "VaultPatch"
| sort by TimeGenerated desc.
```