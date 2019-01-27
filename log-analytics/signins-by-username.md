# Signins by username
#### #signinlogs #username

Return signin activity by username from the Azure SigninLogs table/log.

```OQL
SigninLogs
| where TimeGenerated  >= ago(256d)
| where UserPrincipalName == "" // provide userprincipal name
| extend dtUTC = format_datetime(TimeGenerated,'yyyy-MM-dd hh:mm')
| extend dtAU = format_datetime(TimeGenerated +10h,'yyyy-MM-dd hh:mm')
| extend City = parse_json(LocationDetails).city
| project TimeGenerated , dtUTC , dtAU , UserPrincipalName , Type, Status, IPAddress  , Location , City , ResultType , ResultDescription, ClientAppUsed , DeviceDetail , AppDisplayName   
| sort by TimeGenerated desc
```