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
