## Chart a week-over-week view of the number of computers sending data
#### #startofweek #dcount #barchart
<!-- article_id: 3107‎2017‏‎03827010 -->

The following example charts the number of distinct computers that sent heartbeats, each week.

```OQL
Heartbeat
| where TimeGenerated >= startofweek(ago(21d))
| summarize dcount(Computer) by endofweek(TimeGenerated) | render barchart kind=default
```