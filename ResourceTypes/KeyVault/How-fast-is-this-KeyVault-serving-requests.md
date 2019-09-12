// Author: someone@somewhere.com
// Display name: How fast is this KeyVault serving requests?
// Description: Line chart showing trend of request duration over time using different aggregations.
// Category: Azure Resources
// Topic: General
// ResourceType: KeyVault	// may no be needed, support for smart saving, helps if saved in solutions folder
// Keywords:

```
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.KEYVAULT" 
| where httpStatusCode_d >= 300 and not(OperationName == "Authentication" and httpStatusCode_d == 401)
| summarize count() by requestUri_s, ResultSignature
// ResultSignature contains HTTP status such as "OK" or "Forbidden".
// httpStatusCode_d contains HTTP status code returned by the request such as 200 or 401.
// requestUri_s contains the URI of the request.
```