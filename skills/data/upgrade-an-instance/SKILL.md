# Upgrade an Instance

Pre-Upgrade Steps

This topic is intended for customers who are upgrading from an earlier version of InterSystems IRIS®, InterSystems IRIS for Health™, or HealthShare® HealthConnect. Customers looking to migrate from InterSystems Caché® should see Why Migrate to InterSystems IRIS?

Note:

Health Connect 2019.1 was the first release of Health Connect that is po wered by InterSystems IRIS. Because of this change in underlying technology, a special upgrade procedure is required when upgrading from a previous version of Health Connect. If you are upgrading to Health Connect 2019.1 or later from Health Connect 15.03, see the InterSystems IRIS Migration Guide, which is available from the InterSystems WRC Documents page.

Important:

InterSystems recommends that each application be thoroughly tested in the upgraded environment before it is deployed to customers and begins processing live data.

Note:

If you are upgrading to a maintenance release, some tasks are marked as optional. However, performing all tasks will ensure optimum performance.

### 1.1 Step 1: Review Incompatibilities

Review the following documents and prepare to address any incompatibilities:

- InterSystems Upgrade Impact Checklist (or the Incompatibility History) — a list of incompatibilities between versions that may affect your release.

- Special Considerations When Upgrading — a list of considerations particular to upgrading this specific v ersion.

- InterSystems Supported Platforms — the supported platforms for this version. Your technologies should be checked against this to determine if they are still supported.

### 1.2 Step 2: Confirm Source Code Availability

After a major upgrade, you must recompile all class code under the new version or else provide class code that has already been compiled under the new version. Otherwise, you will not be able to run your application after the upgrade. It is recommended that you recompile any routine code.

Pre-Upgrade Steps

Check that you have the code for any classes running in deployed mode (which you can place under deployed mode again when the upgrade is complete), as well as the code for custom routines not generated from classes (*.mac or *.int).

### 1.3 Step 3: Save Custom Classes, Routines, and Globals

On an upgrade, the IRISSYS database is modified. To prevent your own classes, routines and globals in the %SYS namespace from being affected by the upgrade installation, ensure that they have names that begin with Z, z, %Z, or %z. All .int and .obj routines (except for Z*, z*, %Z*, and %z*) are deleted from the %SYS namespace when upgrading.

Similarly, on an upgrade, the IRISLIB, IRISTEMP, and ENSLIB databases are completely replaced.

### 1.4 Step 3.5: Mirror the HSSYS Database

Required Only for InterSystems IRIS for Health and HealthShare Health Connect Upgrades

The HSSYS database must be mirrored.

### 1.5 Step 4: Save User Files

To ensure that your user files are not deleted or replaced during the upgrade, sa ve them in the install-dir\mgr\User directory, which is the only directory that is not subject to modification during an upgrade.

### 1.6 Step 5: Examine Huge/Large Page Allocations

On Linux and AIX® systems, the huge/large page allocation must be greater than the shared memory allocation; otherwise,
your system will not use huge/large pages which can cause performance issues.

If your current huge/large pages allocation is exactly equal to your system’s shared memory allocation, you should reallocate huge/large pages before upgrading, adding several additional MB, to account for any upward change in shared memory allocation between versions. For details, see Configuring Huge and Lar ge Pages.

### 1.7 Step 6 (Optional): Create an Installation Manifest

Optional for All Releases

A manifest is useful for silent installs, as you can invoke the post-upgrade tasks to run as soon as the upgrade is complete, eliminating the need for interactive steps. See Creating and Using an Installation Manifest for more information.

Step 7: Precompile User Code That Runs on Startup

### 1.8 Step 7: Precompile User Code That Runs on Startup

If your application calls any user code at instance startup (using %ZSTART, ZAUTHENTICATE, or other means), you must precompile it on an instance of the new version and use an installation manifest to install it as part of the upgrade process. If you do not, the instance will fail to start up.

### 1.9 Step 8: Check System Integrity

Run a system integrity check on existing directories to ensure there is no corruption in any of the databases. For more information, see Introduction to Data Integrity.

### 1.10 Step 9: Back up the System

Before upgrading, InterSystems recommends that you run a complete backup of your system using your customary full operating system backup procedures. If the upgrade is not successful, you may need to restore from this backup. For information about backups, see Backup and Restore.

### 1.11 Step 10: Stop Productions and Disable Auto-Start

If your system is running any productions, follow the instructions in Stopping a Production and disable auto-start so that you can recompile code before starting productions up again.

Upgrade an Instance on Windows

### 2.1 Perform Attended Upgrade

The following steps outline how to perform an attended upgrade of your instance on a Windows system. Before beginning, make sure you have followed any pre-upgrade steps. If you are upgrading a mirrored system or ECP configurations , review the respective documentation. You can also perform an unattended installation using the command line.

### 2.2 Step 1: Confirm Prerequisites

Confirm that you ha ve completed all necessary pre-upgrade steps.

If you are upgrading a mirrored system, review Upgrading a Mirror for specific details on upgrading mirrored systems.

If you are upgrading an ECP configuration, re view Upgrading ECP Configurations for specific details on upgrading ECP configurations.

If you are using a manifest as part of your upgrade process, see the instructions in Creating and Using an Installation Manifest before performing the standard installation steps.

### 2.3 Step 2: Shut Down the Instance

Prior to beginning an upgrade of an instance, it is essential that the instance be shut down cleanly. To verify that the shutdown was clean, examine the messages.log file after the shutdo wn finishes. If the log contains entries similar to the follo wing,
then the shutdown was clean:

... 05/03/19-14:24:13:234 (5204) 0 Journal restore not required at next startup 05/03/19-14:24:13:234 (5204) 0 Transaction rollback not required at next startup ...

If these entries are not present, the instance did not shut down cleanly. Please contact the InterSystems Worldwide Response Center before proceeding with the upgrade.

Upgrade an Instance on Windows

### 2.4 Step 3: Begin Installation

Double-click the installer file, for e xample, IRIS-win_x64.exe. The installer displays a list of all existing instances on the host. Select the name of the instance you want to upgrade and click OK.

### 2.5 Step 4: Configure Web Server

Only if a web server is not already configur ed

If you have not already configured a web serv er for you instance, you can configure one during the upgrade process. To do so, follow the instructions below. If you have already configured a web serv er, you will not be prompted to configure one when upgrading.

If a local Microsoft Internet Information Services (IIS) web server is detected, the Local Web Server dialog box lets you select whether or not the installer should automatically configure the web serv er for this instance. If you choose to not have the installer configure your web serv er automatically, you will have to configure it manually after the installation finishes. If a local web server is not detected, the dialog box instead asks if you want to Abort the installation or Continue the installation without Web Gateway. If you choose to continue anyway, you will have to configure the web serv er manually after the installation finishes.

Important:

InterSystems recommends using the Microsoft IIS web server because it can be automatically configured during the upgrade process. Make sure it is installed and running before beginning the upgrade process. In most cases, it is not necessary to manually configure the IIS web serv er.

### 2.6 Step 5: Add or Remove Components (Optional)

You can add or remove components during the upgrade process. To do so, select the Customize button, then follow the instructions on selecting components from the custom install guide. Once you have chosen which components you would like to add or remove, click Save and proceed with the upgrade.

### 2.7 Step 6: Run the Upgrade

After you’ve selected all upgrade options, click Upgrade. The system runs the upgrade process. After the upgrade is completed, click Finish.

Important:

Do not interrupt the installation while it is in progress. If the upgrade fails with any error messages, correct the issues and restart the upgrade installation.

Step 7: Examine Logs for Errors

### 2.8 Step 7: Examine Logs for Errors

Examine messages.log, iboot.log, and ensinstall.log in the install-dir/mgr directory for any errors. If any fatal error is found, correct the error, and then run the installer again.

Examine messages.log, iboot.log, ensinstall.log, and most recent HS.Util.Installer.<namespace>-<number>.log files in the install-dir/mgr directory for any errors. If any fatal error is found, correct the error, and then run the installer again.

If your operating system is configured to use lar ge memory pages, check the startup messages to make sure shared memory is being allocated in accordance with these settings. If you see a message similar to the following, reboot your server to avoid an out-of-memory situation.

Failed to allocate 592MB shared memory using large pages. Switching to small pages.

### 2.9 Unattended Upgrade or Reinstall

In addition to installing a new instance, the installer can be called on an existing installed instance. To do so, you must use the /instance flag to specify the name of the tar get existing instance. The action the installer takes depends on the version
of the installation file compared to the v ersion of the instance, as follows:

- If the installation file is the same v ersion as the target installed instance, the installer reinstalls (repairs) the instance.

- If the installation file is a later v ersion than the target installed instance, the installer upgrades the instance to the new version.

For example, to run an unattended upgrade of an installed instance IRISB that is an earlier version than the installation file,
use the following:

C:\downloads\IRIS-2019.1.0.516.0-win_x64.exe /instance IRISB /qn

You can reinstall one or more specific features, as listed in the Custom-Installable Features Reference, by specifying the target instance and using the REINSTALL property (see the Command-Line Properties Reference). For example, to reinstall Studio for the installed instance IRISB, you can use the following command (assuming the installation file and
the same version):

IRISB are

C:\downloads\IRIS-2018.1.0.508.0-win_x64.exe /instance IRISB /qn REINSTALL=studio

Upgrade an Instance on UNIX®, Linux, or macOS

### 3.1 Step 1: Confirm Prerequisites

Confirm that you ha ve completed all necessary pre-upgrade steps.

If you are upgrading a mirrored system, review Upgrading a Mirror for specific details on upgrading mirrored systems.

If you are upgrading an ECP configuration, re view Upgrading ECP Configurations for specific details on upgrading ECP configurations.

If you are using a manifest as part of your upgrade process, see the instructions in Creating and Using an Installation Manifest before performing the standard installation steps.

Note:

If the profile of the user e xecuting irisinstall has a value set for the CDPATH variable, the upgrade fails.

### 3.2 Step 2: Shut Down the Instance

Prior to beginning an upgrade of an instance, it is essential that the instance be shut down cleanly. To verify that the shutdown was clean, examine the messages.log file after the shutdo wn finishes. If the log contains entries similar to the follo wing,
then the shutdown was clean:

... 05/03/19-14:24:13:234 (5204) 0 Journal restore not required at next startup 05/03/19-14:24:13:234 (5204) 0 Transaction rollback not required at next startup ...

If these entries are not present, the instance did not shut down cleanly. Please contact the InterSystems Worldwide Response Center before proceeding with the upgrade.

Upgrade an Instance on UNIX®, Linux, or macOS

### 3.3 Step 3: Begin Upgrade

If your installation kit is in the form of a .tar file, you must first
installation procedure by running the irisinstall script, located at the top level of the installation files:

uncompress it. As a user with root privileges, start the

# sudo sh /<pathname>/irisinstall

where <pathname> is the location of the installation kit, typically the temporary directory to which you have extracted the kit.

The script displays a list of all existing instances on the host. You are prompted with:

Enter instance name:

Type the name of the instance you want to upgrade. If you do not type the name of an existing instance, you will begin an installation using the new kit instead of an upgrade. To confirm that you are upgrading an e xisting instance make sure you
are prompted with:

Do you want to update InterSystems IRIS instance 'IRIS' <Yes>?

and not:

Do you want to create InterSystems IRIS instance 'IRIS' <Yes>?

### 3.4 Step 4: Choose Installation Type

You are prompted to choose which installation type to perform:

Select installation type. 1) Development - Install InterSystems IRIS server and all language bindings 2) Server only - Install InterSystems IRIS server 3) Custom Setup type <1>?

Upgrades using the Development or Server only installation types have fewer options when performing the upgrade. The Custom installation type provides additional upgrade options.

### 3.5 Step 5: Modify Group to Start or Stop the Instance

You are prompted to change the group that is allowed to start and stop the instance:

What group should be allowed to start and stop this instance <existinggroup>?

where <existinggroup> is the group currently configured to start and stop the instance.

If you would like to change the group, enter the name or group ID number of an existing group; the installer will verify
that the group exists before proceeding.

For more details, see Determining Owners and Groups.

Step 6: Configure Effective Group

### 3.6 Step 6: Configure Effective Group

Custom installation type only

You are prompted to configure the effective group for InterSystems IRIS processes:

What is the effective group for InterSystems IRIS processes <exisitinggroup>?

where <existinggroup> is the currently configured ef fective group for InterSystems IRIS processes. This is the Inter- Systems IRIS internal effective group ID, which also has all privileges to all files and e xecutables in the installation. For maximum security, no actual users should belong to this group.

If you would like to change the group, enter the name or group ID number of an existing group; the installer will verify
that the group exists before proceeding.

For details, see Determining Owners and Groups.

### 3.7 Step 7: Configure Web Server

If a local web server is detected, you are prompted if you would like to use the web server to connect to your installation:

Local web server detected. Would you like to use the web server to connect to this installation <Yes>?

If you enter y, the installer configures your web serv er to serve requests to your instance. If the web server was already configured, then no action is tak en. When performing a custom installation, the installer prompts you to provide additional configuration information including the location of the httpd.conf file and the Apache httpd port number.

If you enter n, the web server will not be connected automatically. If a web server was already connected, it will not be disconnected. However, if a web server was not connected, you will have to configure it manually after the installation finishes.

If a web server is not detected, you are prompted if you would like to abort:

No local web server found. Would you like to abort the installation <Yes>?

If you choose to continue the installation, you will have to configure your web serv er manually after the installation finishes.

Important:

InterSystems recommends using the Apache httpd web server because it can be automatically configured during the installation or upgrade process. Make sure it is installed and running in the default installation location before beginning the upgrade process. In most cases, it is not necessary to manually configure the Apache web server.

### 3.8 Step 8: Activate License Key

If a license key is detected in the <install-dir>/mgr/ directory, then this step is skipped.

If a license key is not detected, you are prompted to enter a license key:

InterSystems IRIS did not detect a license key file

Do you want to enter a license key <No>?

Upgrade an Instance on UNIX®, Linux, or macOS

If you input y, you are prompted to input the filepath:

License key file:

Input a path to the iris.key file to automatically acti vate the key; it is copied to the instance’s /mgr/ directory. If you do not
specify a license key, you can activate a license key following installation. See Activating a License Key for information about licenses, license keys, and activation.

### 3.9 Step 9: Run the Upgrade

The installation script summarizes the upgrade options and again asks you to confirm the upgrade:

Please review the installation options:
--------------------------------------- ... <installation options> ... ---------------------------------------

Confirm InterSystems IRIS upgrade <Yes>?

Input y to continue with the upgrade.

Important:

Do not interrupt the installation while it is in progress. If the upgrade fails with any error messages, correct the issues and restart the upgrade installation.

After the upgrade finishes, the instance restarts and an y installation manifest is run.

### 3.10 Step 10: Examine Logs for Errors

Examine messages.log, iboot.log, and ensinstall.log in the install-dir/mgr directory for any errors. If any fatal error is found, correct the error, and then run the installation script again.

Examine messages.log, iboot.log, ensinstall.log, and most recent HS.Util.Installer.<namespace>-<number>.log files in the install-dir/mgr directory for any errors. If any fatal error is found, correct the error, and then run the installation script again.

If your operating system is configured to use huge memory pages, check the startup messages to mak e sure shared memory is being allocated in accordance with these settings. If you see a message similar to the following, reallocate huge pages to be greater than the shared memory allocation, then reboot your server to avoid an out-of-memory situation.

Failed to allocate 1468MB shared memory using Huge Pages. Startup will retry with standard pages.

Uninstall or Reinstall an Instance

### 4.1 Uninstall or Reinstall on Windows

By running setup and selecting an instance of the same version as the installer, or by selecting Programs and Features from Windows Control Panel and selecting an instance, you can make changes to or uninstall the instance.

When you run setup as described in Windows Attended Installation and select an instance of the same version as the installer in the Select Instance box, or select an instance in Programs and Features and use the Change or Repair buttons, the Updating Instance instancename dialog box displays.

Note: When you select the Uninstall button in Programs and Features, the uninstall operation begins immediately.

Click Next to display the Modify, repair or remove the program dialog box, then select the appropriate option on this dialog to change, repair, or uninstall the instance.

- Select Modify to display the Custom Setup dialog box described in Windows Custom Installation. Using this dialog box, you can select the component groups or components you want to add or remove. Components are described in the Components Installed by Setup Type table.

- Select Repair to repair problems with the instance such as missing or corrupt files or re gistry entries.

- Select Remove to uninstall the instance.

Important:

Use only the InterSystems installer or Windows Control Panel Programs and Features to uninstall an instance. Other uninstall programs are not supported and using them may cause unexpected results.

### 4.2 Unattended Removal on Windows

To launch an unattended removal, specify the instance to uninstall and the REMOVE=ALL property, as follows:

<path>\<installer>.exe /instance <instancename> /q[b|n] REMOVE=ALL

You can also use the REMOVE property to remove specific features, as described in the Custom-Installable Features
Reference. For example, to remove the Apache 2.0 Web Gateway from instance IrisC, use the command:

C:\downloads\IRIS-2018.1.0.508.0-win_x64.exe /instance IrisC /qn REMOVE=cspgateway,cspapache20

Uninstall or Reinstall an Instance

#### 4.2.1 Special Consideration

If you do not have access to the original installation package, you can run uninstall in unattended mode by using the Win-
dows® Installer command-line application (msiexec) and information in the Registry, as follows:

msiexec /x {<product_guid>} /qn /l <logfile>

where <product_guid> is the ProductCode property value of the version you installed.

You can obtain the ProductCode property value from the following Registry location:

Processor Type

Registry Location

32–bit

64–bit

HKEY_LOCAL_MACHINE\SOFTWARE\Intersystems\IRIS\Configurations\<instance>

HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Intersystems\IRIS\Configurations\<instance>

where <instance> is the name of the instance you want to uninstall in unattended mode. The ProductCode property value
is displayed in a row similar to:

ProductCode REG_SZ {80E3F658-2D74-4A81-92AD-FD16CD226154}

You can also use any of the properties in the Command-Line Properties Reference with msiexec. For information about msiexec, see the Microsoft msiexec (command-line options) TechNet article (https://docs.microsoft.com/en-us/previousversions/windows/it-pro/windows-server-2003/cc759262(v=ws.10)).

### 4.3 Uninstall on UNIX®, Linux, and macOS

To safely uninstall an instance, follow this procedure:

1. Find the name of the instance you wish to delete using the iris list command to list all the instances on your machine:

iris list

2. Verify the instance is stopped. If it is not, stop it with the iris stop command:

iris stop <instname>

Where instname is the instance name that you chose during the installation. If it hangs, force it down using iris force:

iris force <instname>

3. Remove the instance using the iris delete command:

iris delete <instname>

4. Remove the installation directory using the following operating system command:

rm -r <directory>

Important:

Be aware that this removes files you may wish to k eep. For example: the license key (iris.key), the configuration file

(iris.cpf), and the user database file (iris.dat).

The uninstall procedure removes all files installed and created during normal processing, including journal and temporary database files.

Important:

The SUSE Linux Enterprise Server 9 platform uses asynchronous scriptlets, so the uninstall process cannot guarantee that the instance stops before it removes files.

Uninstall on UNIX®, Linux, and macOS

This section provides instructions for upgrading instances, an application, or both on the members of a mirror.

As noted in Mirror Compatibility, all failover members of a mirror must be of the same InterSystems IRIS version, and can differ only for the duration of an upgrade. DR async members, however, may run on a different version than the failover members as part of a broader upgrade strategy. For example, they may remain on an older version for an extended period to serve as a fallback after upgrading the primary and backup members.

Once an upgraded member becomes primary, you cannot make use of the other failover members (and in particular cannot allow them to become the primary) until the upgrade is completed.

Reporting async members are also not required to run the same version as the failover members, although application
functionality may require it; for more information, see InterSystems IRIS Instance Compatibility.

There are four mirror upgrade paths to choose from. To determine which procedure you should follow, review the factors in the Choosing Mirror Upgrade Procedure section below. The four procedures are located in the Mirror Upgrade Procedures section below.

Also review the following two sections about upgrading a mirror:

- Mirror Upgrade Terms, which defines some of the terms used in the mirror upgrade procedures.

- Adding Mirror Members During an Upgrade, which discusses when you should add members to a mirror.

Important:

On Linux systems supporting systemd, although it is possible to use either systemctl commands or the
/etc/init.d/ISCAgent script to manage the ISCAgent, you must choose one method and use it exclusively;
the ISCAgent should always be stopped using the method with which it was started. For more information, see Starting the ISCAgent on Linux Systems in the “Mirroring” chapter of the InterSystems High Availability Guide.

When you upgrade an instance on such a Linux system, a running ISCAgent is automatically restarted using systemd. If you are using the /etc/init.d/ISCAgent script to manage the ISCAgent, stop the agent before performing the upgrade so that it is not automatically restarted, then restart it using the script after the upgrade.

### 5.1 Choosing Mirror Upgrade Procedure

To upgrade your mirrored environment, you must choose one of four supported upgrade procedures. To determine the best upgrade procedure for your system, follow the flo wchart or review the criteria below.

If you are upgrading to a maintenance release and you aren’t making any application changes during the upgrade process, you can use this simplified procedure.

For details, see Procedure 1: Maintenance Release Upgrades with No Application Changes.

This procedure can be used for major version upgrades or upgrades with application changes where downtime is not a concern and simplifies some steps by shutting do wn all mirror members at the same time.

For details, see Procedure 2: Major Version Upgrades with Planned Downtime.

Procedures 3 & 4: Major Version Upgrades with Minimal Downtime

If you are upgrading to a major version or performing applications changes and you need to minimize downtime you must use Procedure 3 or 4. Procedure 3 allows for the shortest downtime, only requiring the time necessary to perform a planned failover. Procedure 4 involves downtime while you perform any application upgrades and recompile mirrored classes and routines.

No Procedure1:...Start...Yes Areyoumakingapplicati...MajorVersionMaintenanceReleaseWhatkindofreleaseare... No Yes Isdowntimeaconcernfo... No YesDoyouhaveclassesand... No YesAreyouperforminganap... No YesAreyouusinginteropera...Procedure3:...Procedure2:...Procedure4:...

Adding Mirror Members During an Upgrade

If any of the following conditions apply, your upgrade involves mirrored database changes and you must use Procedure 4: Major Version Upgrade with Mirrored Database Changes.

- Classes and routines are stored in mirrored databases that also contain application data.

- An application upgrade you are performing includes changes to data in a mirrored database.

- Your system uses interoperability productions.

If none of the above conditions apply, you should use Procedure 3: Major Version Upgrade with No Mirrored
Database Changes.

### 5.2 Adding Mirror Members During an Upgrade

If you plan to add members to a mirror, you may want to defer this until you plan to perform one of the upgrades described in this section and add members of the new version during the upgrade, so that you do not have to upgrade them later. You can always add members of a newer version to a mirror during an upgrade, provided you immediately continue with and complete the upgrade as described, with one restriction: once a member of the newer version becomes primary, it must remain primary until all other members have been upgraded.

Adding new members during an upgrade can be very helpful when migrating a mirror to new hardware. Rather than upgrading one of the failover members before failing over to it, you can install a new instance of the new version on the target system, add it to the mirror as a DR async member, promote it to backup and then fail over to it, thus migrating the mirror primary to the new system. By repeating this technique you can then migrate the remaining failover member.

### 5.3 Mirror Upgrade Terms

In the procedures in this section, the following terms are used:

Upgrade classes and routines

Recompile all classes in all application namespaces on the instance. This should be done after a major version upgrade (as described in Post-Upgrade Tasks) and/or application upgrade, which may involve one or more of the
following operations, depending on your situation:

- As noted in the foregoing, when classes exist in any mirrored database that also contains application data, they must be recompiled locally on the functioning primary failover member (regardless of whether they are modified by an application upgrade). It is recommended that an y existing routines are recompiled.

- Classes and routines stored in nonmirrored routines databases that are separate from application data can be recompiled on a mirror member regardless of whether it is the current primary.

- Classes and routines stored in separate nonmirrored routines database can also be “precompiled” by recompiling a copy of the database on a system that has already been upgraded to the target product release, then distributed to each mirror member following the upgrade.

System A

The mirror member that is initially the primary failover member.

System B

The mirror member that is initially the backup failover member.

Set/clear no failover state

Use the ^MIRROR routine to set or clear the no failover state so that failover cannot occur; see Avoiding Unwanted
Failover During Maintenance of Failover Members for instructions.

Perform a graceful shutdown

Use the iris stop command to shut the instance down cleanly (see Controlling InterSystems IRIS Instances).

Promote to failover member

Follow the procedure for promoting a DR async mirror member to failover member as described in Promoting a DR Async Member to Failover Member.

Viewing the Mirror Monitor

Use the Mirror Monitor page in the instance’s Management Portal to review the status of the mirror and its members;
see Using the Mirror Monitor.

### 5.4 Mirror Upgrade Procedures

There are four mirror upgrade paths to choose from. To determine which procedure you should follow, review the factors
in the Choosing Mirror Upgrade Procedure section. The four procedures are:

- Procedure 3: Major Version Upgrade with No Mirrored Database Changes

- Procedure 4: Major Version Upgrade with Mirrored Database Changes

- These four procedures assume that for each instance you have already performed any relevant steps listed in the Pre-Upgrade
steps. For details on upgrading an individual instance, refer to the procedure for your operating system:

- Windows

- Unix®, Linux, or macOS

#### 5.4.1 Procedure 1: Maintenance Release Upgrades with No Application Changes

If you are upgrading to a maintenance release rather than a new major version and are not making any application changes, use the following procedure, which renders the mirror unavailable only for the time required to execute a planned failover.

1. Access the Mirror Monitor. You should use the Mirror Monitor throughout the upgrade process to confirm that each

step is performed correctly. Whenever a step involves shutting down mirror member, failing over, or restarting a mirror member, you should confirm after performing that the Mirror Monitor correctly reflects the change.

2. To prevent failover from occurring until the backup is fully upgraded, set the no failover state.

3. Perform a graceful shutdown of the backup (B).

4. Upgrade the backup (B) with the new version of your product. System B restarts and returns as backup.

5. Clear the no failover state.

6. Perform a graceful shutdown of the primary (A). The mirror fails over and the backup (B) takes over as primary.

7. Upgrade system A with the new version of your product. System A restarts and becomes backup.

8. Perform a graceful shutdown of the primary (B). The mirror fails over and the backup (A) becomes the primary. This
ensures that all automated upgrade and reactivation steps are performed on both mirror members and that both instances are ready to act as primary.

9. Restart system B so that it returns as backup.

#### 5.4.2 Procedure 2: Major Version Upgrades with Planned Downtime

If you are upgrading to a new major version and/or performing an application upgrade and have a significant planned maintenance window that obviates the need to minimize mirror downtime, you may prefer to use the following procedure,
regardless of whether changes to mirrored databases on the primary are required:

1. Disallow all user access to the mirror using established practices at your site. Additionally, you must disable any

application jobs that would normally start on instance startup.

2. Access the Mirror Monitor. You should use the Mirror Monitor throughout the upgrade process to confirm that each

step is performed correctly. Whenever a step involves shutting down mirror member, failing over, or restarting a mirror member, you should confirm after performing that the Mirror Monitor correctly reflects the change.

3. Perform a graceful shutdown of the backup (B).

4. Perform a graceful shutdown of the primary (A).

5. Upgrade system B with the new version of your product. System B restarts and becomes primary.

6. Upgrade mirrored classes and routines on system B. If an application upgrade requires further changes to mirrored

databases, make these changes.

7. Upgrade nonmirrored classes and routines on system B, if any.

8. Upgrade system A with the new version of your product. System A restarts and becomes backup. Mirrored classes and

routines on system A catch up with those on system B and are automatically upgraded.

9. Upgrade nonmirrored classes and routines on system A, if any.

10. Perform a graceful shutdown of the primary (B). The mirror fails over and the backup (A) takes over as primary. This
ensures that all automated upgrade and reactivation steps are performed on all mirror members and that all instances are ready to act as primary.

11. Restart system B so that it returns as backup.

12. Restore user access to the mirror.

#### 5.4.3 Procedure 3: Major Version Upgrade with No Mirrored Database Changes

If you are upgrading to a new major version and/or performing an application upgrade and have determined that changes to mirrored databases are not required (as described in Choosing a Mirror Upgrade Procedure), you may be able to use the following procedure. This procedure only requires downtime for the length of time it takes to execute a planned failover.

This procedure is simplest for static applications where separate nonmirrored routines databases are always maintained. It can, however, be used even if the separate routines databases are normally mirrored by removing these databases from the mirror for the duration of the upgrade. See Temporarily Removing Mirrored Databases From the Mirror for details on this process.

1. Enact a code freeze and application configuration freeze to disallo w application changes during the upgrade, using

established procedures at your site, to ensure that routines databases are not modified during the upgrade.

2. Access the Mirror Monitor. You should use the Mirror Monitor throughout the upgrade process to confirm that each

step is performed correctly. Whenever a step involves shutting down mirror member, failing over, or restarting a mirror member, you should confirm after performing that the Mirror Monitor correctly reflects the change.

3. To prevent failover from occurring until the backup is fully upgraded, set the no failover state.

4. Perform a graceful shutdown of the backup (B).

5. Upgrade the backup (B) with the new version of your product. System B restarts and returns as backup.

6. Upgrade all classes and routines on system B.

7. Clear the no failover state.

8. Perform a graceful shutdown of the primary (A). The mirror fails over and the backup (B) takes over as primary.

9. To prevent system A from taking over as primary until fully upgraded, set the no failover state.

10. Upgrade system A with the new version of your product. System A restarts and returns as backup.

11. Upgrade all classes and routines on system A.

12. Clear the no failover state.

13. Perform a graceful shutdown of the primary (B). The mirror fails over and the backup (A) becomes the primary. This
ensures that all automated upgrade and reactivation steps are performed on all mirror members and that all instances are ready to act as primary.

14. Restart system B so that it returns as backup.

##### 5.4.3.1 Temporarily Removing Mirrored Databases from the Mirror

Procedure 3 can be used for systems that mirror routines databases by temporarily removing the databases from the mirror during the upgrade process.

Important:

If the routines databases are normally mirrored, ensure that they do not contain any application data before removing them from the mirror.

This procedure cannot be used with normally mirrored routines databases if ECP application servers connect to the mirror.

To use the above procedure with mirrored routines databases:

1. Before starting the upgrade, enact a code freeze and application configuration freeze to disallo w application changes
during the upgrade, using established procedures at your site, to ensure that routines databases are not modified during the upgrade.

2. Before shutting down system B in Step 4, remove the databases from the mirror.

3.

4.

In Step 6, make sure you upgrade the classes and routines in the databases that are temporarily removed from the mirror.

In Step 11, only upgrade non-mirrored classes and routines on system A. (Do not upgrade classes and routines from the databases that were removed from the mirror on system B.)

5. After upgrading the non-mirrored classes and routines on system A, remove the mirrored routines databases from

system A.

6. Add the databases to the mirror on system B.

7. Back up the databases on system B and restore them on system A using the procedures for adding an existing database
to a mirror provided in Adding Databases to a Mirror. Retain these backups, as they represent the first backups of
newly-added mirrored databases; older backups made prior to the upgrade cannot be used to restore these databases
in the event of disaster.

8. Add the databases to the mirror on system A.

9. Continue with Step 12 and finish the rest of Procedure 3 as normal.

#### 5.4.4 Procedure 4: Major Version Upgrade with Mirrored Database Changes

If you are upgrading to a new major version and/or performing an application upgrade and have determined that changes to mirrored databases are required (as described in Choosing a Mirror Upgrade Procedure), use the following procedure, which renders the mirror unavailable only for the time it takes to execute a planned failover and make the required mirrored
database changes:

1. Access the Mirror Monitor. You should use the Mirror Monitor throughout the upgrade process to confirm that each

step is performed correctly. Whenever a step involves shutting down mirror member, failing over, or restarting a mirror member, you should confirm after performing that the Mirror Monitor correctly reflects the change.

2. To prevent failover from occurring until the backup is fully upgraded, set the no failover state.

3. Perform a graceful shutdown of the backup (B).

4. Upgrade the backup (B) with the new version of your product. System B restarts and returns as backup.

5. Upgrade nonmirrored classes and routines on system B, if any.

6. Disallow new user access to the mirror using established practices at your site. Additionally, you must disable any

application jobs that would normally start on system B when it becomes primary.

7. Clear the no failover state.

8. Perform a graceful shutdown of the primary (A). The mirror fails over and the backup (B) takes over as primary.

9. Upgrade mirrored classes and routines on the new primary (B). If an application upgrade requires further changes to

mirrored databases, make these changes.

10. Restore user access to the mirror.

11. To prevent system A from taking over as primary until fully upgraded, set the no failover state.

12. Upgrade system A with the new version of your product. System A restarts and returns as backup.

13. Upgrade nonmirrored classes and routines on system A, if any.

14. Clear the no failover state.

15. Perform a graceful shutdown of the primary (B). The mirror fails over and the backup (A) becomes primary. This

ensures that all automated upgrade and reactivation steps are performed on all mirror members and that all instances are ready to act as primary.

16. Restart system B so that it returns as backup.

Upgrade ECP Configurations

In general, ECP application servers should be upgraded before the data servers they connect to. Application servers must have either local routines databases to recompile following upgrade or access to “precompiled” routines database (previously recompiled on a separate system running the target version) on the data server.

Downtime can be minimized using rolling upgrades with users connecting to both upgraded and unupgraded application
servers as well as the database server if one of the following is true:

- There are no application changes.

- There are application changes, but the new code does not generate any new data structures, meaning that old code can work with data generated by new code.

If the new application code can work against old data, but can generate new data structures not understood by the old code,
follow this procedure:

1. Upgrade the application servers on a rolling basis, but do not allow users to connect to an application server once it is

upgraded. (Application server capacity is gradually reduced.)

2. When enough application servers have been upgraded, restore user access to the upgraded application servers and end
all user connections to the remaining (not upgraded) application servers and the data server (if need be), ensuring that users have no access to these systems until you enable it.

3. Upgrade the remaining application servers, restoring user access to each application server after it is upgraded.

4. Upgrade the data server and restore user access as needed. (Upgrading the data server causes a pause in application

activity, the length of which depends on the amount of downtime involved in the upgrade.)

If you have questions or concerns about how to upgrade your ECP configuration, please contact InterSystems Worldwide Customer Support (WRC).

Post-Upgrade Tasks

The post-upgrade tasks required depend on whether you have upgraded to a new major version or to a maintenance release
of the installed version. Also note the following points:

- If you changed an instance from 8–bit to Unicode during the upgrade, the upgrade does not automatically convert your databases. 8–bit databases may be compatible with Unicode in some cases (see Database Compatibility Considerations). If your locale is not compatible, you will need to manually convert the data from 8–bit to Unicode.

- It is not necessary to re-import any OpenAPI 2.0 specification files.

- It is not necessary to re-import any Web Service Definition (WSDL) files.

- Cached queries are always purged during upgrade. They are recompiled and cached as needed.

- If you did not configure your web serv er automatically during the installation process, you will need to connect it manually.

- If your web server is using a port number other than 80, you will need to change the CPF WebServerPort and Web- ServerURLPrefix parameters to your web server’s port number in order to connect with your IDE.

- If you upgraded from an instance with a private web server (2023.1 or older), you should disable and remove the private web server.

- If you are on Linux or AIX® and are using huge or large pages, confirm that the y are still being used:

- In the <install-dir>/mgr/messages.log file, confirm there is a message indicating shared memory has been allocated using huge or large pages.

If huge/large pages are not enabled, you may need to adjust the allocation to account for increases in shared memory with the new version. After reallocating, restart your system to allow the changes to take effect. See Configuring Huge and Large Pages for details on this process.

Interoperability productions require a foundation namespace. For instructions how to create a foundation namespace or convert a standard namespace into a foundation namespace, see Foundation Namespaces.

### 7.1 Maintenance Release Post-Upgrade Tasks

When the upgrade is complete, if your system runs any productions, follow the instructions in Starting a Production to restart the productions.

Typically, maintenance release upgrades do not require you to change external files and clients, or to recompile classes and routines. However, the Studio version on a client must be the same or later than the server version to which it connects.

Post-Upgrade Tasks

Note:

If you are performing a maintenance release upgrade to version 2024.1.4, you must recompile all existing REST web services after the upgrade.

If you choose to recompile, review the information in the Major Version Post-Installation Tasks section.

### 7.2 Major Version Post-Installation Tasks

After upgrading to a new major version, it is important to follow the guidance provided in Special Considerations When Upgrading. You must also perform the following tasks (if you have not already done so as part of one of the previous pro-
cedures in this chapter):

Recompile classes and routines

InterSystems recommends that customers recompile all classes and all routines in each namespace. See How to Compile Namespaces for instructions. You may have your own tools and procedures for this purpose, taking into account any dependencies and other needs particular to the instance that was upgraded.

Reinstall any add-on modules that were installed by InterSystems Package Manager

When you recompile a package, the class compiler automatically removes any classes that are marked deployed from that package, so it is necessary to reinstall those classes.

Recompile custom %SYS classes and routines

The %SYS namespace is skipped by default when compiling all classes and routines. Make sure you recompile the custom classes and routines in this namespace as well. See How to Compile Namespaces for instructions. Only classes and routines beginning with Z, z, %Z, or %z are preserved on upgrade. These classes and routines cannot be precompiled.

Regenerate proxy classes

You must regenerate any proxy classes you had generated in the upgraded instance by following the instructions in the appropriate guides in the InterSystems IRIS Language Bindings set.

This item does not apply to web services and web clients; it is not necessary to re-import any Web Service Definition
(WSDL) files.

Validate production interfaces

You can validate that your upgraded system behaves the way you expect it to by using the Production Validator. The Production Validator extracts HL7 headers, messages, and operation messages to a temporary database, which is then copied to an upgraded InterSystems IRIS for Health instance and replayed. By comparing the original messages to the messages processed on the upgraded system, you can evaluate and address differences.

Review SQL query plans

If your instance is not running in Adaptive Mode, your query plans are frozen after upgrading. See Frozen Plans After Software Version Upgrade for details.

Restart productions

If your system runs any productions, follow the instructions in the Starting a Production section of the “Starting and Stopping Productions ” chapter in Managing Productions.

Major Version Post-Installation Tasks

Upgrade Studio clients

The Studio version on a client must be the same or later than the server version to which it connects.

Upgrade the Web Gateway

If your Web Gateway is on a separate machine from the server you are upgrading, you must also upgrade the Web Gateway on that separate machine. You can accomplish this by following the Windows Upgrade Procedure in this chapter, or performing a silent installation with the ADDLOCAL property as discussed in Windows Unattended
Installation.

Update web server files

Following upgrades you must deploy these using established practices at your site.
