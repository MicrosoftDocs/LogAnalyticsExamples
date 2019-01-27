# Office 365 activity by username
#### #office365 #unified-audit-log #audit

Return activity from the Office365 unified audit log by username.

```OQL
OfficeActivity
| where UserId == "" 
| where TimeGenerated >= ago(256d) 
| extend dtUTC = format_datetime(TimeGenerated,'yyyy-MM-dd HH:mm')
| extend dtAU = format_datetime(TimeGenerated +11h,'yyyy-MM-dd HH:mm')
| extend UserAgent = parse_json(ExtendedProperties)[0].Value
| extend Cip = strcat(ClientIP,Client_IPAddress)
| extend UAgent = strcat(UserAgent, ClientInfoString)
| extend CreateItemSubject = parse_json(Item).Subject
| extend CreateItemPath = parse_json(Item).ParentFolder.Path
| extend InternetMessageID = parse_json(Item).InternetMessageId 
| extend DeleteItemSubject = parse_json(AffectedItems)[0].Subject
| extend DeleteItemPath = parse_json(AffectedItems)[0].ParentFolder.Path
| extend DestinationFolderPath = parse_json(DestFolder).Path
| extend MTDMessageID = parse_json(AffectedItems)[0].InternetMessageId
| project TimeGenerated,dtUTC,dtAU,UserId,Operation,ResultStatus,Cip,UAgent,CreateItemSubject,CreateItemPath,InternetMessageID,DeleteItemSubject,DeleteItemPath,MTDMessageID,DestinationFolderPath,OfficeObjectId 
| sort by dtUTC desc 
```