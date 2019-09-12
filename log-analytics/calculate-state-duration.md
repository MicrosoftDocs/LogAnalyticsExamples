## Calculate the duration of a VM state, logged continuously
#### #datatable #sort #prev

This example reviews status reports of VMs, which are either Running or Waiting, and can change from one to the other several times, and calculates the waiting time of each VM.
```OQL
datatable (VMName:string, Status:string, TimeGenerated:datetime)
[
  "VM1", "Running", datetime('2018-11-13T19:27:16.000'),
  "VM1", "Running", datetime('2018-11-13T19:32:17.000'),
  "VM2", "Running", datetime('2018-11-13T19:31:10.000'),
  "VM2", "Waiting", datetime('2018-11-13T19:29:17.000'),
  "VM1", "Waiting", datetime('2018-11-13T19:28:14.000'),
  "VM1", "Waiting", datetime('2018-11-13T19:29:15.000'),
  "VM1", "Waiting", datetime('2018-11-13T19:30:19.000'),
  "VM2", "Waiting", datetime('2018-11-13T19:25:12.000'),
  "VM2", "Running", datetime('2018-11-13T19:26:10.000'),
]
| sort by VMName asc, TimeGenerated asc
| extend Status_changed = (VMName != prev(VMName) or Status != prev(Status))
| where Status_changed == true
| extend Waiting_time = iff(Status=="Running" and prev(Status)=="Waiting", tostring(TimeGenerated-prev(TimeGenerated)), "null")
```

VMName       |Status       |TimeGenerated           |Status_changed |Waiting_time
-------------|-------------|------------------------|---------------|--------------
VM1          |Running      |"2018-11-13T19:27:16Z"  |true           |null
VM1          |Waiting      |"2018-11-13T19:28:14Z"  |true           |null
VM1          |Running      |"2018-11-13T19:32:17Z"  |true           |"00:04:03"
VM2          |Waiting      |"2018-11-13T19:25:12Z"  |true           |null
VM2          |Running      |"2018-11-13T19:26:10Z"  |true           |"00:00:58"
VM2          |Waiting      |"2018-11-13T19:29:17Z"  |true           |null
VM2          |Running      |"2018-11-13T19:31:10Z"  |true           |"00:01:53"
