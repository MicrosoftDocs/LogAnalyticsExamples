## Parse activity name and ID
#### #project #parse #split
<!-- article_id: 3107‎2017‏‎03827025 -->

The 2 examples below rely on the fixed structure of the Activity column: <ID>-<Name>.

The first example uses the *parse* operator to assign values to 2 new columns: activityID and activityDesc.
```OQL
SecurityEvent
| take 100
| project Activity 
| parse Activity with activityID " - " activityDesc
```

This example uses the *split* operator to create an array of separate values
```OQL
SecurityEvent
| take 100
| project Activity 
| extend activityArr=split(Activity, " - ") 
| project Activity , activityArr, activityId=activityArr[0]
```