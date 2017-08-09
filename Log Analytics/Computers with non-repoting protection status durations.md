## Computers with non-repoting protection status durations
#### #count #min #max #join #extend

The following example lists computers that had a list one "Not respoinding" protection status.
It also measures the duration they were in this status (assuming it's a single event, not several "fragmentations" in reporting).
```OQL
ProtectionStatus
| where ProtectionStatus == "Not Reporting"
| summarize count(), startNotReporting = min(TimeGenerated), endNotReporting = max(TimeGenerated) by Computer, ProtectionStatusDetails
| join ProtectionStatus on Computer
| summarize lastReporting = max(TimeGenerated), startNotReporting = any(startNotReporting), endNotReporting = any(endNotReporting) by Computer
| extend durationNotReporting = endNotReporting - startNotReporting
```