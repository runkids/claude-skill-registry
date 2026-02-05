# Windows Installation Details

Windows User Accounts

When installing InterSystems IRIS, you must choose the Windows user account to run the InterSystems service, InterSystems
IRIS Controller for <instance-name>. There are two options:

- The default SYSTEM account (Windows Local System account). This is used in Minimal security installations.

- A defined Windows user account. This account must have interactive login privileges for the duration of the installation;
they can be revoked after.

Running the InterSystems service under the default SYSTEM account is appropriate for many installations, but in some cases can cause issues relating to file permissions and netw ork security access. If you anticipate potential problems in these areas for an InterSystems IRIS instance—for example due to your network configuration or security arrangements—specify a Windows account for the InterSystems service that has the needed privileges and access, such as a domain administrator account.

For instructions on how to change the service account after installation, see Managing Access to the InterSystems IRIS
Instance.

Important:

If you are using Kerberos, you must configure a Windows account before installing InterSystems IRIS. InterSystems recommends you use a separate account specifically set up for this purpose as described in Preparing the Security Environment for Kerberos.

Note:

If running InterSystems IRIS under a defined Windows user account, be sure to grant that account the Windows “Lock Pages in Memory” (SELockMemory) privilege. See Configuring Lar ge Pages on Windows in the “Preparing to Install InterSystems IRIS” chapter for details.

Installing a Web Server on Windows

Before installing InterSystems IRIS, you should install a supported web server in order to access web applications, including the Management Portal. The installation procedure will vary depending on the web server you choose. For details, you should refer to your web server’s documentation.

In many cases, the InterSystems IRIS installer can automatically configure a ne w or upgraded instance to serve its built-in web applications using your web server. For details, see Connect Your Web Server Automatically.

If you would like to manually set up your web server, you can do this after installing IRIS. For details, see Connect Your Web Server Manually.

If you intend on configuring the web serv er manually and you are performing an unattended installation, you should include the cspiis component and set CSPSKIPIISCONFIG=1. This installs the necessary IIS CSP binary files without configuring your web server. If the cspiis component is included and CSPSKIPIISCONFIG is not set or is set to 0, the installer will attempt to configure your web serv er and will fail if one is not detected.

If you do not plan on configuring a web serv er at any point, you can omit cspiis from ADDLOCAL. This prevents the installation of the IIS CSP binary files.

Important:

InterSystems recommends using the Microsoft IIS web server because it can be automatically configured during the installation process. Make sure it is installed and running before beginning the installation process. In most cases, it is not necessary to manually configure the IIS web serv er.

### 3.1 Command-Line Properties Reference

The command-line properties reference describes the InterSystems IRIS-specific unattended install properties that you can modify via the command-line interface. These can be used when performing an unattended installation or when launching an attended installation from the command line. The property name must be uppercase, but the arguments are not case-
sensitive; each property must be separated by one or more spaces, and properties can be specified in an y order as
PROPERTYNAME=argument. For example:

... ISCSTARTIRIS=0 ISCSTARTLAUNCHER=0 INITIALSECURITY=Normal

Note:

In the following reference, the REINSTALL and REMOVE properties are used with installed instances, as described in Running an Unattended Upgrade or Reinstall and Running an Unattended Removal, respectively.

ADDLOCAL

Default: ALL (installs all features)

Use this property to custom install a new instance of InterSystems IRIS with a subset of features or to omit optional databases (see the Custom-Installable Features Reference) by specifying a comma-separated list of featurenames together with their group names, as described in the example following this reference.

See also the REINSTALL property, for use with installed instances.

CSPSKIPIISCONFIG

Default: 0 if the cspiis component is included, otherwise 1

Use this property to install IIS CSP binary files. With a value of 1, the files are installed without an y changes to the IIS web server configuration. With a value of 0, the installer updates the IIS web server configuration re gardless of the existence of the /csp virtual directory.

When this property is set to 0, the installation will fail if a web server is not detected. If you don’t want the installer to automatically configure your web serv er, you should set this property to 1.

CSPSYSTEMUSERPASSWORD

Default: value of IRISUSERPASSWORD if security level is Normal or LockedDown, otherwise not used

If the security level is Normal or LockedDown, optionally use this property to specify a password for the CSP- System predefined user .

If the initial security level is None, do not use this property.

CSPSYSTEMUSERPASSWORD

Default: value of IRISUSERPASSWORD

Optionally use this property to specify a password for the CSPSystem predefined user .

INITIALSECURITY

Default: LockedDown

Use this property to specify the level of security to be used by the instance being installed. Specify None, Normal, or LockedDown.

Use this property to specify the level of security to be used by the instance being installed. Specify Normal or
LockedDown.

See also the IRISUSERPASSWORD, CSPSYSTEMUSERPASSWORD, and SERVICECREDENTIALS properties in this reference.

INSTALLDIR

Default: C:\InterSystems\IRISn, where n is {empty}, 1, 2, ... 127.

Default: C:\InterSystems\IRISHealthn, where n is {empty}, 1, 2, ... 127.

Default: C:\InterSystems\HealthConnectn, where n is {empty}, 1, 2, ... 127.

Use this property to specify the directory in which the instance is to be installed.

INSTALLERMANIFEST

If installing with an installation manifest, as described in Using the Manifest in the appendix “Creating and Using an Installation Manifest”, you must use this property to specify the location of the installation manifest (that is, your exported manifest class).

INSTALLERMANIFESTLOGFILE

If installing with an installation manifest, as described in Using the Manifest in the appendix “Creating and Using an Installation Manifest”, this property specifies where %Installer prints messages.

INSTALLERMANIFESTLOGLEVEL

If installing with an installation manifest, optionally use this property to specify the log level of the setup() method of your installation manifest class. The default log level is 1.

INSTALLERMANIFESTPARAMS

If installing with an installation manifest, as described in Using the Manifest in the appendix “Creating and Using an Installation Manifest”, use this property to specify the name/value pairs (name=value) to be passed to the first argument of the setup() method of your installation manifest clas. This property can be used to modify the config-
uration parameter file ( iris.cpf) and activate the changes before your manifest runs. You can specify these parameters:

- bbsiz

- globals4kb, globals8kb, globals16kb, globals32kb, globals64kb

- gmheap

- LibPath

- locksiz Command-Line Properties Reference

- MaxServerConn

- Path

- routines

- ZFSize, ZFString

For example:

INSTALLERMANIFESTPARAMS="bbsiz=512000,globals4kb=20, globals8kb=30,globals16kb=40,globals32kb=50, globals64kb=100,routines=40,gmheap=10000, LibPath=c:\libpath\,locksiz=2179648,MaxServerConn=5, Path=c:\lib\,ZFSize=2000,ZFString=3000"

The following would be useful in installing and activating 100 MB of 64KB buffers before running a manifest
that creates a 64kb block size database:

INSTALLERMANIFESTPARAMS="globals64kb=100"

IRISSERVICEDOMAIN

Required if the service credentials are defined as UserDefined

If the service credentials are specified as LocalSystem, do not use this property.

See the SERVICECREDENTIALS property in this reference. Use this property to specify the domain of the Windows InterSystems service login account specified by IRISSERVICEUSER.

IRISSERVICEPASSWORD

Required if the service credentials are defined as UserDefined

If the service credentials are specified as LocalSystem, do not use this property.

See the SERVICECREDENTIALS property in this reference. Use this property to specify the password for the Windows InterSystems service account specified by IRISSERVICEUSER.

IRISSERVICEUSER

Required if the service credentials are defined as UserDefined

If the service credentials are specified as LocalSystem, do not use this property.

See the SERVICECREDENTIALS property in this reference. Use this property to specify the username of the account under which to run the Windows InterSystems service.

IRISUSERPASSWORD

Required if the security level is Normal or LockedDown

If the initial security level is None, do not use this property.

See the INITIALSECURITY property in this reference. Use this property to specify the password for the predefined InterSystems IRIS accounts _SYSTEM, Admin, and SuperUser, as well as the account with the username specified by IRISSERVICEUSER if SERVICECREDENTIALS is specified as UserDefined.

IRISUSERPASSWORD

Required

Use this property to specify the password for the predefined InterSystems IRIS accounts _SYSTEM, Admin, and SuperUser, as well as the account with the username specified by IRISSERVICEUSER if SERVICECREDENTIALS is specified as UserDefined.

ISCSTARTIRIS

Default: 1 (start InterSystems IRIS after installation)

Optionally set this property to 0 to prevent InterSystems IRIS from starting after installation.

ISCSTARTLAUNCHER

Default: 1 (add the launcher to the system tray)

Optionally set this property to 0 to prevent the InterSystems IRIS launcher from being added to the system tray.

REINSTALL

Use this property to reinstall (repair) an installed instance of InterSystems IRIS or to change the custom-installed
features (see the Custom-Installable Features Reference) for an installed instance of InterSystems IRIS:

- To reinstall whatever features are currently installed for the instance—whether that is a custom-installed subset of features or all features—specify ALL.

- To reinstall a subset of InterSystems IRIS features that is different from the subset of features currently installed, specify a comma-separated list of featurenames together with their group names (as described in the example following this reference).

See also the ADDLOCAL property (for use with new instances) and REMOVE property (for uninstalling installed instances).

REMOVE

Use this property to uninstall (remove) an instance of InterSystems IRIS or a subset of custom-installed features
(see the Custom-Installable Features Reference) installed for an installed instance of InterSystems IRIS:

- To remove an instance of InterSystems IRIS, specify ALL.

- To remove a subset of InterSystems IRIS features, specify a comma-separated list of featurename together with their group names (as described in the example following this reference).

See also the ADDLOCAL (for new instances) and REMOVE properties in this reference.

SERVICECREDENTIALS

Default: LocalSystem if security level is Normal or LockedDown, otherwise not used

If the initial security level is None, do not use this property.

If the security level is Normal or LockedDown, optionally use this property to specify the credentials under which the Windows InterSystems service runs: LocalSystem for the default local system account or UserDefined (an existing Windows user account).

If you specify UserDefined for this property, you must also specify the IRISSERVICEDOMAIN, IRISSERVICEPASSWORD, and IRISSERVICEUSER properties.

See Managing Access to the InterSystems IRIS Instance for important information about the InterSystems service account.

Custom-Installable Features Reference

SERVICECREDENTIALS

Default: LocalSystem

Use this property to specify the credentials under which the Windows InterSystems service runs: LocalSystem for the default local system account or UserDefined (an existing Windows user account).

If you specify UserDefined for this property, you must also specify the IRISSERVICEDOMAIN, IRISSERVICEPASSWORD, and IRISSERVICEUSER properties.

See Managing Access to the InterSystems IRIS Instance for important information about the InterSystems service account.

SKIPUPGRADECHECK

Default: 0 (pre-upgrade checking enabled)

When upgrading an instance, set this property to 1 to bypass system pre-upgrade checking.

Note:

Generally, you should leave pre-upgrade checking enabled.

SUPERSERVERPORT

Default: 1972 if available, otherwise 51773 or the first a vailable subsequent number

Use this property to specify the Superserver port to be used by the instance being installed.

UNICODE

Default: 1 (16–bit Unicode characters are supported)

Use this property to specify whether 8–bit or 16–bit Unicode characters are to be supported by the instance being
installed. For 8–bit characters, specify 0; for 16–bit characters, specify 1.

Important:

Do not use this parameter for InterSystems IRIS for Health and HealthShare Health Connect installations. These products require support for 16–bit Unicode characters and therefore must use the default value.

### 3.2 Custom-Installable Features Reference

The custom-installable features reference lists component group/component names and the associated featurename for each. You can specify “ ALL” (to specify all available features) or a comma-separated list (with no spaces) of feature names (to specify individual features).

To specify components in ADDLOCAL, REINSTALL, and REMOVE properties, specify the featurename of a component group, followed by the featurename of each specific component from that group that you w ant installed. For example, to
install only the USER database include the following in the command line:

ADDLOCAL=server,server_user

When specifying a component group, you must also specify at least one associated component; if no components are listed
with a component group, the component group is ignored and no components are installed. For example, if you specify:

ADDLOCAL=documentation,documentation_pdf,server,development,callin

the server component group is ignored and no server components are installed. (This requirement does not apply to the ipm or cube groups, as they have no components.)

development

Use development for the development component group which includes the following components:

- ActiveX Connectivity (activex)

- Callin (callin)

- Callin, Threaded (callin_threaded)

- Other Development Libraries (development_other) documentation

Use documentation for the documentation component group which includes the following components:

- PDF Documentation (documentation_pdf) cube server

Use cube for the launcher component. This component group includes no other components.

Use server for the server component group which includes the following components:

SQL Gateway (sqlgateway)

Apache Formatting Objects Processor (fop)

Server monitoring tools (server_monitoring)

Agent Service (agent_service)

InterSystems Package Manager (ipm)

HotJVM RenderServer/QueuingRenderServer for Zen Reports (renderserver)

- sqltools

- Use sqltools for the database drivers component group which includes the following components:

- ODBC (odbc)

- JDBC (jdbc)

- cspgateway

- Use cspgateway for the Web Gateway component group which includes the following components:

- IIS (cspiis)

- Managing Auto-start

- The Windows InterSystems service includes the instance name. After installing, by default the instance starts automatically
when you start your server; this means the InterSystems IRIS instance is automatically configured to autostart (start when
the system starts).

You can configure the instance not to autostart by changing the Start InterSystems IRIS on System Boot setting on the Memory and Startup page of the Management Portal (from the home page, select System Administration > Configuration > System Configuration > Memory and Startup).

The Write-cache Buffer

Certain InterSystems IRIS features utilize Windows write-cache buffer flushing, which is enabled by default. To verify this
option is correctly enabled and InterSystems IRIS receives the full benefit of these features:

1. Open the Device Manager from the Control Panel.

2. Select the storage device from the Disk Drives section.

3. Click on the Policies tab.

4. Ensure that Turn off Windows write-cache buffer flushing on this device is not selected.
