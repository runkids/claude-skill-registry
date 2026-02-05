# IRISSECURITY Upgrade Impact

In InterSystems IRIS 2025.2, security data was moved from the IRISSYS database to the IRISSECURITY database, and the %SecurityAdministrator role was introduced for general security administration tasks. Unlike IRISSYS, IRIS- SECURITY can be encrypted, which secures your sensitive data at rest. IRISSECURITY cannot be mirrored, but support is planned for a future version.

The introduction of the IRISSECURITY database introduces several breaking changes in behavior, which can lead to unexpected behavior when upgrading from InterSystems IRIS 2025.1 and below. This page details each change in behavior, the operations affected, and the updated procedures.

Note:

The changes described in this page affect both continuous delivery (CD) and extended maintenance (EM) release tracks. That is, starting with versions 2025.2 (CD) and 2026.1 (EM), InterSystems IRIS will include the IRISSE- CURITY database, and all security data is automatically moved from IRISSYS to IRISSECURITY when you upgrade.

## 1 Before You Upgrade

When you upgrade from InterSystems IRIS 2025.1 or below, all security data is automatically moved from IRISSYS to the IRISSECURITY database. This makes several improvements to data security and access management, but these changes
can be breaking:

- Users can no longer directly access security globals without %All and must instead use the APIs provided by the various security classes.

- OAuth2 globals can no longer be mapped to a different database.

- Users can no longer arbitrarily query security tables, even when SQL security is disabled.

- System databases now use predefined resources that cannot be changed. On Unix, if you created and assigned a ne w resource to a system database in a previous version, it will be replaced by the predefined resource when you upgrade (though if any roles reference the non-default resource, they must be changed manually to use the default resource to keep database access).

On Windows, you must change the resource back to the default. If you attempt to upgrade on Windows while databases have non-default resources, the upgrade will halt (the instance is not modified) and display an error message "Database must have a resource label of..."

The following sections go into detail about these changes and what you should do instead if you depended on the original
behavior, but in general, before you upgrade, you should verify and test that your applications and macros:

- Use the provided security APIs to administer security (as opposed to direct global access).

- Have the necessary permissions (%DB_IRISSYS:R and %Admin_Secure:U) for using those APIs.

## 2 Changes in Behavior and Updated Procedures

The following sections go into detail about these changes and what you should do instead if you depended on the original behavior.

### 2.1 Global Access

Previously, when security globals were stored in the IRISSYS database, users could access security data with the following
privileges:

- %DB_IRISSYS:R: Read security globals both directly and through security APIs.

- %DB_IRISSYS:RW: Read and write security globals.

- %DB_IRISSYS:RW and %Admin_Secure:U: Administer security through security APIs.

Starting InterSystems IRIS 2025.2:

- Security globals are now stored in IRISSECURITY.

- Users can no longer access security globals directly without %All.

- Both %DB_IRISSYS:R and %Admin_Secure:U are the minimum privileges needed to both access security data (through the provided security APIs) and administer security through the various security classes.

- For general security administration, you can use the new %SecurityAdministrator role.

- Read-only access to security data (previously available through %DB_IRISSYS:R) has been removed.

### 2.2 Global Locations

In InterSystems IRIS 2025.2, the following security globals have been moved from IRISSYS to the ^SECURITY global
located in IRISSECURITY:

- ^SYS("SECURITY")

- ^OAuth2.*

- ^PKI.*

- ^SYS.TokenAuthD The following table lists the most notable globals that have been moved, their security classes, old locations, and new
locations:

Table 1:

Security Class

Old Location (IRISSYS)

New Location (IRISSECURITY)

N/A

^SYS("Security","Version")

^SECURITY("Version")

Security.Applications

^SYS("Security","ApplicationsD")

^SECURITY("ApplicationsD")

Security.DocDBs

Security.Events

^SYS("Security","DocDBsD")

^SECURITY("DocDBsD")

^SYS("Security","EventsD")

^SECURITY("EventsD")

Security.LDAPConfigs

^SYS("Security","LDAPConfigsD")

^SECURITY("LDAPConfigsD")

Security.KMIPServers

^SYS("Security","KMIPServerD")

^SECURITY("KMIPServerD")

Security Class

Old Location (IRISSYS)

New Location (IRISSECURITY)

Security.Resources

^SYS("Security","ResourcesD")

^SECURITY("ResourcesD")

Security.Roles

Security.Services

^SYS("Security","RolesD")

^SECURITY("RolesD")

^SYS("Security","ServicesD")

^SECURITY("ServicesD")

Security.SSLConfigs

^SYS("Security","SSLConfigsD")

^SECURITY("SSLConfigsD")

Security.System

Security.Users

^SYS("Security","SystemD")

^SECURITY("SystemD")

^SYS("Security","UsersD")

^SECURITY("UsersD")

%SYS.PhoneProviders

^SYS("Security","PhoneProvidersD")

^SECURITY("PhoneProvidersD ")

%SYS.X509Credentials

^SYS("Security","X509CredentialsD")

^SECURITY("X509CredentialsD ")

%SYS.OpenAIM.IdentityServices

^SYS("Security","OpenAIMIdentityServersD")

^SECURITY("OpenAIMIdentityServersD")

OAuth2.AccessToken

^OAuth2. AccessTokenD

^SECURITY("OAuth2.AccessToken
")

OAuth2.Client

^OAuth2.ClientD

^SECURITY("OAuth2.Client")

OAuth2.ServerDefinition

^OAuth2.ServerDefinitionD

^SECURITY("OAuth2.ServerDefinitionD")

OAuth2.Client.MetaData

^OAuth2.Client.MetaDataD

^SECURITY("OAuth2.Client.MetaDataD")

OAuth2.Server.AccessToken

^OAuth2.Server.AccessTokenD

^SECURITY("OAuth2.Server.AccessTokenD")

OAuth2.Server.Client

^OAuth2.Server.ClientD

^SECURITY("OAuth2.Server.ClientD")

OAuth2.Server.Configuration

^OAuth2.Server.ConfigurationD

^SECURITY("OAuth2.Server.ConfigurationD")

OAuth2.Server.JWTid

^OAuth2.Server.JWTidD

^SECURITY("OAuth2.Server.JWTidD")

OAuth2.Server.Metadata

^OAuth2.Server.MetadataD

^SECURITY("OAuth2.Server.MetadataD")

PKI.CAClient

PKI.CAServer

PKI.Certificate

^PKI.CAClientD

^PKI.CAServerD

^PKI.CertificateD

^SECURITY("PKI.CAClient")

^SECURITY("PKI.CAServer")

^SECURITY("PKI.Certificate")

%SYS.TokenAuth

^SYS.TokenAuthD

^SECURITY("TokenAuthD")

### 2.3 OAuth2 Global Mapping

Previously, you could map OAuth2 globals to a different database, which allowed OAuth2 configurations to be mirrored.

Starting in InterSystems IRIS 2025.2, OAuth2 globals can no longer be mapped, and IRISSECURITY cannot be mirrored.
If you depended on this behavior for mirroring, you can use any of the following workarounds:

- Manually make changes to both the primary and failover.

- Export the settings from the primary and then import them to the failover (requires %All).

To export OAuth2 configuration data:

set items = $name(^|"^^:ds:IRISSECURITY"|SECURITY("OAuth2"))_".gbl"
set filename = "/home/oauth2data.gbl"
do $SYSTEM.OBJ.Export(items,filename)

To import OAuth2 configuration data:

do $SYSTEM.OBJ.Import(filename)

### 2.4 SQL Security

Previously, SQL security was controlled by the CPF parameter DBMSSecurity. When DBMSSecurity was disabled, users with SQL privileges could arbitrarily query all tables in the database.

Starting in InterSystems IRIS 2025.2:

- The DBMSSecurity CPF parameter has been replaced with the system-wide SQL security property. You can enable
(1, default) or disable (0) this in several ways:

– Management Portal: System Administration > System > System Security > System-wide Security Parameters >

Enable SQL security

–

$SYSTEM.SQL.Util.SetOption():

do ##class(%SYSTEM.SQL.Util).SetOption("SQLSecurity", 1)

–

Security.System.Modify():

set properties("SQLSecurity")=1
do ##class(Security.System).Modify(,.properties)

- Security tables can now only be queried through the Detail and List APIs, which require both %DB_IRISSYS:R and %Admin_Secure:U even when SQL security is disabled.

For example, to get a list of roles, you can no longer directly query the Security.Roles table. Instead, you should use the
Security.Roles_List() query:

SELECT Name, Description FROM Security.Roles_List()

### 2.5 Percent-class Access Rules

In previous versions of InterSystems IRIS, the procedure for creating rules for managing a web application's access to additional percent classes involved writing to security globals. You can accomplish this in InterSystems IRIS 2025.2 through the Management Portal or the ^SECURITY routine.

To create a class access rule with the Management Portal:

- Go to System Administration > Security > Web Applications.

- Select your web application

- In the Percent Class Access tab, set the following options:

–

–

–

–

Type: Controls whether the rule applies to the application's access to just the specified percent class ( AllowClass) or all classes that contain the specified prefix ( AllowPrefix).

Class name: The percent class or prefix to gi ve the application access to.

Allow access: Whether to give the application access to the specified percent class or package.

Add this same access to ALL applications: Whether to apply the rule for all applications.

To create a class access rule with the ^SECURITY routine:

- From the %SYS namespace, run the ^SECURITY routine:

DO ^SECURITY

- Choose options 5, 1, 8, and 1 to enter the class access rule prompt.

- Follow the prompts, specifying the following:

–

–

–

–

Application?: The name of the application.

Allow type?: Whether the rule applies to the application's access to just the specified percent class ( AllowClass) or all classes that contain the specified prefix ( AllowPrefix).

Class or package name?: The class or prefix to gi ve the application access to

Allow access?: Whether to give the application access to the specified class or package.
