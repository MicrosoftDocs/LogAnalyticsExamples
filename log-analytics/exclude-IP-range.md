## Exclude IP range and specific IPs from results
#### #range #parse_ipv4 #binary_and #binary_shift_right #datatable
<!-- article_id: 1209201903827018 -->
This example shows how to exclude a list of IPs and a set of additinal specific IPs from query results.
```OQL
let generateIpRange = (fromIp: string, toIp: string){
 //convert input parameters to integers, and generate all integers between them to produce the full required IP range
 range IP from parse_ipv4(fromIp) to parse_ipv4(toIp) step 1
 //... then convert this range back into IPv4 strings
 | extend LSB = binary_and(IP, 255), IP = binary_shift_right(IP, 8) 
 | extend thirdBit = binary_and(IP, 255), IP = binary_shift_right(IP, 8)
 | extend secondBit = binary_and(IP, 255), IP = binary_shift_right(IP, 8)
 | extend MSB = binary_and(IP, 255)
 | project IpStr=strcat(MSB, ".", secondBit, ".", thirdBit, ".", LSB)
};
let additionalIps = 
 //define any additional IPs outside of the initial range that we might want to exclude
 datatable(IpStr:string)
 [
 "77.222.135.70", 
 "68.233.194.2", 
 "68.233.194.3", 
 "68.233.194.6", 
 "68.233.194.7", 
 "68.233.194.61",
 ];
let excludedIps = //put together in this table a superset of all the things we want to exclude
 union 
 generateIpRange("104.210.0.0", "104.210.255.255"), 
 additionalIps;
Heartbeat
| where TimeGenerated >= ago(1h)
| where ComputerIP != "" and ComputerIP !in (excludedIps)
| project TimeGenerated, ComputerIP
```