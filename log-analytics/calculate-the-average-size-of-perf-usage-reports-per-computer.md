## Calculate the average data volume size of perf usage reports per computer
#### #avg #sort #barchart
<!-- article_id: 3107‎2017‏‎03827034 -->

This example calculates the average size of perf usage reports per computer, over the last 3 hours.
The results are shown in a bar chart.
```OQL
Perf
| where TimeGenerated > ago(3h)
| where _IsBillable == true
| summarize AvgBytes=avg(_BilledSize) by  Computer | sort by AvgBytes desc
```
