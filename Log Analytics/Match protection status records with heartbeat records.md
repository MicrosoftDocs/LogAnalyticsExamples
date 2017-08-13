## Match protected status records with heartbeat records
#### #join #let #project #bin #round
<!-- article_id: 3107‎2017‏‎03827024 -->

This example finds related protection status records and heartbeat records, matched on both Computer and time.
Note the time field is rounded to the nearest minute. We used runtime bin calculation to do that: `round_time=bin(TimeGenerated, 1m)`.

```OQL
let protection_data = ProtectionStatus
    | project Computer, DetectionId, round_time=bin(TimeGenerated, 1m);
let heartbeat_data = Heartbeat
    | project Computer, Category, round_time=bin(TimeGenerated, 1m);
protection_data | join (heartbeat_data) on Computer, round_time
```

