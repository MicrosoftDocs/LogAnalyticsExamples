# Signins by ip
#### #signinlogs #ip

Return signin activity by one or more ip address from the Azure SigninLogs table/log.

```OQL
SigninLogs
| where TimeGenerated  >= ago(256d)
| where IPAddress in ('0.0.0.0','0.0.0.1')
| extend dtUTC = format_datetime(TimeGenerated,'yyyy-MM-dd hh:mm')
| extend dtAU = format_datetime(TimeGenerated +11h,'yyyy-MM-dd hh:mm')
| extend City = parse_json(LocationDetails).city
| project TimeGenerated , dtUTC , dtAU , UserPrincipalName , Type, Status, IPAddress  , Location , City , ResultType , ResultDescription, ClientAppUsed , DeviceDetail , AppDisplayName
| sort by TimeGenerated desc
//| summarize by IPAddress
```