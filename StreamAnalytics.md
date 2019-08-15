Formatted for dev
"### Input data Errors

#### Title
List all input data errors

#### Description
Shows all errors that occurred while processing the data from inputs.

#### Content
AzureDiagnostics 
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type == ""DataError"" 
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all input deserialization errors

#### Description
Shows errors caused due to malformed events that could not be deserialized by the job.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType in (""InputDeserializerError.InvalidData"", ""InputDeserializerError.TypeConversionError"", ""InputDeserializerError.MissingColumns"", ""InputDeserializerError.InvalidHeader"", ""InputDeserializerError.InvalidCompressionType"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all InvalidInputTimeStamp errors

#### Description
Shows errors caused due to events where value of the TIMESTAMP BY expression can't be converted to datetime

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""InvalidInputTimeStamp""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all InvalidInputTimeStampKey errors

#### Description
Shows errors caused due to events where value of the TIMESTAMP BY OVER timestampColumn is NULL

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""InvalidInputTimeStampKey""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Events that arrived late

#### Description
Shows errors due to events where difference between application time and arrival time is greater than the late arrival policy.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""LateInputEvent""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Events that arrived early

#### Description
Shows errors due to events where difference between Application time and Arrival time is greater than 5 minutes.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""EarlyInputEvent""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Events that arrived out of order

#### Description
Shows errors due to events that arrive out of order according to the out-of-order policy.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""OutOfOrderEvent""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"### Output data errors

#### Title
All output data errors

#### Description
Shows all errors that occurred while writing the results of the query to the outputs in your job.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType in (""OutputDataConversionError.RequiredColumnMissing"", ""OutputDataConversionError.ColumnNameInvalid"", ""OutputDataConversionError.TypeConversionError"", ""OutputDataConversionError.RecordExceededSizeLimit"", ""OutputDataConversionError.DuplicateKey"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all RequiredColumnMissing errors

#### Description
Shows all errors where the output record produced by your job has a missing column.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""OutputDataConversionError.RequiredColumnMissing""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all ColumnNameInvalid errors

#### Description
Shows errors where the output record produced by your job has a column name that doesn't map to a column in your output.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""OutputDataConversionError.ColumnNameInvalid""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all TypeConversionError errors

#### Description
Shows errors where the output record produced by your job has a column can't be converted to a valid type in the output

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""OutputDataConversionError.TypeConversionError""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all RecordExceededSizeLimit errors

#### Description
Shows errors where the size of the output record produced by your job is greater than the supported output size. 

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""OutputDataConversionError.RecordExceededSizeLimit""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
List all DuplicateKey errors

#### Description
Shows errors where the output record produced by job contains a column with the same name as a System column

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType == ""OutputDataConversionError.DuplicateKey""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"### General

#### Title
List all administrative operations

#### Description
Operations performed on the job such as start, stop, add input and output etc.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and Category == ""Authoring"" 
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Reference data logs

#### Description
Shows all diagnostic logs related to reference data operations.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type in (""ReferenceDataLoadSnapshot"" , ""ReferenceDataInputAdapterError"", ""ReferenceDataInputAdapterProcessBlobFailed"", ""ReferenceDataInputAdapterTransientError"", ""ReferenceDataScanSnapshots"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
All logs with level ""Error""

#### Description
Shows all logs that is likely to have negatively impacted your job.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and Level == ""Error"" 
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Operations that have ""Failed""

#### Description
Shows all operations on your job that have resulted in a failure

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and status_s == ""Failed"" 
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Output Throttling logs (cosmos db, pbi, event hubs)

#### Description
Shows all instances where writing to one of your outputs was throttled by the destination service.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type in (""DocumentDbOutputAdapterWriteThrottlingError"", ""EventHubOutputAdapterEventHubThrottlingError"", ""PowerBIServiceThrottlingError"", ""PowerBIServiceThrottlingError"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Transient input and output errors

#### Description
Shows all errors related to input and output that are intermittent in nature.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type in (""AzureFunctionOutputAdapterTransientError"", ""BlobInputAdapterTransientError"", ""DataLakeOutputAdapterTransientError"", ""DocumentDbOutputAdapterTransientError"", ""EdgeHubOutputAdapterEdgeHubTransientError"", ""EventHubBasedInputInvalidOperationTransientError"", ""EventHubBasedInputOperationCanceledTransientError"", ""EventHubBasedInputTimeoutTransientError"", ""EventHubBasedInputTransientError"", ""EventHubOutputAdapterEventHubTransientError"", ""InputProcessorTransientFailure"", ""OutputProcessorTransientError"", ""ReferenceDataInputAdapterTransientError"", ""ServiceBusOutputAdapterTransientError"", ""TableOutputAdapterTransientError"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


"
"#### Title
Summary of all data errors in the last 7 days

#### Description
Summary of all data errors in the last 7 days

#### Content
AzureDiagnostics
| where TimeGenerated > ago(7d) //last 7 days
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type == ""DataError""
| extend DataErrorType = tostring(parse_json(properties_s).DataErrorType)
| summarize Count=count(), sampleEvent=any(properties_s)  by DataErrorType, JobName=Resource


"
"#### Title
Summary of all errors in the last 7 days

#### Description
Summary of all errors in the last 7 days

#### Content
AzureDiagnostics
| where TimeGenerated > ago(7d) //last 7 days
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS""
| extend ErrorType = tostring(parse_json(properties_s).Type)
| summarize Count=count(), sampleEvent=any(properties_s)  by ErrorType, JobName=Resource


"
"#### Title
Summary of 'Failed' operations in the last 7 days

#### Description
Summary of 'Failed' operations in the last 7 days

#### Content
AzureDiagnostics
| where TimeGenerated > ago(7d) //last 7 days
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and status_s == ""Failed"" 
| summarize Count=count(), sampleEvent=any(properties_s) by JobName=Resource  


"
