# Recent security alerts
#### #security #alert $user #location

Return triggered security alerts in the last 24 hours.

```OQL
SecurityAlert
| extend dtUTC = format_datetime(TimeGenerated,'yyyy-MM-dd HH:mm')
| extend dtAU = format_datetime(TimeGenerated +11h,'yyyy-MM-dd HH:mm')
| extend IP = parse_json(ExtendedProperties)['Client IP Address']
| extend Username = parse_json(ExtendedProperties)['User Name']
| extend Location = parse_json(ExtendedProperties)['Client Location']
| project TimeGenerated, dtUTC, dtAU, AlertType, AlertName, AlertSeverity , Description , Username , IP , Location
```