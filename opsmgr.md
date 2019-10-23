
## Sizing Exercise for Ops Manager Deployments
 
For the Ops Manager installation, the process we typically use is as follows:
* We send you a series of questions about your database and your requirements for backups
* We generate a sizing estimation to meet the specific needs.
* Once the figures are discussed, we propose an architecture or topology based on your high availability requirements.
 
If you are unfamiliar with a typical Ops Manager installation, please refer to the [introductory documentation](https://docs.opsmanager.mongodb.com/current/introduction/) that explains the components of the application and how they work together. This background knowledge may provide useful context for the sizing questionnaire.
 
---
 
## Sizing Questions
 
### **Use case**
1. How many MongoDB processes belong to replica sets and/or sharded clusters that will be managed and/or monitored by Ops Manager?
1. If leveraging Backups, would you prefer to store your backup snapshots in
   * A MongoDB instance(s) dedicated to backups (referred to as a [Blockstore](https://docs.opsmanager.mongodb.com/current/reference/glossary/#term-backup-blockstore-database)), or
   * In a filesystem location as database data files ([Filesystem Store](https://docs.opsmanager.mongodb.com/current/reference/glossary/#term-file-system-store)), or
   * [S3 Blockstore](https://docs.opsmanager.mongodb.com/current/reference/glossary/#term-s3-snapshot-store)?
1. Do you want high availability for your Ops Manager installation?
   - We define high availability in the context of Ops Manager as follows:
      - _All backing databases are replica sets with 3 data bearing nodes (Application Database, Blockstores, Oplog Stores)_
      - _HTTP Service (GUI Dashboard) is installed on multiple servers (Requires a HTTP load balancer to ensure seamless failover)_
 
 
### **Backups (if applicable):**
1. How many replica sets and/or cluster shards will be backed up by Ops Manager?
   - _Here is an example of a valid response template for this question:_

| Item                                                                            | Data size (uncompressed) | File size (compressed) | Oplog GB/day |
|:--------------------------------------------------------------------------------|:-------------------------|:-----------------------|:-------------|
| Replica Sets:                                                                   |                          |                        |              |
| rs_prod                                                                         |                          |                        |              |
| rs_dev                                                                          |                          |                        |              |
| rs_qa                                                                           |                          |                        |              |
| Clusters (each with its own config replica set and different amount of shards): |                          |                        |              |
| Sh_prod_cluster (2 shards, 1 config replica set)                                |                          |                        |              |
| sh_prod_1                                                                       |                          |                        |              |
| sh_prod_2                                                                       |                          |                        |              |
| prod_config                                                                     |                          |                        |              |
| Sh_dev_cluster (4 shards, 1 config replica set)                                 |                          |                        |              |
| sh_dev_1                                                                        |                          |                        |              |
| sh_dev_2                                                                        |                          |                        |              |
| sh_dev_3                                                                        |                          |                        |              |
| sh_dev_4                                                                        |                          |                        |              |
| dev_config                                                                      |                          |                        |              |
| Total: 11 (6 shards, 3 replica sets, 2 config replica sets)                     |                          |                        |              |

2. For each replica set or cluster shard, what is the:
   * Uncompressed total size of the data (GB)
   * File size used on the disk (GB) - This value is the compressed size if you are using the WiredTiger storage engine.
        * If you don’t still know the File size please let us know how compressible is the data to be backed up? Is it text, videos, binaries?
   * Oplog/day (GB)
      * _Provide the output of `rs.printReplicationInfo()` ran via Mongo Shell on the current primary of the replica set or cluster shard._
      * _If this is a new environment with no data yet, please provide your best estimate to the nearest GB on how much data you are going to update / insert every day._
      * Estimated Write Operations per Second (insert/updates/deletes)
         * _Provide the output of `use local; db.oplog.rs.count();` ran via Mongo Shell on each replica set_
      * What is your expected growth over the next 6, 12, and 18 months? “Growth” includes (but is not limited to):
         * _Size of the data stored in the environment (uncompressed total data size and file size):_
         * _Increase in the number of operations run against the environment (ops/second and oplog/day):_
         * _Addition of new replica sets, sharded clusters, or cluster shards:_
 
 
### **Backup Snapshots (if applicable):**
_(if you have multiple replica sets or cluster that needs to be backup please specify these values for each one)_
1. How many hours apart should a short term snapshot be taken? _(6/8/12/24) Default=24_
2. How many days should short term snapshots be kept? _(1-5) Default=2_
3. How many Daily snapshots should be kept? _(0-360) Default=0 (disabled)_ - not applicable if short terms snapshots are set to 24
4. How many Weekly snapshots should be kept? _(0-52) Default=2_
   - Weekly snapshots must be stored for longer than daily snapshots.
5. How many Monthly snapshots should be kept? _(0-36) Default=1_
   - Monthly snapshots must be stored for longer than weekly snapshots.
6. Do you want point-in-time (PIT) restores? _(Yes/No)_
    6a. If `Yes`, how many days back will you need to be able to restore using PIT restores? _(1-360) Default=1_
    6b. If `Yes`, how frequently (in minutes) will you need [cluster checkpoints](https://docs.opsmanager.mongodb.com/current/core/backup-preparations/#checkpoint) to be created?  _(15/30/60) Default=30_
 
### **Additional Considerations:**
- In question 4 of the Usage section, the `Blockstore` is a MongoDB replica set. We recommend a three node replica set for all backing databases for high-availability.  Please note, disk space requirements will increase since snapshot blocks will be copied to all nodes.
- Depending on resource constraints and load, the Blockstore and Oplog Store may run on different replica sets on the same servers, or they may also be combined onto a single replica set. However, the Application Database (which Ops Manager is installed on) must live separately in its own replica set. The [cacheSizeGB](https://docs.mongodb.com/manual/reference/configuration-options/#storage.wiredTiger.engineConfig.cacheSizeGB) parameter may need to be adjusted if multiple `mongod` processes run on any given server.
- The `Oplog/day` calculation we make in question 2 of the Backup Snapshots section is an approximation due to the ever changing nature of the oplog. For the most accurate sizing estimate, you would need to gather these metrics over a period of your highest load.



1. How many data centers will this environment managed or monitored by Ops Manager spread across?
   - If more than one, how are these geographically distributed?
1. Do you want to deploy Ops Manager on multiple data centers?
   - Do you have any network data traffic restriction across your multiple data centers?
1. Which are your RTO (recovery time objective) requirements for each of MongoDB Environment you are backing up?
   - This can affect our proposed architecture. Lower RTO values will require more hardware and network resources.
1. Is there a standardized machine specification you would like to use with this deployment? If so, please provide the following:
      * _Number of servers available:_
      * _Are these physical, virtual machines or cloud servers?_
      * _Number of CPU cores per server:_
      * _Amount of RAM per server:_
      * _Disk type (Magnetic or SSD), size, and disk configuration (physical, virtual):_
      * _Disk space available per server to this install:_
      * _Are you allowed to add more disk space easily in the future?_
   - If it is somewhat difficult to procure additional hardware resources at your organization, we recommend sizing up for more than you will immediately need.
 
 
## Additional questions that affect the Ops Manager installation procedure
 
1. Will you be using LDAP or other security options like Kerberos, x509, or SSL?
1. Do you have root access for the servers on which you will be installing the application?
1. Do the servers hosting the Ops Manager application have access to the outside internet in order to download the latest versions of MongoDB/agents? Please describe any outbound connectivity constraints.
