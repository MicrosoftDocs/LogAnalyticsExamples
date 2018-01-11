## Computers with non-reporting protection status duration
#### #count #min #max #join #extend
<!-- article_id: 3107‎2017‏‎03827013 -->

The following example lists computers that had a list one "Not Reporting" protection status.
It also measures the duration they were in this status (assuming it's a single event, not several "fragmentations" in reporting).
```OQL
ProtectionStatus
| where ProtectionStatus == "Not Reporting"
| summarize count(), startNotReporting = min(TimeGenerated), endNotReporting = max(TimeGenerated) by Computer, ProtectionStatusDetails
| join ProtectionStatus on Computer
| summarize lastReporting = max(TimeGenerated), startNotReporting = any(startNotReporting), endNotReporting = any(endNotReporting) by Computer
| extend durationNotReporting = endNotReporting - startNotReporting
```