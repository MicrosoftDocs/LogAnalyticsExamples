## Top 10 custom events
#### #dcount #render #barchart
<!-- article_id: 3107‎2017‏‎03827001 -->

The following query retrieves all customEvents recorded in the past 24 hours, and calculates their total count by name, and the number of distinct users (also by name).
The 10 names with the highest count are selected, and their calculated values (count and distict users) are displayed in a barchart:

```AIQL
customEvents 
 | where timestamp >= ago(24h)
 | summarize dcount(user_Id), count() by name
 | top 10 by count_ 
 | render barchart
```

The output will look like this:
<p><img src="~/examples/images/top-10-custom-events.png" alt="top 10 custom events"></p>