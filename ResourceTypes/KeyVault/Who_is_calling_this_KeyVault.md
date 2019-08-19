// Author: someone@somewhere.com
// Display name: Who is calling this KeyVault?
// Description: List of callers identified by their IP address with their request count.
// Category: Azure Resources, Security
// Topic: General
// ResourceType: KeyVault	// may no be needed, support for smart saving, helps if saved in solutions folder

```
// KeyVault diagnostic currently stores logs in AzureDiagnostics table which stores logs for multiple services. 
// Filter on ResourceProvider for logs specific to a service.
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.KEYVAULT"
| summarize count() by CallerIPAddress
```
