## Find user accounts that failed to login over 5 times in 1 day
#### #let #join #project-away
<!-- article_id: 3108‎2017‏‎03827034 -->

The following example identifies user accounts that failed to login more than 5 times in the last day, and when they last attempted it.


```OQL
let timeframe = 1d;
SecurityEvent
| where TimeGenerated > ago(1d)
| where AccountType == 'User' and EventID == 4625 // 4625 - failed login
| summarize failed_login_attempts=count(), latest_failed_login=arg_max(TimeGenerated, Account) by Account 
| where failed_login_attempts > 5
| project-away Account1
```

Using *join*, and *let* statements we can check if the same suspicious accounts were later able to login successfully
```OQL
let timeframe = 1d;
let suspicious_users = 
	SecurityEvent
	| where TimeGenerated > ago(timeframe)
	| where AccountType == 'User' and EventID == 4625 // 4625 - failed login
	| summarize failed_login_attempts=count(), latest_failed_login=arg_max(TimeGenerated, Account) by Account 
	| where failed_login_attempts > 5
	| project-away Account1;
let suspicious_users_that_later_logged_in = 
    suspicious_users 
    | join kind=innerunique (
        SecurityEvent
        | where TimeGenerated > ago(timeframe)
        | where AccountType == 'User' and EventID == 4624 // 4624 - successful login,
        | summarize latest_successful_login=arg_max(TimeGenerated, Account) by Account
    ) on Account
    | extend was_login_after_failures = iif(latest_successful_login>latest_failed_login, 1, 0)
    | where was_login_after_failures == 1
;
suspicious_users_that_later_logged_in
```