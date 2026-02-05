# Server Migration Guide

Many possible scenarios exist where you want to take an existing instance of InterSystems IRIS® data platform and move it from one server to another. For example, if you want to move to a new server that is a similar or identical to the original server, you can use a full system restore.

Other scenarios can be more challenging, such as when the existing server is running an operating system that is no longer supported and you need to move the instance to a new server running a different operating system. This document provides some guidelines that will help you migrate your instance and its data to a new server. Moving data or code contained in an InterSystems IRIS database is straightforward, but you must also consider items that need to be moved over manually.

This document is intended to be used for migrating an instance of InterSystems IRIS to a new server running the same version of InterSystems IRIS. For other types of migration, see Notes on Migrating to a Newer Version of InterSystems
IRIS.

Important:

The server migration process has changed substantially in InterSystems IRIS 2025.2 and later due to the new security database. (See the release notes for details.) If you are using an earlier version of InterSystems IRIS, see the server migration documentation for that version.

Important:

As a system administrator you should review this document, decide which items are applicable to your system and whether items not on the list must also be migrated.

All InterSystems IRIS installations are unique. This document covers the topics InterSystems believes to be the most common, however, it cannot cover all possible scenarios. If you need assistance in determining the best course of action to take, contact the InterSystems Worldwide Response Center.

InterSystems recommends that customers have a document that outlines how to completely rebuild their instances. If you do not have such a document, a migration event is a good time to create such a document.

Important:

If you are migrating to an operating system that does not support your current version of InterSystems IRIS, you should first perform an upgrade to a supported v ersion of InterSystems IRIS. (See Upgrade an Instance.) After fully testing this upgrade, perform the migration to the new operating system.

Note:

This document is intended to be used for InterSystems IRIS migrations only. While the general principles apply to other InterSystems products, those products may require unique procedures that are beyond the scope of this document.

This document:

- Describes the high-level steps needed to set up a new server prior to performing the migration.

- Alerts you to some special considerations pertaining to migration to a different operating system.

- Provides guidelines on migrating the types of items listed below:

–

–

InterSystems IRIS license key

Encryption key files

– Configuration P arameter File

– Databases

– Namespace interoperability settings

–

Task Manager tasks

Before Performing the Migration

– Custom code in %SYS namespace

– CSP, JS, and CSS files

–

External linked libraries and custom shared libraries

- Describes how to migrate mirror members.

- Provides some notes on migrating to a later version of InterSystems IRIS.

## 1 Before Performing the Migration

### 1.1 Provision the Target Server

Unless you are purposely downsizing your server, make sure that the target server equals or exceeds the source server in
terms of:

- CPU

- Memory

- Disk space For more information on sizing a server, see System Resource Planning and Management.

### 1.2 Perform the Initial Installation

After procuring the target server, perform the initial installation of the operating system and InterSystems IRIS on the target
server:

1.

Install the operating system.

2. Perform the following:

- Make sure necessary users at the operating system-level are configured.

- Make sure large or huge pages are configured.

- Make sure swap space or page file configurations are consistent with those on the source serv er.

- Make sure all drives or file systems are a vailable with the same names and permissions.

- Make sure the new machine has the same IP address, or if it has a new IP address then consider if other systems need to allow the new IP address through their fire walls.

3.

Install the same version of InterSystems IRIS as on the source server.

For the smoothest migration, make sure that the following installation options are the same as on the source server:

- Instance name

- Installation directory

Note:

If you do change the installation directory, note that you may have to update any directory path names in the CPF when you perform the migration.

- Setup type (for example, Development, Server, or Custom) Notes on Migrating from One Operating System to Another

- Character width (8-bit or Unicode)

- Port numbers

Note:

If the port numbers on the target server do not match those on the source server, you may have to update the port numbers in the CPF when you perform the migration.

- Security Setting (Minimal, Normal, or Locked Down) For more information, see Installation Planning Considerations.

4.

Install the web server and configure the web serv er and the web gateway (if required). For more information, see the Web Gateway Guide.

5.

Install any necessary security certificates.

6. Configure an y needed fire wall settings.

## 2 Notes on Migrating from One Operating System to Another

If you are migrating from one operating system to another, for example, from Windows to Linux, some files and settings may not be directly compatible. For example, you may need to hand-edit your configuration parameter file (CPF) or e settings files before migrating them to the tar get server.

xported

Before you begin the migration process, make a backup copy of the original configuration parameter file, on the target server, in case you need to refer to it later.

/<installdir>/iris.cpf,

Items you may need to edit include, but are not limited to the following:

- Any directory path names in the CPF, the exported Applications settings, and the exported SSL Configurations settings

- The overview parameter in the [Config] section of the CPF See the original CPF and exported settings files on the tar get server for guidance.

If you are migrating to an operating system that has a different Endianness (big-endian versus little-endian), you must first convert the byte order of any databases using the cvendian utility. See Using cvendian for Byte Order Conversion for details.

Important:

If you did not purchase a platform-independent license, contact your account team to obtain a license for the new platform before performing the migration.

## 3 Perform the Migration

### 3.1 Preparation Steps

Before you begin the migration, perform the following steps:

1. Make a copy of the original CPF file ( /<installdir>/iris.cpf) on the target server in case you need to refer to it during the

migration process.

2.

If database encryption is turned on for the IRISSECURITY database on the source instance, turn off encryption for this database by going to System Administration > Encryption > Database Encryption > Configure Startup Settings. Then restart the instance. You can turn encryption back on for the IRISSECURITY database after performing the migration.

Other databases can remain encrypted during migration.

3. Perform a clean shutdown of the instances on both servers. Do not restart the instances until instructed.

### 3.2 InterSystems IRIS License Key

Copy the iris.key file from the

/<installdir>/mgr/ directory on the source server to the same directory on the target server.

### 3.3 Encryption Key Files

If you are using standard key files for managed key encryption, copy any needed key files from the source serv er to the same directories on the target server.

Important:

If you are using other methods of key management, contact the InterSystems Worldwide Response Center for assistance.

### 3.4 Configuration Parameter File (CPF)

Copy the iris.cpf file from the

/<installdir>/ directory on the source server to the same directory on the target server.

Important:

If your source server had any directories or port numbers that differ from the target server, you will need to edit your CPF file such that the directories and port numbers match that of the original tar get CPF file you saved before beginning the migration.

If the target server is running on a different operating system from the source server, see Notes on Migrating from One Operating System to Another.

### 3.5 Databases

#### 3.5.1 Decide Which Databases to Migrate

In general, it is easy to migrate a database from the source server to the target server simply by copying it, but not all databases can or should be migrated.

User-Created Databases

Any user-created databases that you want to retain on the target server should be migrated.

IRISSECURITY

Starting with InterSystems IRIS 2025.2, security settings are stored in the IRISSECURITY database. This database should be migrated to the target server.

Security records in this database include:

Applications

Documentation databases

Events

KMIP servers

LDAP configurations

- OAuth2 configurations

- Open AIM identity services

- Phone providers

- PKI configurations

- Resources

- Roles

- Services

- SQL privileges

- SSL configurations

- System

- Users

- X509 credentials

- X509 users

- IRISSYS

- The IRISSYS database, located in the /<installdir>/mgr directory, cannot be migrated by copying it. Any data needed from the source IRISSYS database, such as tasks, can be exported and then imported into the destination IRISSYS database. See the remainder of this document for details.

- IRISMETRICS

- The IRISMETRICS database can be migrated by copying it, if that is necessary for business reasons.

- Other System-Supplied Databases Other system-supplied databases should not be migrated, as fresh copies are provided by the installer. These databases
include:

- ENSLIB

- IRISAUDIT

- IRISLIB

- IRISLOCALDATA

- IRISTEMP If you have placed custom code in the ENSLIB database, InterSystems recommends evaluating and implementing alternative solutions before performing the migration.

#### 3.5.2 Migrate the Databases

Copy the IRIS.DAT files to be migrated, along with their enclosing directories to the same locations on the tar get server.

Note:

If you see any iris.lck files with the running or did not shutdown cleanly. Shut down the instance cleanly and try again.

iris.dat files on the source serv er, the source instance of InterSystems IRIS is

Start the instance on the target server, and it will start up using the new license key, encryption key files, CPF , and databases.

Note:

If InterSystems IRIS cannot mount a database upon startup, you will see the following message:

Database <db_name> is required, but could not be mounted Shutting down the system

Frequently, this error means one of the following:

- You did not copy the database to the location you intended to copy it.

- Make sure that the database is located in the correct directory, and then start InterSystems IRIS again.

- You installed InterSystems IRIS into a different directory than on the source server.

Edit the CPF and change all directory names to indicate the new installation directory, and then start InterSystems IRIS again..

The file or directory permissions are not set correctly for the InterSystems IRIS o wner and users.

Adjust the permissions and then start InterSystems IRIS again.

Note:

If you see a message similar to the following upon startup, it means an iris.lck file w as present when you copied
over the database:

Database <db_name> is locked from <instance_name> Cannot remove database lock <file_name>

This usually means that the source instance of InterSystems IRIS is running or did not shutdown cleanly. Shut down the instance cleanly and try again.

Note:

If encryption is turned on for the IRISSECURITY database, startup will fail with the messages in messages.log
similar to the following:

## 0 [Utility.Event] Decrypting IRISSECURITY database <key ID> is not activated.
## 3 [Utility.Event] Error: ERROR #5002: ObjectScript error: <ILLEGAL VALUE>MakeIRISSecurity+57^%SYS.DATABASE - Shutting down the system

In such a case, perform the following steps:

1. Start the instance on the source server.

2. Turn off encryption for the IRISSECURITY database in the Management Portal by going to System Adminis-

tration > Encryption > Database Encryption > Configure Startup Settings.

3. Restart the instance and verify that encryption for the IRISSECURITY database is turned off.

4. Perform a clean shutdown of the instance.

5. Copy the new version of the IRISSECURITY database to the correct folder on the target server.

6. Restart the instance on the target server and verify that it starts normally.

#### 3.5.3 Turn on Encryption for the IRISSECURITY Database (Optional)

If you turned off encryption for the IRISSECURITY database prior to the migration, you can turn it back on now, by going to System Administration > Encryption > Database Encryption > Configure Startup Settings.

### 3.6 Namespace Interoperability Settings

If you are using interoperability productions in a namespace, you must enable the namespace to use productions on the target server, as this setting does not come over in either the CPF or the databases associated with the namespace.

Run the following command for each namespace to be interoperability enabled:

do ##class(%Library.EnsembleMgr).EnableNamespace("<namespace>",1)

As an alternative, you could reconfigure the namespaces in a single operation using the configuration mer ge feature. To do this, execute the iris merge command with a merge file lik e the following, containing an entry for each namespace you
want to be interoperability enabled:

[Actions]
ModifyNamespace:Name=NamespaceA,Interop=1
ModifyNamespace:Name=NamespaceB,Interop=1
ModifyNamespace:Name=NamespaceC,Interop=1
. . .

### 3.7 Task Manager Tasks

Export any Task Manager tasks you want to migrate by exporting individual tasks from within the Task Manager or by passing a list of tasks to the %SYS.Task.ExportTasks() method.

To use the Task Manager to export a task:

1.

In the Management Portal, select System Operations > Task Manager > Task Schedule.

2. On the Task Schedule page, click the name of the task you want to export.

3. On the Task Details screen, click Export.

4. On the Export screen, enter a path and file name, and click Perform Action Now.

Note:

By default, Task Manager exports a task to the file

/<installdir>/mgr/Temp/ExportTask.xml.

You can also use the Task Schedule page to identify the IDs of the tasks you want to export. Then set a variable to the list of task IDs and call %SYS.Task.ExportTasks() to export the desired tasks to an XML file.

For example, from any namespace:

set tasklist = $lb(1, 1000, 1001)
set status = ##class(%SYS.Task).ExportTasks(tasklist, "Tasks.xml")

Note: %SYS.Task.ExportTasks() exports tasks to an XML file with the specified name in the directory of the Def

ault

Database for Globals for the namespace where you ran the command.

Copy the exported XML files to the tar get server and then import them using the Task Manager:

1.

In the Management Portal, select System Operations > Task Manager > Import Tasks.

2. On the Import screen, enter a path and file name, and click Perform Action Now.

Note:

By default, Task Manager imports tasks from the directory /<installdir>/mgr.

If you are importing a System task, Task Manager will create a new task, rather than overriding an existing task. The new task will have the next available ID greater or equal to 1000. If desired, delete or suspend the existing task from the Task Manager.

When you are done importing your tasks, you need to configure your Task Manager email settings on the target server, as these do not come over in the Task Manager export. You can do this in the Management Portal by going to System Administration > Configuration > Additional Settings > Task Manager Email. Copy and paste each field from the same screen on the source server.

### 3.8 Custom Items in %SYS Namespace

Export any custom classes, routines, or globals from the %SYS namespace of the source server and import them to the %SYS namespace on the target server.

For example, migrate the following routines if you are using them:

- ^ZWELCOME

- ^ZAUTHENTICATE and ^ZAUTHORIZE

- ^ZMIRROR

- ^%ZSTART and ^%ZSTOP

- ^%ZLANG*

- ^%ZJREAD

### 3.9 CSP, JS, and CSS Files

Copy all files and directories for an y custom CSP applications from the source server to the same locations on the target server.

### 3.10 External Linked Libraries and Custom Shared Libraries

If you are using any external linked libraries or custom shared libraries, copy these from the source server to the target server.

This procedure is site specific and instructions are not pro vided in this document.

## 4 Migrate Mirror Members

If you are using InterSystems IRIS mirroring, you can use migration to assist you in:

- Creating a New Mirror Member

- Moving to a Mirror to New Servers For an in-depth discussion of mirroring, see Mirroring.

### 4.1 Use Migration to Assist in Creating a New Mirror Member

If you have an existing mirror, you can use migration to set up a new server to be used as a new failover member or async member. Simply migrate an existing failover member to a new server, and then join the target server to the mirror.

Prepare the target server as described in this document, with the following differences.

- Delete the [Mirrors] and [MapMirrors] sections from the CPF before migrating it to the new server.

- Revert the [MirrorMember] section of the CPF to its default before migrating it to the new server. You can copy this section from the freshly installed CPF on the target server.

Note:

This prevents the new instance from trying to use the same Agent Address as the old instance.

Then on the new InterSystems IRIS instance, perform the following:

1. Start the ISCAgent. (See Starting and Stopping the ISCAgent.)

2.

In the Management Portal, select System Administration > Configuration > Mirror Settings > Enable Mirror Service.

3. On the Edit Service window, select Service Enabled, and then click Save.

4. Under Mirror Settings, select Join as Failover or Join as Async, depending on which type of mirror member you would

like to add.

Note:

If you don’t see the Join as Failover or Join as Async menu options, but instead see the Edit Mirror option, it indicates that some mirror configuration information remained in the CPF before it w as migrated. You will
need to remove the existing mirror configuration, as follo ws:

a. Select Edit Mirror.

b. Click Remove Mirror Configuration.

c. On the Remove Mirror Configuration screen, click Remove. Do not remove the mirrored attribute from

the mirrored databases.

d. Restart InterSystems IRIS and resume with Step 4.

5. On the Join Mirror screen, fill in the appropriate information for the e xisting mirror, and then click Next.

6. After the system retrieves information from the mirror, confirm the Member Information is correct.

7.

If you are adding an async member, select the desired Async Member System Type.

8. Click Save.

9. Select System Operation > Mirror Monitor.

10. On the Mirror Monitor screen, under Mirrorred Databases, Activate each mirrored database.

11. Then, Catchup each mirrored database.

### 4.2 Use Migration to Assist in Moving to a Mirror to New Servers

Migration can also assist you in moving an existing mirror to new servers.

For example, you might have a mirrored configuration, on operating system X, where Serv er A is the primary failover member and Server B is the backup failover member. Your goal is to migrate to a configuration on operating system Y, where Server C is the primary failover member and Server D is the backup failover member.

The procedure for performing this move is summarized in the table below:

Notes on Migrating to a Newer Version of InterSystems IRIS

Table 1: Moving a Mirror to New Servers

Step

Server A

Server B

Server C

Server D

Perform migration to Server C and Server D, and add as DR async members (See Use Migration to Assist in Creating a New Mirror
Member).

Promote C to failover member, making C the backup and demoting B to DR async (See Promoting a DR Async Member to
Failover Member)

Failover from A to C, making A the backup and C the primary (See Planned Failover to a Promoted DR Async)

Promote D to failover member, making D the backup and demoting A to DR async (See Promoting a DR Async Member to
Failover Member)

Remove A and B from mirror (See Editing or Removing an Async Member )

Primary

Backup

Primary

Backup

Backup

Primary

Primary

Backup

Disconnected

Disconnected

Primary

Backup

## 5 Notes on Migrating to a Newer Version of InterSystems IRIS

There are times when you may want to perform a migration to a server running a newer version of InterSystems IRIS, for example, when evaluating how your application runs on the newer version of InterSystems IRIS. Some additional steps may be required for this type of migration, however, the details are beyond the scope of this document. If possible, perform a standard upgrade, instead of migrating to a newer version of InterSystems IRIS.

For information on migrating from Caché or Ensemble to InterSystems IRIS, see How to Migrate to InterSystems IRIS, available on the WRC Document Distributions page (login required).
