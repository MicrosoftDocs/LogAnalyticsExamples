## Inner join: find exception related to failed requests
#### #join #project #bin #round
<!-- article_id: 3107‎2017‏‎03002 -->

This example finds which exceptions are related to failed requests in the past 24 hours.

```AIQL
requests 
 | where timestamp > ago(24h) and success=="False"
 | join kind=inner (exceptions 
	| where timestamp > ago(24h) ) on operation_Id 
 | project type, method, requestName = name, requestDuration = duration
```