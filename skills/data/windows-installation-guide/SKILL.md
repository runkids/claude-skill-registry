# Windows Installation Guide

Windows Installation Overview

The Windows Installation Guide provides guidance on installing kit-based deployments on Microsoft Windows.

### 1.1 How to Use This Guide

For all installations, you should begin with the Pre-Installation steps. You can then follow the steps for either an attended or unattended installation. The attended installation process is different depending on the setup type you choose. After following the steps for attended installations, use the documentation for the setup type you’ve chosen to continue the installation process. After completing the installation, refer to the Post-Installation section for additional tasks that should be completed.

This guide breaks steps into sections titled Default and More. Default includes basic information for a given step, details on what actions need to be taken, and recommendations on which options to choose. More includes additional details and other options that can be chosen.

In general, the Default sections are sufficient for quickly getting started. If you are unsure about a particular step or about which option to select, it is recommended you follow the guidance in the Default sections.

### 1.2 Deploying for Production Systems

Deploying for a live production system is a more involved procedure than deploying for development. In particular, you should carefully consider the resources at your disposal and plan your configuration and deplo yment accordingly. Before beginning the installation process, you should review the following sections that give detailed guidance on planning and
managing your resources:

- System Resource Planning and Management

- Memory and Startup Settings You can still follow the procedures outlined in this guide, however the procedures outlined in the Default sections may not be sufficient for your system. Re view each step thoroughly, including the More sections, and select the configuration options appropriate for your system.

Additionally, you should consider the following when installing for a production system:

- Unattended installations are recommended for production systems. This method allows you to easily save your configuration and redeploy with the same settings.

Windows Installation Overview

- You should install with “Locked Down” security settings. This allows for the strongest initial security for your deployment. See Initial InterSystems Security Settings for more details.

- If you are performing an attended installation, the custom installation is recommended. This allows you to only install the components necessary for your deployment.

Windows Pre-Installation

This page details the pre-installation steps for Windows installations.

Before beginning, make sure you review the Windows Installation Overview, including:

- How to Use This Guide

- Deploying for Production Systems

### 2.1 Step 1: Review Supported Platforms

Default:

- Review InterSystems Supported Platforms before installing to make sure the technologies you intend on using are supported.

### 2.2 Step 2: Choose Your Windows User Account

Default:

- Use a defined Window domain administrator account.

- You can also use the default SYSTEM account, however this is not recommended.

More:

- Review details on Windows User Accounts.

### 2.3 Step 3: Install a Web Server

Default:

- Enable Microsoft Internet Information Services (IIS). Make sure you also enable HTTP Redirection and WebSocket
Protocol.

Windows Pre-Installation

More:

- Install another supported web server (you will have to manually configure this web serv er).

- Proceed with Microsoft IIS turned off (you will have to manually configure a web serv er).

- Some installations will fail unless IIS auto-configuration is successful or skipped. To skip auto-configuration, e xecute the installation file from the command line and specify the CSPSKIPIISCONFIG=1 flag. See Installing a Web Server for details.

### 2.4 Step 4: Install the VS Code ObjectScript Development Environment

Default:

- Install InterSystems ObjectScript extensions for Visual Studio Code.

- This can be done before or after installing.

- The development environment enables you to connect to an instance and develop code in ObjectScript.

### 2.5 Step 5: Acquire a Kit

Default:

- Acquire an installation kit from the WRC kit download site.

### 2.6 Step 6: Choose Your Installation Strategy

Default:

- Perform an Attended Installation using the Installer Wizard.

More:

Perform an Unattended Installation.

Use an Installation Manifest.

- Windows Attended Installation

- This page details the initial steps for attended installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 3.1 Step 1: Execute the Installation File

Default:

- Double click on your installation file to launch the Installer Wizard.

More:

- Launch your installation file from the command line. This allows you to use command line properties to modify the
installation. For example, the following would prevent the instance from starting immediately after installation:

C:\Users\Public\Downloads\IRIS-<version_number>-win_x64.exe ISCSTARTIRIS=0 ISCSTARTLAUNCHER=0

- You can change the Installer Wizard’s language by changing the Windows language for non-Unicode programs setting.

### 3.2 Step 2: Begin Installation

Default:

- Choose New Instance and click OK.

- Use Next to continue to the next dialog box, Back to return to the previous dialog box, and Cancel to stop the installation.

- Review the terms of the License Agreement. Click I accept the terms in the license agreement to confirm that you accept the license agreement.

More:

- Click on an existing instance to upgrade the instance.

Windows Attended Installation

### 3.3 Step 3: Name the Instance

Default:

- Click Next to use the default name.

More:

- Give your instance a unique name, using only alphanumeric characters, underscores, and dashes.

- The default name is IRIS (or, if other instances exist, IRISn, where n is the number of instances already installed—the second instance will be IRIS1).

- The default name is IRISHealth (or, if other instances exist, IRISHealthn, where n is the number of instances already installed—the second instance will be IRISHealth1).

- The default name is HealthConnect (or, if other instances exist, HealthConnectn, where n is the number of instances already installed—the second instance will be HealthConnect1).

### 3.4 Step 4: Choose the Installation Directory

Default:

- Click Next to use the default installation directory:

C:\InterSystems\<name-of-instance>

More:

- Click Change to specify a different destination directory. Review Installation Directory for details on where instances can be installed.

- If the specified directory doesn't e xist, the Installer Wizard will automatically create it.

### 3.5 Step 5: Choose a Setup Type

Default:

- Select the Development setup type and click Next to continue.

- Continue reading the documentation for a Development setup type.

More:

- Choose any setup type. Review Choosing a Setup Type for details on the different setup types.

- Continue reading the documentation for the setup type you choose:

– Development

–

Server

– Client

– Web Server

– Custom

- If the CSP Gateway is already installed on your system when you install the Web Gateway, the installer automatically upgrades the CSP Gateway to the Web Gateway. For details, see Preexisting CSP Gateway.

Step 5: Choose a Setup Type

Windows Development Installation

This page details the steps for attended development installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 4.1 Development Installation Overview

Default:

- A development installation installs only the components that are required on a development system.

More:

- Development installations include the following component groups:

–

–

InterSystems IRIS Database Engine (including user database, Language Gateways, InterSystems Package Manager, and Server Monitoring Tools)

– Database drivers

–

InterSystems IRIS Application Development (including language bindings)

- For details on these component groups, see Choosing a Setup Type.

### 4.2 Step 1: Configure Web Server

Default:

- Make sure the installer says “Local IIS web server detected” and choose the option Configure local IIS web server for this instance.

Windows Development Installation

- If the installer says “No local web server found”, choose Abort the installation. Review Installing a Web Server and ensure that Microsoft Internet Information Services (IIS) is on, then start the installation process over by executing the installation file .

More:

- InterSystems recommends that you use the IIS web server and allow the Installer Wizard to automatically configure it. You should review the automatic configuration beha vior.

- It is possible to manually configure your web serv er after installation. This requires additional steps after finishing the installation process. If you choose this option, continue the installation process selecting the option to continue without configuring the web serv er.

### 4.3 Step 2: Install Unicode Support

Default:

- More:

- See Character Width Setting for details on 8–bit and Unicode systems and choosing one for you system.

This step is skipped by the HealthShare installer and Unicode support is chosen automatically. Continue to the next step.

Important:

For InterSystems IRIS for Health and HealthShare Health Connect installations this must be Unicode.

### 4.4 Step 3: Choose Initial Security

Default:

- More:

- See Initial InterSystems Security Settings for details on the different security settings and choosing one for your system.

### 4.5 Step 4: Enter Credentials

Default:

- Choose to Run InterSystems IRIS under default SYSTEM account.

More:

- The SYSTEM account is not always appropriate. See Windows User Accounts for details on which account you should use.

- Specify a defined Username account. The installer will verify that the account exists on the domain and the password is correct.

### 4.6 Step 5: Configure Users

Default:

- Enter a password that will be used by all predefined user accounts.

- After selecting Next, enter a password for the CSPSystem account.

- Both passwords must be between 8 and 32 characters (3 and 32 if you chose an initial security setting other than Locked
Down).

More:

- Review Initial InterSystems Security Settings for details on password criteria.

- Review Predefined User Accounts for details on the predefined accounts that are created during this step.

### 4.7 Step 6: Review Installation

Default:

- Review the installation options you specified.

- (Optional) Select the License button to navigate to the directory where your license key is located. If the key is valid it will be activated automatically and the License Key setting in Summary of installation options will update to say
Valid.

- Once you have reviewed the installation options and, optionally, added a license key, select Install.

More:

- If you activate a license key during this step it is automatically copied to install-dir/mgr during installation and renamed iris.key.

- If you don’t activate a license key during this step, you can activate one following installation. See Activating a License Key, for details.

### 4.8 Step 7: Complete Installation

Default:

- Once the installation process completes, continue to Windows Post-Installation.

More:

- By default, the instance starts automatically after installation is complete and the launcher icon is added to the system tray area of the Windows tool bar. An InterSystems IRIS item is also added to the Windows Programs menu.

Windows Server Installation

This page details the steps for attended server installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 5.1 Server Installation Overview

Default:

- A server installation installs only the components that are required on a server system.

More:

- Server installations include the following component groups:

–

–

InterSystems IRIS Database Engine (including user database, Language Gateways, InterSystems Package Manager, and Server Monitoring Tools)

- For details on these component groups, see Choosing a Setup Type.

### 5.2 Step 1: Configure Web Server

Default:

- Make sure the installer says “Local IIS web server detected” and choose the option Configure local IIS web server for this instance.

- If the installer says “No local web server found”, choose Abort the installation. Review Installing a Web Server and ensure that Microsoft Internet Information Services (IIS) is on, then start the installation process over by executing the installation file .

Windows Server Installation

More:

- It is highly recommended that you use the IIS web server and allow the Installer Wizard to automatically configure it. You should review the automatic configuration beha vior.

- It is possible to manually configure your web serv er after installation. This requires additional steps after finishing the installation process. If you choose this option, continue the installation process selecting the option to continue without configuring the web serv er.

### 5.3 Step 2: Install Unicode Support

Default:

- More:

- See Character Width Setting for details on 8–bit and Unicode systems and choosing one for you system.

This step is skipped by the HealthShare installer and Unicode support is chosen automatically. Continue to the next step.

Important:

For InterSystems IRIS for Health and HealthShare Health Connect installations this must be Unicode.

### 5.4 Step 3: Choose Initial Security

Default:

- More:

- See Initial InterSystems Security Settings for details on the different security settings and choosing one for your system.

### 5.5 Step 4: Enter Credentials

Default:

- Choose to Run InterSystems IRIS under default SYSTEM account.

More:

- The SYSTEM account is not always appropriate. See Windows User Accounts for details on which account you should use.

- Specify a defined Username account. The installer will verify that the account exists on the domain and the password is correct.

### 5.6 Step 5: Configure Users

Default:

- Enter a password that will be used by all predefined user accounts.

- After selecting Next, enter a password for the CSPSystem account.

- Both passwords must be between 8 and 32 characters (3 and 32 if you chose an initial security setting other than Locked
Down).

More:

- Review Initial InterSystems Security Settings for details on password criteria.

- Review Predefined User Accounts for details on the predefined accounts that are created during this step.

### 5.7 Step 6: Review Installation

Default:

- Review the installation options you specified.

- (Optional) Select the License button to navigate to the directory where your license key is located. If the key is valid it will be activated automatically and the License Key setting in Summary of installation options will update to say
Valid.

- Once you have reviewed the installation options and, optionally, added a license key, select Install.

More:

- If you activate a license key during this step it is automatically copied to install-dir/mgr during installation and renamed iris.key.

- If you don’t activate a license key during this step, you can activate one following installation. See Activating a License Key, for details.

### 5.8 Step 7: Complete Installation

Default:

- Once the installation process completes, continue to Windows Post-Installation.

More:

- By default, the instance starts automatically after installation is complete and the launcher icon is added to the system tray area of the Windows tool bar. An InterSystems IRIS item is also added to the Windows Programs menu.

Windows Client Installation

This page details the steps for attended client installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 6.1 Client Installation Overview

Default:

- A client installation installs only the components that are required on a client system.

More:

- Client installations include the following component groups:

–

– Database drivers

–

InterSystems IRIS Application Development (including language bindings)

- For details on these component groups, see Choosing a Setup Type.

### 6.2 Step 1: Review Installation

Default:

- Review the installation options you specified.

- Once you have reviewed the installation options, select Install.

Windows Client Installation

### 6.3 Step 2: Complete Installation

Default:

- Before you can use the client, you must specify the preferred server for this client. See Define a Remote Serv er Connection for details.

- Once the installation process completes, continue to Windows Post-Installation.

More:

- By default, the launcher icon is added to the system tray area of the Windows tool bar. It appears dimmed because there is no InterSystems IRIS server running.

Windows Web Server Installation

This page details the steps for attended web server installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 7.1 Web Server Installation Overview

Default:

- A web server installation installs only the components that are required for the Web Gateway.

More:

- Web server installations include the following component groups:

- For details on these component groups, see Choosing a Setup Type.

### 7.2 Step 1: External Web Server Configuration

Default:

- The installer will automatically configure the Microsoft Internet Information Services (IIS) web serv er. Make sure you installed the web server prior to beginning the installation.

More:

- Review details on automatic configuration beha vior for IIS web servers.

- If a local web server is not detected, you will have to manually connect your web server after the installation finishes.

- The Web Gateway configures the follo wing application paths pointing to the server configured for the instance:

–

/

Windows Web Server Installation

–

–

/csp

/instance-name (by default, /IRIS)

- You can change the configurations manually after installation using the Web Gateway application.

### 7.3 Step 2: Review Installation

Default:

- Review the installation options you specified.

- Once you have reviewed the installation options, select Install.

### 7.4 Step 3: Complete Installation

Default:

- Once the installation process completes, continue to Windows Post-Installation.

This page details the steps for attended custom installations using the installer wizard.

Make sure you have completed the following before performing the steps on this page:

### 8.1 Custom Installation Overview

Default:

- A custom installation allows you to select specific components to install on the system. Some selections require that you install other components.

### 8.2 Step 1: Select Components

Default:

- Select the components you want to install. Some components include sub-items; to view these, select the + icon.

- Clicking on a component displays a short Feature Description.

- Use the drop-down next to a component to choose whether or not it should be installed. Selecting the X icon corresponding to This feature will not be available will prevent that component and any sub-items from being installed.

- Before continuing, review the next step for details on web server configuration for custom installations.

More:

- Review the table of available components.

- Click Space to ensure that there is enough space on the disk for the selected components.

### 8.3 Step 2: Web Server Configuration

Default:

- If you are including the web gateway components (Web Server Gateway), make sure the CSP for IIS sub-item is included and that the Microsoft Internet Information Services (IIS) web server is installed before beginning the installation. The installer will automatically configure the IIS web serv er for the Web Gateway.

More:

- If the Web Server Gateway and CSP for IIS components are both selected, but an IIS web server is not detected, the installation will fail unless IIS configuration is skipped.

- –

- To skip IIS configuration, execute the installation file from the command line and specify CSPSKIPIISCONFIG=1. This will skip automatic web server configuration and install the IIS CSP binary files necessary for manual configuration in the C:\inetpub\CSPGateway\ directory. You will have to manually configure your web serv er after the installation finishes.

If you only select the Web Server Gateway component and do not select the CSP for IIS component, the installation will be successful, but the IIS CSP binary files will not be installed. This options allows you to manually configure a different supported web server.

If you do not intend on using a web server at any point you can choose to not include either of these components. Without a web server, you will not have access to web applications including the Management Portal.

### 8.4 Step 3: Install Unicode Support

Default:

- More:

- See Character Width Setting for details on 8–bit and Unicode systems and choosing one for you system.

This step is skipped by the HealthShare installer and Unicode support is chosen automatically. Continue to the next step.

Important:

For InterSystems IRIS for Health and HealthShare Health Connect installations this must be Unicode.

### 8.5 Step 4: Set Port Numbers

Default:

- Use the default SuperServer port number.

More:

- The default port number is 1972. If taken, the default is 51773 or the first a vailable subsequent number.

- See Port Numbers for more details.

Step 5: Choose Initial Security

### 8.6 Step 5: Choose Initial Security

Default:

- More:

- See Initial InterSystems Security Settings for details on the different security settings and choosing one for your system.

### 8.7 Step 6: Enter Credentials

Default:

- Choose to Run InterSystems IRIS under default SYSTEM account.

More:

- The SYSTEM account is not always appropriate. See Windows User Accounts for details on which account you should use.

- Specify a defined Username account. The installer will verify that the account exists on the domain and the password is correct.

### 8.8 Step 7: Configure Users

Default:

- Enter a password that will be used by all predefined user accounts.

- After selecting Next, enter a password for the CSPSystem account.

- Both passwords must be between 8 and 32 characters (3 and 32 if you chose an initial security setting other than Locked
Down).

More:

- Review Initial InterSystems Security Settings for details on password criteria.

- Review Predefined User Accounts for details on the predefined accounts that are created during this step.

### 8.9 Step 8: Review Installation

Default:

- Review the installation options you specified.

- (Optional) Select the License button to navigate to the directory where your license key is located. If the key is valid it will be activated automatically and the License Key setting in Summary of installation options will update to say
Valid.

- Once you have reviewed the installation options and, optionally, added a license key, select Install.

More:

- If you activate a license key during this step it is automatically copied to install-dir/mgr during installation and renamed iris.key.

- If you don’t activate a license key during this step, you can activate one following installation. See Activating a License Key, for details.

### 8.10 Step 9: Complete Installation

Default:

- Once the installation process completes, continue to Windows Post-Installation.

More:

- By default, the instance starts automatically after installation is complete and the launcher icon is added to the system tray area of the Windows tool bar. An InterSystems IRIS item is also added to the Windows Programs menu.

This page details the steps for unattended installations.

Make sure you have completed the following before performing the steps on this page:

### 9.1 Unattended Installation Overview

Default:

- An unattended operation does not prompt the user for input; instead, it gets input from properties passed to the instal-
lation file on the command line.

- These properties are described in the Command Line Reference.

- No messages are displayed during unattended installation, upgrade, reinstallation, or uninstallation.

### 9.2 Step 1: Before Beginning

Default:

- Before beginning your installation, perform the necessary pre-installation steps.

- Determine your strategy for installing an external web server:

–

–

The easiest option is to install Microsoft Internet Information Services (IIS) before beginning the installation. The installer can auto-configure this web serv er.

If you intend on using a different web server or manually configuring the IIS web server, review Installing a Web Server for necessary steps that must be performed prior to the installation.

### 9.3 Step 2: Determine Properties to Specify

Default:

- You do not need to include any additional properties to perform a basic unattended installation. The installer will use the default options.

More:

- Review details on using command-line properties.

– Use the form: PROPERTYNAME=argument.

–

Properties must be upper-case.

– Arguments are not case-sensitive.

–

Each property must be separated by one or more spaces.

- Refer to the Command-Line Properties Reference for the properties available for unattended installations.

- Make a note of any properties you will use for your unattended installation.

### 9.4 Step 3: Determine Features to Install

Default:

- The ADDLOCAL property is used to determine which features to install.

- If it is left blank, it defaults to ADDLOCAL=ALL which installs all features.

- For a basic development environment, there is no need to include this property. All features will be installed.

More:

- Review details on specifying custom-installable features.

– Use the ADDLOCAL property to specify which features to include.

–

Specify the featurename of a component group, followed by the featurename components within that group separated by a comma. Repeat this for each component group to create a comma-separated list.

- Refer to the Custom-Installable Features References for available features.

### 9.5 Step 4: Create Installation Command

Default:

- Use the following command:

<path>\<installer>.exe /instance <instancename> /q{b|n} <properties>

where:

Step 4: Create Installation Command

– <path> — The path to the installation file.

– <installer>.exe — The name of the installation file. If omitted, the def ault path is C:\InterSystems\IRISn, where

n is {empty}, 1, 2, ... 127.

– <installer>.exe — The name of the installation file. If omitted, the def ault path is C:\InterSystems\HealthConnectn,

where n is {empty}, 1, 2, ... 127.

– <installer>.exe — The name of the installation file. If omitted, the def ault path is C:\InterSystems\IRISHealthn,

where n is {empty}, 1, 2, ... 127.

– <instancename> — The name for the new instance. If omitted, the default value is IRISn, where n is {empty},

1, 2, ... 127.

– <instancename> — The name for the new instance. If omitted, the default value is HealthConnectn, where n is

{empty}, 1, 2, ... 127.

– <instancename> — The name for the new instance. If omitted, the default value is IRISHealthn, where n is

{empty}, 1, 2, ... 127.

–

/qb or /qn — Whether to display a progress bar during the installation (/qb) or to perform a fully silent installation (/qn).

– <properties> — The properties to passing to the installer (see the Command-Line Properties Reference).

More:

- Replace <properties> with any properties you would like to include in the installation.

- Use the ADDLOCAL property to specify which features you would like to install.

Examples:

- Install an instance with the default instance name in an installation directory named C:\InterSystems\MyIris on a 64–bit
windows system:

- C:\downloads\IRIS-<version_number>-win_x64.exe /qn INSTALLDIR=C:\InterSystems\MyIris

- Install an instance with the instance name IrisA:

- C:\downloads\IRIS-<version_number>-win_x64.exe /instance IrisA /qn

Install a subset of features using the ADDLOCAL property:

C:\downloads\IRIS-<version_number>-win_x64.exe /qn ADDLOCAL=cube, server, server_user

Install all available components.

C:\downloads\<installation_executable.exe> /instance HSHCsilent /qb
INSTALLDIR="D:\InterSystems\HSHCsilent" IRISUSERPASSWORD="<password>"

- Installs all available components.

C:\downloads\<installation_executable.exe> /instance HSIHsilent /qb
INSTALLDIR="D:\InterSystems\HSIHsilent" IRISUSERPASSWORD="<password>"

### 9.6 Step 5: Install the Instance

Default:

- Execute the command, including any properties, using a command-line interface.

- Once the Installation finishes, proceed to Windows Post-Installation.

Windows Post-Installation

This page details the post-installation tasks for Windows installations.

Make sure you have completed the following before performing the tasks on this page:

- Successfully performed an attended or unattended installation.

### 10.1 Post-Installation Tasks

Get Started

- Use the Management Portal to manage your instance.

- Prevent your instance from starting automatically.

Healthcare Setup

- Change the HS_Services password.

- Create a Foundation namespace.

- After creating a Foundation namespace, import the SDA3 schema if you are using SDA3 or SDA3 transformations.

Web Server Setup

- If you did not configure your web serv er automatically during the installation process, you will need to connect it manually.

- In order for your web server to implement any configuration changes, you should restart your web serv er after the installation finishes.

Advanced Setup

- If you plan to connect remotely to other instances, follow the procedure described in Define a Remote Serv er
Connection.

- If you will be performing memory intensive activities, allocate system memory accordingly.

- Review details on how InterSystems products interact with third-party software.

Windows Post-Installation

- Migrate data from a different database to your newly installed instance.

Special Considerations

- If you are running multiple instances, review Configuring Multiple InterSystems IRIS Instances .

- Change the language.

- Verify the Windows write-cache buffer is correctly enabled.
