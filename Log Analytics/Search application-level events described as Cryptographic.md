## Search application-level events described as "Cryptographic"
#### #search

Search the Events table for records in which EventLog is "Application", and RenderedDescription contains "cryptographic" (case-insensitive).
Reviews records from the last 5 hours.

```OQL
search in (Event) EventLog == "Application" and TimeGenerated > ago(5h) and RenderedDescription:"cryptographic"
```