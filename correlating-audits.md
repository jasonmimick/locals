Correlating Audits in MongoDB Enterprise
===

Scenario: A MongoDB administrator logs into Ops Manager and creates
a new database user name `User1`  for a project in Ops Manager. This event is
then deployed to multiple database nodes and applied accordingly.


Problem: 
The audit log for `mongod` will how the user `User1` as being
created by the `automation-agent` user rather than the
actual user performed the action in Ops Manager.

Solution:
Perform a procedure to correlate various audit events with their
corresponding Ops Manager events.

Procedure
===

Find all the audit event types:

```bash
$docker exec vibrant_keldysh cat /data/audit.log | jq '.atype'  | sort | uniq -c
  80524 "authCheck"
  12601 "authenticate"
      1 "createCollection"
      1 "createUser"
```

Find all the Ops Mgr Global Events

```bash
curl -u "${OM_USER}:${OM_API_KEY}" --digest "http://localhost:8080/api/public/v1.0/globalEvents?pageNum=1" | jq '.'
```

