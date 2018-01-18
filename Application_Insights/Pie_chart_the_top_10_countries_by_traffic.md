## Top 10 countries by traffic
#### #count #render #piechart
<!-- article_id: 3107‎2017‏‎03827004 -->

The following example counts the number of requests received from each country (aka "traffic") in the past 24 hours. Traffic distribution from the top 10 countries is displays in a pie-chart.

```AIQL
requests 
 | where  timestamp > ago(24h) 
 | summarize count() by client_CountryOrRegion
 | top 10 by count_ 
 | render piechart
```

The output will look like this:
![top 10 countries by traffic](/images/top_10_countries_by_traffic.png)