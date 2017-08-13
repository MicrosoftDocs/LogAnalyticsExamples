## Find accounts that failed to logon from computers on which we identify a security detection
#### #makeset #let #in #count
<!-- article_id: 3107‎2017‏‎03827019 -->

This example finds and counts accounts that failed to logon from computers on which we identify a security detection.
```OQL
let detections = toscalar(SecurityDetection
| summarize makeset(Computer));
SecurityEvent
| where Computer in (detections) and EventID == 4624
| summarize count() by Account
```