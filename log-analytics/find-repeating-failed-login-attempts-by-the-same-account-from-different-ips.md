## Find repeating failed login attempts by the same account from different IPs
#### #let #join #project-away
<!-- article_id: 3108‎2017‏‎03827035 -->

The following examples finds failed login attempts by the same account from more than 5 different IPs, in the last 6 hours, and the enumerates the IPs.

```OQL
SecurityEvent 
| where AccountType == "User" and EventID == 4625 and TimeGenerated > ago(6h) 
| summarize IPCount = dcount(IpAddress), makeset(IpAddress)  by Account
| where IPCount > 5
| sort by IPCount desc
```