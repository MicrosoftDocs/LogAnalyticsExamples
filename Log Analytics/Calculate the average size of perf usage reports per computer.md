## Calculate the average size of perf usage reports per computer
#### #avg #sort #barchart
<!-- article_id: 3107‎2017‏‎03827034 -->

This example calculates the average size of perf usage reports per computer, over the last 3 hours.
The results are shown in a bar chart.
```OQL
Usage 
| where TimeGenerated > ago(3h)
| where DataType == "Perf" 
| where QuantityUnit == "MBytes" 
| summarize avg(Quantity) by Computer
| sort by avg_Quantity desc nulls last
| render barchart
```