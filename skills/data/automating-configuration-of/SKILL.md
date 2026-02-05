# Automating Configuration of InterSystems IRIS with

Introduction to Configuration Merge

This page explains the configuration mer ge feature of InterSystems IRIS® data platform, what types of operations configuration merge can perform, and its primary use cases.

### 1.1 Configuration Merge

The configuration mer ge feature lets you make as many changes as you wish to the configuration of an y InterSystems IRIS instance in a single operation. To use it, you simply record the changes you want to make in a declarative configuration merge file and apply that file to the instance, when it is deplo yed or at any later point. Configuration mer ge can easily be used to automatically deploy multiple instances with varying configurations from the same container image or kit, as well as to simultaneously reconfigure multiple running instances, enabling automated reconfiguration of clusters or other multiinstance deployments. Configuration mer ge can be used in deployment of any InterSystems IRIS instance, containerized or locally installed, on any supported UNIX® or Linux platform, including Linux cloud nodes. You can reconfigure running instances using configuration mer ge on both UNIX/Linux and Windows platforms.

For examples of configuration mer ge files used to deplo y containers, see Deploying an InterSystems IRIS Container with a Merge File. The Configur ation Parameter File Reference contains a comprehensive description of all InterSystems IRIS configuration parameters.

### 1.2 InterSystems IRIS Configuration

The configuration of an InterSystems IRIS instance is determined by a file in its installation directory named contains configuration parameters as name/v alue pairs. Every time the instance starts, including for the first time after it is deployed, it reads this configur ation parameter file , or CPF, to obtain the values for these settings. This allows you to reconfigure an instance at an y time by modifying its CPF and then restarting it.

iris.cpf, which

For example, the globals setting in the [config] section of the CPF determines the size of the instance’s database cache. The setting in the CPF of a newly installed instance specifies an initial cache size equal to 25% of total system memory , which is not intended for production use. To change the size of the database cache, you can open the instance’s CPF in any text editor and specify the desired cache size as the value of globals, then restart the instance. Most parameters can be
changed using other methods; for example, you can also modify the value of globals using the Management Portal or using
the methods in the persistent class Config.config. Updating an instance’ that lets you make multiple configuration changes to an instance in a single operation and automate the simultaneous configuration of multiple instances.

s CPF, however, is the only general mechanism

For an overview of the use and contents of the CPF, see the Configur ation Parameter File Reference.

### 1.3 Configuration Merge File

A configur ation merge file is a partial CPF that contains any desired subset of InterSystems IRIS configuration parameters and values or an [Actions] section or both. When a merge file is applied to an instance with configuration mer are two types of operations that can occur. The first type is updating settings in the instance’ s CPF corresponding to the InterSystems IRIS configuration parameters and v alues specified in the mer ge file, see Merge Updates. The second type is creating, deleting, or modifying InterSystems IRIS objects corresponding to the contents of the [Actions] section, see
Merge Actions.

ge, there

A merge file has the same syntax as a CPF (described in the CPF Format section), and can have any name and extension. The merge file may contain an y of the parameters found within the CPF, though it is not necessary to include the values you are not changing.

Unlike the CPF, a merge file can contain duplicates of the same section and parameter . In this case, InterSystems IRIS prioritizes the value closer to the end of the file, which allo ws you to create a template merge file. F or example, if you keep generally desired values at the top of the file and append instance-specific v prioritize the instance-specific v alues when reading the merge file.

alues at the bottom, InterSystems IRIS will

### 1.4 Merge Updates

When a merge file is applied to an instance with configuration mer those settings are merged into the instance’s CPF, replacing the values, as if you had edited the CPF and changed the values manually. If a parameter in the merge file is not present in the original CPF , it is simply added in the appropriate place.

ge to update InterSystems IRIS configuration parameters,

For example, the data and compute nodes in a sharded cluster typically require with a database cache that is much larger than that generally configured for other purposes, and ha ve more shared memory configured as well. To configure an instance to have a larger database cache and more shared memory when deployed, or to reconfigure an e xisting instance this way, you can apply a configuration mer ge file that includes the globals parameter (which specifies the size of the
database cache) and the gmheap parameter (which specifies the amount of shared memory) with the desired v alues; these
replace the default values in the CPF of the instance. The following illustrates the use of a merge file to update both the
parameters when deploying an instance:

Figure 1–1: Merge File Updates Memory Settings During Deployment

Merge Actions

For examples of using configuration mer ge to update configuration parameters, see Useful Update Parameters in Automated
Deployment.

### 1.5 Merge Actions

In addition to changing the values of configuration parameters, configuration mer
of different InterSystems IRIS objects, such as namespaces and databases; users, roles, and resources; and mirrors and
mirror members. This is done using the parameters in the [Actions] section, which is valid only in a merge file and does not appear in (and cannot be added to) an instance’s CPF. For example, to add a global mapping to an instance, you would include in the merge file an [Actions] section containing the CreateMapGlobal parameter. The parameters in this section, which create, modify, and delete system objects, are sometimes called action parameters, to distinguish them from those that update parameter values, which are known as update parameters.

ge can create, modify, and delete dozens

Action parameters can be used to manage objects on both new and existing instances. The operations specified by action
parameters are idempotent, meaning that they are executed only if they would result in a change. More specifically:

- A Create action is not executed if the specified object e xists.

- A Modify action is not executed if the specified object does not e xist. (If the object exists but the action does not add to/modify the properties of the object, the action is executed but to no effect.)

- A Delete action is not executed if the specified object does not e xist.

defaultiris.cpfmergefiledeployediris.cpf[ConfigFile]...[config]...[ConfigFile]...

- A Config action is not e xecuted if the object exists and the action does not add to/modify the properties of that object;
if the object does not exist, or it exists and the action adds to/modifies its properties, the action is e xecuted.

Action parameters are very useful in deployment, for example to configure se veral deployed instances as a mirror using the ConfigMirror action and the MirrorSetName and MirrorDBName properties of the CreateDatabase action, enabling the new mirror to be fully operational, with mirrored databases in place, immediately following deployment. On the other hand, when used in reconfiguring an e xisting instance with the iris merge command, action parameters can enable
you to immediately make changes that would otherwise require a Management Portal procedure or a class method call;
notable examples are adding an arbiter to an existing mirror and adding a new database to an existing mirror using the MirrorSetName and MirrorDBName properties of the ModifyDatabase action, which must be done on the running primary instance.

The operations performed by action parameters are effected by calling methods of classes in the Config and Security packages, the SYS.Database and %SYSTEM.SQL.Security classes, as well as two SQL commands.

For examples of the use of action parameters, see Useful Action Parameters in Automated Deployment.

For the list of available action parameters, see [Actions] Parameter Reference.

### 1.6 Configuration Merge Uses

There are two primary uses for configuration mer ge:

- Configuring multi-instance topologies and stand-alone instances during deplo yment.

- Reconfiguring deplo yed multi-instance topologies and stand-alone instances.

For more information on using configuration mer ge during deployment, see Configuration Mer ge in Deployment.

For more information on using configuration mer ge to reconfigure e xisting InterSystems IRIS instances, see Reconfigure an Existing Instance Using Configuration Mer ge.

### 1.7 See Also

- This page describes the use case of configuration mer ge related to configuring multi-instance topologies and stand-alone instances during deployment. The use case of configuration mer ge related to reconfiguring an e xisting instance is described ge.

Applying a configuration mer ge file during deplo yment lets you modify the default configurations of the deplo yed instance before it starts for the first time. This enables you to deploy containers with varying configurations from the same image, or install differently-configured instances from the same kit, directly into a multi-instance topology , rather than having to configure the instances into the desired topology after deplo yment. For example, in automated containerized deployment of a sharded cluster with compute nodes, you can apply different merge files for data node 1, the remaining data nodes,
and the compute nodes in that order, as shown in the following illustration; when all of the instances are up and running,
so is the sharded cluster.

Figure 2–1: Automated Deployment of a Sharded Cluster Using Configuration Merge

In similar fashion, when deploying a mirror, you would apply different configuration mer ge files for the primary , backup, and async members. Even a mirrored sharded cluster is easily deployed using this approach.

node1remainingdatanodescomputenodesdatanode1InterSystems...configurationmergefi...312

Activating configuration mer ge during deployment requires only that the location of the merge file be specified by the environment variable ISC_CPF_MERGE_FILE, or by the field used for that purpose in the InterSystems K ubernetes
Operator (IKO). For example, in manual or scripted deployment:

ISC_CPF_MERGE_FILE=/home/user/mergefiles/cmf_090821.cpf

The specific manner in which you specify the mer ge file depends on the deplo yment mechanism you are using and whether the instance is containerized or noncontainerized.

- Deploying an InterSystems IRIS container

- Installing InterSystems IRIS from a kit

- Deploying with the InterSystems Kubernetes Operator

### 2.1 Deploying an InterSystems IRIS Container with a Merge File

When deploying an InterSystems IRIS container, the environment variable and merge file can be included in the follo wing
ways:

- Include them in the script or docker-compose.yml file you are using for deplo yment.

In the following sample deployment script, the merge file specified by ISC_CPF_MERGE_FILE, as well as the license key, are staged on the external volume specified for durable %SYS by ISC_DATA_DIRECTORY so they are accessible inside the container.

#!/bin/bash
# script for quick demo and quick InterSystems IRIS image testing

# Definitions to toggle_________________________________________
container_image="intersystems/iris:latest-em"

# the docker run command

docker run -d -p 9091:1972 -v /data/durable263:/durable -h iris --name iris
--cap-add IPC_LOCK
--env ISC_DATA_DIRECTORY=/durable/irisdata
--env ISC_CPF_MERGE_FILE=/durable/merge/CMF.cpf
$container_image
--key /durable/key/iris.key

Note:

The image tags shown in this document are examples only. Please go to the InterSystems Container Registry (ICR) to browse current repositories and tags.

This sample docker-compose.yaml file contains the same elements as the deplo yment script.

Installing InterSystems IRIS from a Kit with a Merge File

version: '3.2'

services:
iris:
image: intersystems/iris:latest-em command: --key /durable/key/iris.key hostname: iris

ports:
# 1972 is the superserver default port
- "9091:1972"

volumes:
- /data/durable263:/durable

environment:
- ISC_DATA_DIRECTORY=/durable/irisdata
- ISC_CPF_MERGE_FILE=/durable/merge/CMF.cpf

- Include the merge file in the container image and the en vironment variable in the script or Docker compose file used in deployment.

When creating a custom InterSystems IRIS container image by starting with an InterSystems IRIS image from Inter- Systems and adding your own code and dependencies, you can execute the iris merge command in the Dockerfile to reconfigure the InterSystems IRIS instance contained in the image. F or example, you can run the iris merge command with a merge file with [Actions] parameters to add namespaces and databases to the instance, which will then be present on the instance in every container created from your custom image. This method is explained and illustrated in Creating InterSystems IRIS Images in Running InterSystems Products in Containers.

If you want the containerized instances to continue to use the merge file you placed in the container , you can set ISC_CPF_MERGE_FILE in your script or compose file to the location of this file. You can also run an additional,
separate merge during deployment using a merge file positioned on the durable SYS v olume, as illustrated above; if
you plan to do this, add a command in the Dockerfile to remo ve the included merge file after it has been applied to the instance.

For examples of use cases for automated deployment using configuration mer ge, see Useful Update parameters in automated deployment and Useful Action parameters in automated deployment.

### 2.2 Installing InterSystems IRIS from a Kit with a Merge File

To apply a merge file when installing InterSystems IRIS from a kit, manually or in a script, you must separate installation from startup, using the steps below.

On UNIX® or Linux system:

1.

Install the instance without starting it by preceding the irisinstall or irisinstall_silent script with the
ISC_PACKAGE_STARTIRIS parameter, as follows:

ISC_PACKAGE_INSTANCENAME="IRIS27" ISC_PACKAGE_STARTIRIS="N" /tmp/iriskit/irisinstall

2. Start the instance with the iris start command, preceding it with the ISC_CPF_MERGE_FILE variable, as follows:

ISC_CPF_MERGE_FILE=/tmp/iriskit/CMF/merge.cpf iris start IRIS27

On a Windows system:

1.

Install and start the instance, for example:

IRIS-2023.2.0.227.0-win_x64.exe /instance IRIS27 INSTALLDIR=C:\InterSystems\IRIS27

2. When the instance is fully started, use the iris merge command (as described in Reconfigure an e xisting instance using

configuration mer ge) to apply your merge file:

iris merge IRIS27 C:\InterSystems\IRIS27\merge.cpf

### 2.3 Using a Merge File when Deploying with the InterSystems Kubernetes Operator

Kubernetes is an open-source orchestration engine for automating deployment, scaling, and management of containerized workloads and services. The InterSystems Kubernetes Operator (IKO) extends the Kubernetes API with the IrisCluster custom resource, which can be deployed as an InterSystems IRIS sharded cluster, distributed cache cluster, or standalone instance (all optionally mirrored) on any Kubernetes platform. The IKO also adds InterSystems IRIS-specific cluster management capabilities to Kubernetes, enabling automation of tasks like adding nodes to a cluster, which you would otherwise have to do manually by interacting directly with the instances.

When deploying with the IKO, you use a Kubernetes ConfigMap to integrate one or more merge files into the deplo yment process. For detailed information, see Create configuration files and pro vide a config map for them in Using the InterSystems
Kubernetes Operator.

### 2.4 See Also

- Reconfigure an Existing Instance Using
Configuration Merge

- This page describes the use case of configuration mer ge related to reconfiguring deplo yed multi-instance topologies and stand-alone instances. The use case of configuration mer ge related to deployment is described Configuration Mer ge in
Deployment.

- By automating application of the same merge file to multiple running instances, you can simultaneously reconfigure all of those instances in the same way, applying the same set of configuration changes across your application or cluster . You can avoid updating settings that may have been customized on a per-instance basis and should not be modified simply by omitting these from the merge file, while including only those you kno w it is safe and desirable to change. A single automated program can of course apply different merge files to dif ferent groups of instances (such as different mirror member or cluster nodes types) as described in the previous section.

Applying all configuration changes with a mer ge file helps you streamline the process of making changes and maintain greater control over the instance’s configuration. Rather than making numerous indi vidual changes from the Terminal, on multiple pages of the Management Portal, or by editing an instance’s CPF manually, you can execute all the changes at once using identical syntax in a merge file. By k eeping your merge files under v ersion control, you ensure the availability of configuration history and the option of restoring a pre vious configuration.

### 3.1 The iris merge Command

The iris merge command, which can be used on both UNIX/Linux and Windows systems, applies a merge file to a running
instance. For Windows operating systems, it requires OS authentication to execute. It is executed as follows:

iris merge instance [merge-file] [target-CPF]

where:

- instance is the name of the InterSystems IRIS instance.

- merge-file is the absolute or relative path to the merge file, including the filename. If merge-file is not specified, the value of the ISC_CPF_MERGE_FILE environment variable is used, if it is set.

- target-CPF is the absolute or relative path to the active CPF for instance instance, which is assumed to be named
iris.cpf. If target-CPF is not specified, the def aults are as follows:

Reconfigure an Existing Instance Using Configuration Merge

–

–

–

For noncontainerized instances, the iris.cpf file located in the directory specified by the ISC_PACKAGE_INSTALLDIR environment variable, if it is set. For most existing instances, this variable is not set, and you must explicitly specify the location of the target CPF.

For containerized instances, the iris.cpf file located in the directory specified by the ISC_DATA_DIRECTORY environment variable or, if it is not set (because durable %SYS is not in use), the ISC_PACKAGE_INSTALLDIR environment variable, which is always set in an InterSystems IRIS container.

If the environment variables ISC_DATA_DIRECTORY and ISC_PACKAGE_INSTALLDIR are not set and target-CPF is not specified, InterSystems IRIS checks for the location of

target-CPF in the operating system registry.

No merge is performed if:

- The specified mer ge file is not present, or the merge-file argument is omitted and ISC_CPF_MERGE_FILE does not exist.

- There is no CPF in the specified tar get location or all three of the following conditions: 1) the target location is not specified, 2) neither ISC_DATA_DIRECTORY or ISC_PACKAGE_INSTALLDIR exist and 3) the operating system registry does not have the path for target-CPF defined.

An exit code of 0 indicates a successful merge.

After entering the command, an InterSystems IRIS terminal prompts for you to supply a username and password (if OS authentication is not enabled). Only once authentication succeeds does the command complete execution. On an unsuccessful merge, the terminal indicates which line the merge failed on and you can press any key to close the window. On a successful merge, the success message displays for three (3) seconds before the window closes automatically.

Some changes merged into a CPF will not take effect immediately, but require a restart. For example, a change in the value of the gmheap parameter, which determines the size of the instance’s shared memory heap, does not take effect until the instance is restarted. When your merge file contains one or more such parameters, you may need to apply the mer ge file
as part of a restart, as in the following sample script excerpt:

# restart instance with the necessary parameters (all on one line)
sudo ISC_CPF_MERGE_FILE=/net/merge_files/config_merge.cpf iris stop IRIS restart

On the other hand, applying a merge file with the
require a restart, including those that cannot be set during instance startup; an example, as noted in Merge Actions, is adding
a database to an existing mirror.

iris merge command lets you immediately change settings that do not

Important: When a container is deployed with configuration mer ge (as described in Deploying an InterSystems IRIS container with a merge file ), the merge file specified by ISC_CPF_MERGE_FILE (which is persistent in the container) is continuously monitored for updates as long as the container is running, with updates immediately merged by an iris merge command when they occur. This means that you can update the configuration of a containerized instance at an y time by updating its merge file, making it easier to automate reconfiguration of containerized instances and clusters.

### 3.2 See Also

- Useful Update Parameters in Automated
Deployment

- The configuration mer ge feature can be used to update any combination of settings in an instance’s CPF. Several automated deployment use cases that you may find useful and mak e good examples of the power of the configuration mer ge feature, along with the parameters involved, are discussed in this page. The following sections are related to merge updates to update parameters in the instances CPF and are those used to modify values in the deployed instance’s CPF before the instance is started, thereby updating the default CPF in the deployment source (installation kit or container). Each parameter name provided is linked to its listing in the Configur ation Parameter File Reference so you can easily review a parameter’s purpose and details of its usage.

- 4.1 Change the Default Password As described in Authentication and Passwords in Running InterSystems Products in Containers, you can use the PasswordHash setting in the [Startup] section to customize the default password of the predefined accounts on an instance at deployment, which eliminates the serious security risk entailed in allowing the default password of SYS to remain in effect. (The password of each predefined account should be indi vidually changed following deployment.) Table 4–1: Password Parameter

[Startup]
Parameter

PasswordHash

Specifies

Default password for the predefined user accounts based on a cryptographic hash of the value and its salt

Note:

The [Actions]/CreateUser parameter also takes a PasswordHash argument that is equivalent to the parameter (see [Actions] Parameter Reference).

### 4.2 Configure and Allocate Memory

There are a number of parameters affecting an InterSystems IRIS instance’s memory usage, the optimal value of which can depend on the physical memory available, the instance’s role within the cluster, the workload involved, and performance requirements.

For example, the optimal size of an instance’s database cache, which can be specified using the globals parameter, can vary
greatly depend on the instance’s role; as noted above, sharded cluster data nodes typically require a relatively large cache.
But even within that role, the optimal size depends on the size of the cluster’s sharded data set, and the implemented size may be smaller than optimal due to resource constraints. (For more information, see Planning an InterSystems IRIS Sharded Cluster in the Scalability Guide.) Further, because the database cache should be carefully sized in general, the default database cache setting (the value of globals in the iris.cpf file pro vided in the container) is intentionally unsuitable for any production environment, regardless of the instance’s role.

Some of the memory usage settings in the [Config] section of the CPF that you might want to update as part of deployment
are listed in the following table:

Table 4–2: Memory Parameters

[Config]
Parameter

Specifies

bbsiz

globals

routines

gmheap

jrnbufs

locksiz

Maximum process private memory per process

Shared memory allocated to the database cache (not from shared memory heap)

Shared memory allocated to the routine cache (not from shared memory heap)

Shared memory configured as the shared memory heap

Shared memory allocated to journal buffers from the shared memory heap

Maximum shared memory allocated to locks from the shared memory heap

For more detail on these and other memory-related parameters, see System Resource Planning and Management, Memory and Startup Settings, Configuring Journal Settings , and Monitoring Locks.

### 4.3 Configure SQL and SQL Shell Options and Map SQL Datatypes

You can specify the SQL and SQL Shell settings for instances you are deploying by merging one or more of the parameters in the [SQL] section of the CPF. In the Management Portal these settings can be reviewed and modified on the SQL page (System Administration > Configuration > SQL and Object Settings > SQL). You can map SQL system data types and SQL user data types to their InterSystems SQL equivalents on deployed instances using the [SqlSysDatatypes] and [SqlUserDatatypes] sections of the CPF, respectively. For more detail on SQL Shell setting and datatype mapping, see Configuring the SQL Shell

and Data Types (SQL), respectively.

Update Parameter Example

### 4.4 Update Parameter Example

The following sample CPF merge file includes some of the update parameters discussed in the preceding sections. The SystemMode parameter specifies a label that is displayed at the top of the Management Portal.

[Startup]
SystemMode=TEST
PasswordHash=FBFE8593AEFA510C27FD184738D6E865A441DE98,u4ocm4qh

[config] bbsiz=-1 globals=0,0,900,0,0,0 routines=64 gmheap=256000 jrnbufs=96 locksiz=1179648

[SQL]
DefaultSchema=user TimePrecision=6

[SqlSysDatatypes]
TIMESTAMP=%Library.PosixTime

### 4.5 See Also

- Configuration Mer ge in Deployment

- ge

- Useful Action Parameters in Automated
Deployment

The configuration mer ge feature can be used to execute certain operations on the instance as specified in the [Actions] section. Several automated deployment use cases that you may find useful and mak e good examples of the power of the configuration mer ge feature, along with the parameters involved, are discussed in this page.

The sections related to creating, modifying, or deleting InterSystems IRIS objects are among those that can be included in the [Actions] section to create, modify, or delete different types of objects on an instance as part deployment (or
reconfiguration), including databases, namespaces, and mappings; users, roles, and resources; and man y more. The use of
action parameters (often simply called actions) is described in merge actions, the comprehensive list of actions is available in [Actions] Parameter Reference

### 5.1 Create, Modify, and Delete Security Objects

Include the operations described in the following table in the [Actions] section to create and modify security objects as part of deployment or reconfiguration.

Table 5–1: Sample Security Object Creation Parameters

[Actions] Parameter

Specifies

CreateUser

CreateRole

The name and properties of the user account to be created. You can also use ModifyUser and DeleteUser.

The name and properties of the role to be created.You can also use ModifyRole and DeleteRole.

CreateResource

The name and properties of the resource to be created. You can also use ModifyResource and DeleteResource.

GrantAdminPrivilege,
GrantPrivilege

The user account to grant SQL admin privileges and SQL privileges to, the privileges to be granted, and the namespace to grant them in. You can also use RevokeAdminPrivlege and RevokePrivilege.

ModifyService

The service to enable or disable.

CreateApplication

The name and properties of the application to be created. You can also use ModifyApplication and DeleteApplication.

CreateSSLConfig

The name, location, and properties of the TLS/SSL configuration to be created. You can also use ModifySSLConfig and DeleteSSLConfig.

CreateLDAPConfig

The name and properties of the LDAP configuration to be created. You can also use ModifyLDAPConfig and DeleteLDAPConfig.

CreateEvent

The name, properties and status of the system audit event to be created. You can also use ModifyEvent and DeleteEvent.

To illustrate the use of action parameters with security objects, suppose you wanted to add to deployed instances a predefined
account for a SQL administrator user who:

- Has SQL access through the %Service_Bindings service (%SQL role).

- Can read from or write to the USER database (%DB_USER role).

- Can create and drop tables, views, procedures, functions, methods, queries, and triggers (%DB_OBJECT_DEFINITION privilege) and use the BUILD INDEX command (%BUILD_INDEX privilege) in the USER namespace.

To do this, you could use the CreateUser parameter to create the user account with password and assign it the needed
roles, and the GrantAdminPrivilege parameter to grant it the needed SQL privileges, as follows:

[Actions]

CreateUser:Name=SQLAdmin,
PasswordHash="cec6638a357e7586fddfb15c0e7dd5719a1964e774cd37466fb0c49c05, 323cb89148c887166dd2be61c107710539af2c01b43f07dccc8d030ac2c1a8cf7c5ace4a00d57e3780f,10000,SHA512",
Roles="%SQL,%DB_USER"

GrantAdminPrivilege:Grantee=SQLAdmin,Namespace=USER,AdminPriv="%DB_OBJECT_DEFINITION,%BUILD_INDEX"

For information about the operations performed by these action parameters and the values of their properties, see Authentication and Passwords, About InterSystems Authorization, and SQL Users, Roles, and Privileges.

#### 5.1.1 Security Macros

InterSystems IRIS supports a set of macros that you can use in the [Actions] section of the configuration mer ge file (CMF). These macros relate to the AutheEnabled property for the Security.Applications, Security.Services, Security.System,

and Security.Users classes as well as the LDAPFlags property in the Security.LDAPConfigs class. Supported macros are listed below.

AutheEnabled macros:

Create, Modify, and Delete Security Objects

- AutheK5CCache — Enables Kerberos credential cache authentication.

- AutheK5Prompt — Enables Kerberos password prompt authentication.

- AutheK5API — Enables Kerberos username and password authentication.

- AutheK5KeyTab — Enables Kerberos keytab file authentication.

- AutheOS — Enables operating system authentication.

- AuthePassword — Enables password authentication.

- AutheUnauthenticated — Enables unauthenticated access.

- AutheKB — Enables Kerberos base connection security level.

- AutheKBEncryption — Enables Kerberos with Encryption connection security level.

- AutheKBIntegrity — Enables Kerberos with Packet Integrity connection security level.

- AutheLDAP — Enables LDAP authentication.

- AutheLDAPCache — Enables LDAP cached credentials for LDAP authentication.

- AutheDelegated — Enables delegated authentication.

- AutheLoginToken — Enables creation of Login Cookies.

- AutheKerberosDelegated — Enables using Kerberos for authentication then uses delegated authorization.

- AutheOSDelegated — Enables using the operating system to authenticate the user then uses delegated authorization.

- AutheOSLDAP — Enables Operating Systems authentication then LDAP authorization.

- AutheTwoFactorSMS — Enables SMS two factor authentication for a user.

- AutheTwoFactorPW — Enables one-time password two factor authentication for a user.

- AutheAlwaysTryDelegated — Enables using delegated authentication code for users authenticating with instance authentication.

- AutheMutualTLS — Enables mutual TLS when modifying %Service_WebGateway.

LDAPFlags macros:

- LDAPActiveDirectory — Indicates that the LDAP server is a Windows Active Directory server.

- LDAPTLSConnection — Enables use of TLS for LDAP sessions.

- LDAPAllowISCLDAPCONFIGURATION — Enables use of the ISC_LDAP_CONFIGURATION environment variable if using OS-based LDAP and multiple domains to determine which LDAP configuration to use for authentication.

- LDAPUseGroups — Enables using LDAP groups for Roles/Routine/Namespace.

- LDAPUseNestedGroups — Enables searching to return all of a user's nested LDAP groups.

- LDAPUniversalGroups — Enables searches using attributes on the LDAP server that are relevant for all InterSystems IRIS instances.

- LDAPEnabled — Enables the LDAP configuration.

- LDAPKerberosOnly — Enables use of Kerberos only for an LDAP configuration.

Example of enabling password authentication and unauthenticated access for %Service_ComPort:

[Actions]
ModifyService:Name=%Service_ComPort,AutheEnabled=$$$AuthePassword+$$$AutheUnauthenticated

Example of using some LDAPFlags macros to create a new LDAP configuration. Note that the v alues for LDAPBaseDN and LDAPBaseDNForGroups contain “=”, so the values must be enclosed in quotes.

[Actions]
CreateLDAPConfig:Name=TestLDAP,LDAPBaseDNForGroups="DC=testcompany,DC=com",LDAPHostNames="testcompany",LDAPBaseDN="DC=testcompany,DC=com",LDAPSearchUsername="ldapadmin",LDAPSearchPassword=SYS,LDAPFlags=$$$LDAPActiveDirectory+$$$LDAPUseGroups+$$$LDAPUseNestedGroups+$$$LDAPEnabled

### 5.2 Create, Modify, and Delete Database Objects

Include the operations described in the following table in the [Actions] section to create databases (both local and remote), namespaces, and mappings as part of deployment or reconfiguration.

Table 5–2: Sample Database and Namespace Action Parameters

[Actions]
Parameter

CreateDatabase

Specifies

The database’s name and properties to be registered in InterSystems IRIS and the location on the host file system of the database file to be created. You can also use ModifyDatabase and DeleteDatabase.

CreateDatabaseFile

The location on the host file system of the database file to be created (without registering the database in InterSystems IRIS). You can also use ModifyDatabaseFile and
DeleteDatabaseFile.

CreateNamespace

The name and properties of the namespace to be created in InterSystems IRIS. You can also use ModifyNamespace and DeleteNamespace.

ModifyNamespace

The name of the existing InterSystems IRIS namespace and its properties to be modified. You can also use CreateNamespace and DeleteNamespace.

CreateMapGlobal

The namespace to create the mapping in, the specification of the global to be mapped, and the database in which that global resides. You can also use ModifyMapGlobal and DeleteMapGlobal. In addition, you can use Create/Modify/DeleteMapRoutine and Create/Modify/DeleteMapPackage to create, modify, and delete routine and package mappings.

To illustrate the use of action parameters with database-related objects, suppose you wanted to:

- Create a database and a resource for it, then modify an existing namespace to make the database you created its global database and enable interoperability.

- Create a second database with resources, then create an interoperability-enabled namespace with the database as its default global database.

Deploy a Distributed Cache Cluster

The following example shows how you could do this with a merge file:

[Actions]

CreateDatabase:Name=APPA,Directory=/database-path/APPA,ResourceName=%DB_APPA
ModifyNamespace:Name=APPA,Globals=APPA,Interop=1

CreateDatabase:Name=APPB,Directory=/database-path/APPB,ResourceName=%DB_APPB
CreateNamespace:Name=APPB,Globals=APPB,Interop=1

Suppose that at a later point you wanted to add mappings of globals and routines in database APPA to namespace APPB.
You could do this with a merge file lik e the following:

[Actions]
CreateMapGlobal:Name="global-name(1):(101)",Namespace=APPB,Database=APPA
CreateMapRoutine:Namespace=APPB,Name=routine-spec,Database=APPA

For information about the operations performed by these action parameters and the values of their properties, see Create/Modify a Namespace, Create a Local Database, and Add Global, Routine, and Package Mapping to a Namespace.

### 5.3 Deploy a Distributed Cache Cluster

With a few simple changes to the merge file e xample in the previous section, you can create merge files to deplo y a distributed cache cluster.

For information about the operations performed by these action parameters in the following sections and the values of their properties, see Remote Databases and Deploying a Distributed Cache Cluster.

#### 5.3.1 Deploy the Data Server

The merge file belo w would be used to deploy the nonmirrored data server. In addition to creating the application databases
and their associated resources and namespaces, it does the following:

- Enables the ECP service with an action parameter.

- Uses an update parameter to set the maximum number of concurrent application server connections the data server can accept to 16.

Differences from the previous sample merge file are emphasized.

# nonmirrored data server merge file

[Config]

MaxServerConn=16

[Actions]

ModifyService:Name=%service_ecp,Enabled=1

CreateDatabase:Name=APPA,Directory=/database-path/APPA,ResourceName=%DB_APPA
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/database-path/APPB,ResourceName=%DB_APPB
CreateNamespace:Name=APPB,Globals=APPB

#### 5.3.2 Deploy the Application Servers

This merge file, which w ould be used to deploy all of the application servers, does the following:

- Adds the data server as a remote server with an update parameter

- Modifies the CreateDatabase actions above by adding the Server and LogicalOnly properties and updating the Directory argument to point to existing databases on the remote server, rather than a local directory in which to create a local database.

Differences from the sample merge file in the pre vious section are emphasized.

# app servers merge file

[ECPServers]

dataAB=dataserver-address,port,0

[Actions]

CreateDatabase:Name=APPA,Server=dataAB,Directory=/database-path-on-dataserver-dataAB/APPA,ResourceName=%DB_APPA,

LogicalOnly=1,

CreateNamespace:Name=APPDBA,Globals=APPA

CreateDatabase:Name=APPB,Server=dataAB,Directory=/database-path-on-dataserver-dataAB/APPB,ResourceName=%DB_APPB,

LogicalOnly=1
CreateNamespace:Name=APPB,Globals=APPB

#### 5.3.3 Deploy the Application Servers with Mirrored Data Server

If you are deploying an application server who’s data server is mirrored, the merge file must be altered. This merge file alters the application server merge file pre viously shown only by changing the 0 at the end of the remote server definition action in [ECPServers] to 1, as emphasized, to indicate that the remote server is a mirror, which allows application connections to transparently switch to the new primary after failover.

# app servers merge file

[ECPServers]

dataAB=dataserver-address,port,1

[Actions]

CreateDatabase:Name=APPA,Directory=/database-path-on-dataserver-dataAB/APPA,ResourceName=%DB_APPA,
Server=dataAB,LogicalOnly=1
CreateNamespace:Name=APPDBA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/database-path-on-dataserver-dataAB/APPB/,ResourceName=%DB_APPB,
Server=dataAB,LogicalOnly=1
CreateNamespace:Name=APPB,Globals=APPB

### 5.4 Mirror the Cluster’s Data Server

To deploy one or more InterSystems IRIS mirrors, you can use separate configuration mer ge files, each containing the ConfigMirror action parameter, for the different mirror roles, sequentially deploying the first f ailover member(s), then the second failover member(s), then DR async members, then any reporting async members if desired.

Deploy the Mirror Using Separate Merge Files

You can also deploy using a single merge file and hostname matching, which determines which member to deplo y on each of a set of hosts the names of which match the required pattern.

This section provides examples of each approach, see ConfigMirror for information on the available properties for the ConfigMirror action parameter.

For detailed information about mirror configuration, see Mirroring Architecture and Planning and Creating a Mirror. Be sure to read Mirroring with InterSystems IRIS Containers before planning containerized deployment of mirrors, or reconfiguring e xisting containerized instances into mirrors. Among other important considerations, you must ensure that the ISCAgent starts whenever the container for a failover or DR async mirror member starts.

### 5.5 Deploy the Mirror Using Separate Merge Files

In planning deployment using separate merge files it is important to bear in mind that the instance configured as the mirror primary must be running before other members can be added, so you must ensure that this instance is deployed and successfully started before other instances are deployed as the remaining members.

Deploy the Data Server Mirror Members

The following merge files deplo y the distributed cache cluster’s data server as a mirror with a DR async member by doing
the following:

- Including the ConfigMirror action parameter to create the mirror and add members.

- On the primary, adding the created databases to the mirror (they will be automatically added on the other members).

Differences from the corresponding merge file in the pre vious section are emphasized.

# mirrored data server primary merge file

[Config]
MaxServerConn=16

[Actions]

ModifyService:Name=%service_ecp,Enabled=1

ConfigMirror:Name=CLUSTERAB,SSLDir=ssl-directory-path,
Member=primary,Primary=localhost,ArbiterURL=address:port

CreateDatabase:Name=APPA,Directory=/ddatabase-path/APPA,ResourceName=%DB_APPA,

MirrorSetName=CLUSTERAB,MirrorDBName=APPA
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/ddatabase-path/APPB,ResourceName=%DB_APPB,

MirrorSetName=CLUSTERAB,MirrorDBName=APPB
CreateNamespace:Name=APPB,Globals=APPB

# mirrored data server merge file to add backup, DR async, read-only reporting async, or read-write
reporting async;
# for ConfigMirror Member argument enter either =backup, =drasync, =rorasync, or =rwrasync as appropriate

[Config]
MaxServerConn=16

[Actions]

ModifyService:Name=%service_ecp,Enabled=1

ConfigMirror:Name=CLUSTERAB,SSLDir=ssl-directory-path,
Member=backup|drasync|rorasync|rwrasync,Primary=primary-address:,ArbiterURL=address:port

CreateDatabase:Name=APPA,Directory=/ddatabase-path/APPA,ResourceName=%DB_APPA,

MirrorSetName=CLUSTERAB,MirrorDBName=APPA
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/ddatabase-path/APPB,ResourceName=%DB_APPB,

MirrorSetName=CLUSTERAB,MirrorDBName=APPB
CreateNamespace:Name=APPB,Globals=APPB

Note:

To add existing databases to the mirror created by the ConfigMirror action instead of creating empty ones, you could use the LogicalOnly parameter of the CreateDatabase action, where the Name and Directory parameters specify an existing database, this is shown in the modified e xcerpt from either section (primary or
backup/DR async) of the previous example:

Deploy the Mirror Using Hostname Matching

ConfigMirror:Name=CLUSTERAB,SSLDir=ssl-directory-path,
Member=backup|drasync,Primary=primary-address:,ArbiterURL=address:port

CreateDatabase:Name=APPA,Directory=/ddatabase-path/APPA,ResourceName=%DB_APPA,
MirrorSetName=CLUSTERAB,MirrorDBName=APPA,LogicalOnly=1
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/ddatabase-path/APPB,ResourceName=%DB_APPB,
MirrorSetName=CLUSTERAB,MirrorDBName=APPB,LogicalOnly=1
CreateNamespace:Name=APPB,Globals=APPB

To copy existing databases (to a new location before being added) to the mirror created by the ConfigMirror action instead of creating empty ones, you could use the Seed parameter of the CreateDatabase action to specify the path names of the databases to copy, as shown in this modified e xcerpt from either section (primary
or backup/DR async) of the previous example:

ConfigMirror:Name=CLUSTERAB,SSLDir=ssl-directory-path,
Member=backup|drasync,Primary=primary-address:,ArbiterURL=address:port

CreateDatabase:Name=APPA,Directory=/ddatabase-path/APPA,ResourceName=%DB_APPA,
MirrorSetName=CLUSTERAB,MirrorDBName=APPA,Seed=/mnt/databases/DB1
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/ddatabase-path/APPB,ResourceName=%DB_APPB,
MirrorSetName=CLUSTERAB,MirrorDBName=APPB,Seed=/mnt/databases/DB2
CreateNamespace:Name=APPB,Globals=APPB

### 5.6 Deploy the Mirror Using Hostname Matching

You can automatically deploy one or more mirrors from a single merge file if the deplo yment hosts have names ending in -number (or, as a regular expression, .*-[0-9]+$), for example iris-000, iris-001, iris-002 ..., or in -number-number, for example

- Setting the Map argument (not used with the separate merge file approach) to the pattern you w ant (it is primary,backup by default, but can also contain up to 14 DR async members as in primary,backup,drasync,...)

- Setting the Member and Primary arguments to auto.

For example, if you used the following ConfigMirror action parameter, mirror members would be deployed on appro-
priately named hosts as shown in the table after the example:

ConfigMirror:Name=AUTOMIRROR,SSLDir=ssl-directory-path,
Map=”primary,backup,drasync”, Member=auto,Primary=auto,ArbiterURL=address:port

Table 5–3: Mirror Deployment by Hostname

Single-number hostnames

Double-number hostnames

Mirror member role

mirror-000

mirror-001

mirror-002

mirror-003

mirror-004

mirror-005

mirror-0-0

mirror-0-1

mirror-0–2

mirror-1-0

mirror-1-1

mirror-1-2

primary

backup

DR async

primary

backup

DR async

To allow multiple independent InterSystems IRIS clusters to communicate without mirror member name collisions, you can offset the hostnames of one of the clusters by a number to prevent overlap using the optional Ordinal property. For example, if Ordinal is set to 100, then the corresponding hostnames are iris-100, iris-101, iris-102 ...

As another example, if you used the following ConfigMirror action parameter, mirror members would be deployed on
appropriately named hosts as shown in the table after the example:

ConfigMirror:Name=AUTOMIRROR,SSLDir=ssl-directory-path,
Map=”primary,backup,drasync”, Member=auto,Primary=auto,ArbiterURL=address:port

Ordinal=100

Table 5–4: Mirror Deployment by Hostname with Ordinal

Single-number hostnames

Double-number hostnames

Mirror member role

mirror-100

mirror-101

mirror-102

mirror-103

mirror-104

mirror-105

mirror-0-100

mirror-0-101

mirror-0–102

mirror-1-100

mirror-1-101

mirror-1-102

primary

backup

DR async

primary

backup

DR async

Deploy Mirror Members by Hostname

Incorporating a ConfigMirror action like the one above, you could use hostname matching to deploy a three-member mirrored data server using the following single merge file on three sequentially named hosts such as iris-001, iris-002, and iris-003 rather than three merge files as sho wn in the previous section.

# mirrored data server using single merge file and hostname mapping

See Also

[Config]
MaxServerConn=16

[Actions]

ModifyService:Name=%service_ecp,Enabled=1

ConfigMirror:Name=CLUSTERAB,SSLDir=ssl-directory-path,
Map=”primary,backup,drasync”,Member=auto, Primary=auto,ArbiterURL=address:port
CreateDatabase:Name=APPA,Directory=/ddatabase-path/APPA,ResourceName=%DB_APPA,
MirrorSetName=CLUSTERAB,MirrorDBName=APPA
CreateNamespace:Name=APPA,Globals=APPA

CreateDatabase:Name=APPB,Directory=/ddatabase-path/APPB,ResourceName=%DB_APPB,
MirrorSetName=CLUSTERAB,MirrorDBName=APPB
CreateNamespace:Name=APPB,Globals=APPB

### 5.7 See Also

- Configuration Mer ge in Deployment

- ge

- Best Practices for Configuration Merge This page describes some of the best practices related to using the configuration mer ge feature. For more information on the configuration mer ge feature, see Introduction to Configuration Mer ge.

Source control your merge files

InterSystems recommends keeping the merge files in volved in any application of the configuration mer ge feature under version control. Version control provides a record of all configuration changes, from deplo yment forward, over the life of an instance or a multi-instance topology. It also allows you to restore a previous configuration and easily share merge files with other users. You can also easily update your automated deployment or reconfiguration process, which uses configuration mer ge, by updating the merge files applied with the latest v ersion of the merge file. You could also require users to get the latest version of the appropriate merge file before deplo ying or reconfiguring an instance, e ven in the case of individual instances used for purposes such as development or testing. This would ensure all deployments and reconfigured instances ha ve identical configurations which match a central specification, re gardless of if it is a single instance or multiple instances.

Once you use configuration merge to deploy or reconfigure, use it for all configuration changes

If you use configuration mer ge, the strongly recommended best practice is to confine all configuration changes to this method — even when this means, for example, using iris merge to change just one or two parameters on one instance. If changes to the instance’s CPF are not made with configuration mer ge, assuming you version and store the merge files, the changes w on’t be source controlled, and a record of those changes will not exist. This poses a risk of configuration mer ge overwriting these changes made by other means, and with no record of the changes, they won’t be recovered. In the case of a single instance, for example, a lone development instance, this
risk may be acceptable; where a record of configuration changes to roll back to in the e vent of a problem is not
necessarily needed. However, in the case of many instances or in a production environment, this risk is not acceptable. Therefore, if you confine all configuration changes to configuration mer and risk of configuration mer ge overwriting changes made by other means.

ge, you can avoid the possibility

In a container, the potential of configuration mer ge overwriting changes made by other means is very great due to the continuous monitoring and merging of the merge file identified by the ISC_CPF_MERGE_FILE variable, as described in The iris merge Command. This allows you to use configuration mer ge and a central repository of merge files to apply further changes to e xisting instances simply by updating their merge files at an y time. However, if the configuration parameters included in the mer ge file ha ve been changed on the instance in the container by another method since deployment, the update merge can erase those changes, of which there may not be any record. Confining all configuration changes to configuration mer startup displays an error message and continues.)

ge avoids this. (If the merge file does not e xist,

Best Practices for Configuration Merge

How to avoid configuration overwrites in a container if not only using configuration merge

ge, you can avoid the possibility of configuration mer ge making If you do not confine changes to configuration mer unwanted changes by including in your automation (using, for example, the iris-main --after option) the scripting
of either or both of the following after instance startup:

- The deletion of the ISC_CPF_MERGE_FILE environment variable in each deployed container. (If the merge file does not e xist, startup displays an error message and continues.)

- The replacement of the merge file in each container with an empty file.
