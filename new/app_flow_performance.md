# Profile Application Flow Performance
#### (25 min to read)

<br/>
> [!Note]
> Before you start...<br/>
> If you haven't completed the [Time Series Analysis](~/learn/tutorials/smart_analytics/make_series.md) tutorial yet, we recommend that you do so.

In this tutorial we review how Azure Log Analytics can help track the performance of code flows in an app using only plain debug logs. 
After completing this walkthrough, you will know how to:
* Turn textual logs into metrics
* Apply advanced time series analysis to determine if the data shows a seasonal pattern.

Let’s start by looking at a short snippet out of a simplified application debug log
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
traces
| where timestamp > startDate and timestamp < endDate
| where operation_Id == "QaXuZhd2b2c=" 
| project timestamp , operation_Id , message
```

The flow we'd like to time in this example is "anomaly detection".
In order to benchmark this flow, we identify the specifc log messages indicating its start and end time. 
so the following query keeps only records that mark the begining and end of this flow:
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
traces
| where timestamp > startDate and timestamp < endDate
| where (message startswith "Processing anomaly detection") or (message == "Done processing")
| project timestamp , operation_Id , message 
| order by operation_Id, timestamp asc
| take 10
```

The results show pairs of lines per operation - the first indicated the starting of the Processing anomaly detection flow, and the second indicated its completion.

The following query calculate the duration of the operation by subtracting the earlier timestamp from the later, per operation.
Once converted to long, a timestamp is the number of ticks. To convert to milliseconds, we divide it by 10,000:
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
traces
| where timestamp > startDate and timestamp < endDate
| where (message startswith "Processing anomaly detection") or (message == "Done processing")
| project timestamp , operation_Id , message 
|   summarize count(), durationInMS=tolong(max(timestamp)-min(timestamp))/10000 by operation_Id
 Filter out operations that do not have both a beginning and an end
|   where count_ == 2
| project-away count_
| take 10
```

To add the duration column back to the original table we use join and operation_Id as the correlator.
Use of materialize() optimizes the performance of the query when joining a set of records with itself.
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
let T = materialize(
traces
| where timestamp > startDate and timestamp < endDate
| where (message startswith "Processing anomaly detection") or (message == "Done processing")
| project timestamp , operation_Id , message );
T
| where message == "Done processing"
| join kind=inner (T  
|   summarize count(), durationInMS=tolong(max(timestamp)-min(timestamp))/10000 by operation_Id
|   where count_ == 2
|   project operation_Id , durationInMS ) on operation_Id
| project-away operation_Id1
| take 10
```

We can now draw a 6 days’ chart of the average durations in time bins of 5 minutes:
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
let T = materialize(
traces
| where timestamp > startDate and timestamp < endDate
| where (message startswith "Processing anomaly detection") or (message == "Done processing")
| project timestamp , operation_Id , message );
T
| where message == "Done processing"
| join kind=inner (T  
|   summarize count(), durationInMS=tolong(max(timestamp)-min(timestamp))/10000 by operation_Id
|   where count_ == 2
|   project operation_Id , durationInMS ) on operation_Id
| project-away operation_Id1
| summarize avg(durationInMS) by bin(timestamp, 5m)
| render timechart
```

Looking at the output chart from the previous query, it seems like there is some repeating pattern in the data which could be seasonal.
Let's use make-series and series-periods to assess whether there is indeed a seasonal pattern in the data.
```AIQL
let startDate = startofday(datetime("2017-02-01"));
let endDate = startofday(datetime("2017-02-07"));
let T = materialize(
traces
| where timestamp > startDate and timestamp < endDate
| where (message startswith "Processing anomaly detection") or (message == "Done processing")
| project timestamp , operation_Id , message );
T
| where message == "Done processing"
| join kind=inner (T  
|   summarize count(), durationInMS=tolong(max(timestamp)-min(timestamp))/10000 by operation_Id
|   where count_ == 2
|   project operation_Id , durationInMS ) on operation_Id
| project-away operation_Id1
```

Apply time series analysis to detect hidden seasonality in the result:
```AIQL
| make-series duration=avg(durationInMS) default=0 on timestamp in range(startDate, endDate, 5m) by "All"
| project periods = series_periods(duration, 4.0, 500.0, 2)
```

Indeed, two seasonal patterns were identified, a shorter one of 24h and a longer one of 12h (values are based on the 5 minutes interval we used).


## Next steps
Continue with our advanced tutorials:
* [Analyze usage metrics - sliding window calculations](~/examples/new/sliding_window_calculations.md)