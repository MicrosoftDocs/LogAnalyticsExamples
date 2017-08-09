# Identifying Data Patterns: Analyze Application Failures with <br/>
#*Autocluster* and *Diffpatterns*
#### (30 min to read)

<br/>
In this walkthrough we'll investigate a surge in application failures manifested as a spiky step jump in number of exceptions.

> [!Note]
> Before you start...<br/>
> If you haven't completed the [Joins - Cross Analysis](~/learn/tutorials/joins.md) tutorial yet, we recommend that you do so.

Let's begin by looking at our application's rate of exception over two weeks.
Run the following query:

```AIQL
exceptions
| where timestamp between (datetime(01-07-2017)..datetime(01-22-2017))
| where isempty(customDimensions["sourceapp"])
| summarize count() by bin (timestamp, 1h)
| render timechart
```

What do we see in the result?
There is a sharp spike at 2017-01-09T08:00:00Z. Click the highlighted marker to run diagnostics and isolate the root cause of a SQL exception.
Around 2017-01-11T15:00:00Z there's a step jump that seems to span until 2017-01-20T21:00:00Z.
Click one of the highlighted markers on the top spikes (2017-01-14T12:00:00Z and 2017-01-16T03:00:00Z).
This action points us to the same segment of OutOfMemory exceptions thrown from some lambda function.
That explains the spikes yet not explaining the massive step jump.

To further understand the step jump, let's see if it's load related.
The following query nicely correlates the jump in number of exceptions to a jump in volume of application requests.

```AIQL
requests
| where timestamp between (datetime(01-07-2017)..datetime(01-22-2017))
| where isempty(customDimensions["sourceapp"])
| summarize count() by bin (timestamp, 1h)
| render timechart
```
Click the highlighted marker (2017-01-11T14:00:00Z) to run diagnostics, which associates the jump in requests with a single client running from Saint Petersburg in Russia! 

Based on the previous step, we know that the following query charts the requests coming from the suspected client.
```AIQL
requests
| where timestamp between (datetime(2017-01-11T14:00:00Z)..datetime(01-22-2017))
| where isempty(customDimensions["sourceapp"])
| where client_City == "Saint Petersburg" and client_CountryOrRegion == "Russia" 
| where client_IP == "188.143.232.0" and isempty(user_Id) and isempty(session_Id) and isempty(operation_SyntheticSource)
| summarize count() by bin (timestamp, 1h)
| render timechart
```

## autocluster
*"autocluster"* find the commonalities between two sets of data.
In order to find the exceptions that are uniquely correlated with the suspicious client identified earlier, we can now scope our time range and use autocluster to find the commonalities between those exceptions:
```AIQL
exceptions
| where timestamp between (datetime(2017-01-11T16:00:00Z)..datetime(2017-01-19T20:00:00Z))
| where isempty(customDimensions["sourceapp"])
| where client_City == "Saint Petersburg" and client_CountryOrRegion == "Russia" 
| where client_IP == "188.143.232.0" and isempty(user_Id) and isempty(session_Id) and isempty(operation_SyntheticSource)
| project-away client_City , client_CountryOrRegion , client_IP , client_StateOrProvince , user_Id , session_Id 
| evaluate autocluster()
```

The results of *"autocluster()"* tell us that an accumulated ~50% of the exceptions are related to attempts of the specific client to create service tickets in the applications, all of which end
with either an OutOfMemoryException in a lambda method or a Win32Exception directly from the MVC ServiceTicketsController method.  

## diffpatterns
What more can we learn about the requests observed during the time of the step jump in addition to being associated with a suspicious client?
By running diffpatterns() we seek differences between two sets of records. In this case we use the column isDuringIncident to split between the two sets.
Run the following query:
```AIQL
requests
| where timestamp between (datetime(01-07-2017)..datetime(01-22-2017))
| where isempty(customDimensions["sourceapp"])
| extend isDuringIncident = iff(timestamp between (datetime("2017-01-11T08:00") .. datetime("2017-01-19T20:00")), "isIncident","isNotIncident")
| evaluate diffpatterns("split=isDuringIncident","target=isIncident")
```

The output shows 2 clear sets:
<p><img src="~/learn/tutorials/smart_analytics/images/diffpatterns.png" alt="Log Analytics diffpatterns"></p>

Scrolling the result table all the way to the right strenghens our hypothesis about the suspicious client but also reveals another interesting fact. 
Over 85% all the requests associated with the suspicious client were hitting application server with a unique version AutoGen_98407902-8f2c-4e10-96f9-95a14d58a283 which could be less robust.
So now we know in which specific version of our code we should be looking for instability and exactly in which methods.


## Next steps
Continue with our advanced tutorials:
* [Time series analysis](~/learn/tutorials/smart_analytics/make_series.md)
* [Profile application flow performance](~/examples/new/app_flow_performance.md)
* [Analyze usage metrics - sliding window calculations](~/examples/new/sliding_window_calculations.md)