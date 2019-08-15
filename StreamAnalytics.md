### Input data Errors

#### Title
List all input data errors

#### Description
Shows all errors that occurred while processing the data from inputs.

#### Content
AzureDiagnostics 
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).Type == ""DataError"" 
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level



#### Title
List all input deserialization errors

#### Description
Shows errors caused due to malformed events that could not be deserialized by the job.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and parse_json(properties_s).DataErrorType in (""InputDeserializerError.InvalidData"", ""InputDeserializerError.TypeConversionError"", ""InputDeserializerError.MissingColumns"", ""InputDeserializerError.InvalidHeader"", ""InputDeserializerError.InvalidCompressionType"")
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


#### Title
List all InvalidInputTimeStamp errors

#### Description
Shows errors caused due to events where value of the TIMESTAMP BY expression can't be converted to datetime

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""InvalidInputTimeStamp""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level


#### Title
List all InvalidInputTimeStampKey errors

#### Description
Shows errors caused due to events where value of the TIMESTAMP BY OVER timestampColumn is NULL

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""InvalidInputTimeStampKey""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level



#### Title
Events that arrived late

#### Description
Shows errors due to events where difference between application time and arrival time is greater than the late arrival policy.

#### Content
AzureDiagnostics
| where ResourceProvider == ""MICROSOFT.STREAMANALYTICS"" and  parse_json(properties_s).DataErrorType == ""LateInputEvent""
| project TimeGenerated, Resource, Region_s, OperationName, properties_s, Level
