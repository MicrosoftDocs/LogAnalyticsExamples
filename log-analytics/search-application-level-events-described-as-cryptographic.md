## Search application-level events described as "Cryptographic"
#### #search
<!-- article_id: 3107‎2017‏‎03827028 -->

Search the Events table for records in which EventLog is "Application", and RenderedDescription contains "cryptographic" (case-insensitive).
Reviews records from the last 24 hours.

```OQL
search in (Event) EventLog == "Application" and TimeGenerated > ago(24h) and RenderedDescription:"cryptographic"
```