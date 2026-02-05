# InterSystems Supported Platforms

### 1.1 Supported Platforms

This release supports the listed server platforms and operating system releases on the indicated InterSystems products.

- Server Platforms

- Container Platforms

- Cloud Platforms

- Development Platforms

#### 1.1.1 Operating System Patches and Service Packs

Because InterSystems relies on the operating system vendor to ensure compatibility, InterSystems does not certify its products for specific operating system patches or service packs.

In the rare event that a specific patch or service pack (SP) is required to run InterSystems products, the appropriate table indicates the explicit requirement.

If a vendor introduces new features or functionality in a base version to create a new offering, InterSystems does not do additional testing but relies on the vendor to assure the quality of the base version.

#### 1.1.2 Server Platforms

Platform

Notes

IBM AIX® 7.2, 7.3 for POWER System-64 (POWER 8 and higher)

InterSystems IRIS supports OpenSSL 3.0 on AIX 7.2 and 7.3 via the aixopenssl30 kit. This kit has, as prerequisites, the latest Tech Level for either AIX 7.2 and 7.3.

InterSystems IRIS for AIX was compiled using the IBM XL C/C++ for AIX 16.1.x and 17.1.x compilers. If the system on which you are installing InterSystems IRIS does not have both of these versions of the compiler or runtime already installed, you must install them both. First install 16.1.x, then 17.1.x.

See https://www.ibm.com/support/pages/node/612497#171X for more information.

Microsoft Windows:

- Server 2022 and 2025 for x86–64

- Windows OS 10 and 11 for x86–64 Oracle Linux 9 and 10 for x86–64 Unmodified kernel.

Red Hat Enterprise Linux 9 and 10 for x86-64 or ARM64

SUSE Linux Enterprise Server 15 for x86-64 SP6 and up

Ubuntu 22.04, 24.04 LTS for x86-64 or
ARM64

#### 1.1.3 Container Platforms

To use Kerberos on the Red Hat platform, you must install the krb5-devel package in addition to the krb5-libs package. See the Red Hat Linux Platform Notes section of the “Preparing to Install InterSystems IRIS” chapter of the Installation Guide for detailed information on obtaining these components.

See Red Hat’s support lifecycle page for guidance on currently supported minor versions.

See SUSE’s support lifecycle pagefor guidance on currently supported minor versions.

InterSystems IRIS requires OpenSSL 3, which is the default starting with SP6.

A default Ubuntu setting can result in semaphore deletion. See the Ubuntu Platform Notes section of the “Preparing to Install InterSystems IRIS” chapter of the Installation Guide for more information.

Container images from InterSystems comply with the Open Container Initiative (OCI) specification and are b uilt using the Docker Enterprise Edition engine, which fully supports the OCI standard. InterSystems containers therefore are supported on any OCI compliant runtime engine on Linux-based operating systems, both on-premises and in public clouds.

Container host systems are subject to the InterSystems Minimum Supported CPU policy.

InterSystems container images are built and tested using Ubuntu as their base operating system. These images are available
for the CPU architectures shown below:

Supported Platforms

Image Operating System

CPU Architecture

Ubuntu 24.04

- Intel/AMD 64–bit

- ARM 64–bit

#### 1.1.4 Cloud Platforms

InterSystems IRIS can be successfully deployed on cloud platforms that meet both of the following criteria:

- The operating system platform is in the supported Server Platform list.

- The cloud platform provides support for their infrastructure.

Customers using mirroring on cloud virtual machines should note that the public clouds require IP addresses, as opposed to virtual IPs, for mirroring.

#### 1.1.5 Development Platforms

In addition to the listed Server Platforms, the following platforms are supported for development work:

Platform

Notes

- Apple macOS 13, 14, and 15 for x86- 64

- Apple macOS 13, 14, and 15 for
ARM

Use the current version of OpenSSL. You can install this using Homebrew: https://formulae.brew.sh/formula/openssl@3

InterSystems IRIS requires several dependencies to run on this platform. See Installing Required Dependencies for more information.

Key Management Interoperability Protocol (KMIP) is not supported on macOS.

On the M1 platform, Shared Memory Connections (SHM) for Java are not supported.

Support for development platforms is subject to the following qualifications:

- Development platforms are to be used for application development only; they are not supported for deployment of
applications.

- The results of comparative analysis will not be underwritten by InterSystems. No valid conclusions can be drawn from performance, sizing, or other measurements taken on supported development platforms versus other supported platforms.

- InterSystems will reevaluate its continued support for these platforms with each major release of InterSystems IRIS.

#### 1.1.6 Hardware Considerations

In most cases, this document focuses specifically on operating system v ersions, and only generally on the characteristics of the underlying hardware. This section is intended as a refinement of that approach, describing specific features of individual hardware offerings that InterSystems products recognize and use to their advantage.

Minimum Supported CPU

InterSystems IRIS running on Intel and AMD (amd64/x86_64) processors must include the AVX, AVX2, BMI, and BMI2 instructions.

### 1.2 Supported File Systems

This release supports the following file systems on the specified platforms:

Platform

Apple macOS

Microsoft Windows for x86-64

Oracle Linux for x86-64

Red Hat Enterprise Linux for x86-64 or
ARM64

SUSE Linux Enterprise for x86-64

Ubuntu for x86-64 or ARM64

Recommended File
System

Other Supported File Systems

HFS

JFS23,4

NTFS

XFS4

XFS4

XFS4

XFS4

APFS

ext31, ext41,2,4, NFS

Btrfs4, ext31, ext41,2,4, NFS

Btrfs4, ext31, ext41,2,4, NFS

## 1 The data=journal mount option for ext3/ext4 file systems is not supported.

## 2 When using Linux, InterSystems recommends using the ext4 file system for the journal/WIJ and the XFS file system for data files.

## 3 For optimum journaling performance, the cio mount option is recommended for JFS2 file systems.

## 4 On this Unix/Linux platform, throughput of database and WIJ expansion and creation is dramatically improved when
using file systems where space can be reserv ed for a file without writing blocks.

### 1.3 Supported Web Servers

This release supports CSP technology on the following web servers for the indicated platforms. This does not necessarily mean that all InterSystems products run on these platforms, but rather that the InterSystems Web Gateway component does.

Web Server

Apache 2.4

Platform

- Apple macOS

- IBM AIX® for POWER System-64 *

- Microsoft Windows**

- Oracle Linux

- Red Hat Enterprise Linux

- SUSE Linux Enterprise

- Ubuntu Microsoft IIS 7.0 and later

- Microsoft Windows

Nginx (Stable)

- Apple macOS

- Microsoft Windows

- Red Hat Enterprise Linux

- SUSE Linux Enterprise

- Ubuntu *Using Kerberos security and/or SSL for the Web Gateway on 64-bit UNIX® platforms requires 64-bit Apache.

**Requires manual configuration. See Install a Stand-Alone Web Gateway for details.

### 1.4 Supported Web Browsers

InterSystems IRIS supports CSP on the web browsers listed in the following tables.

Browser Platforms

Newer versions of the browsers listed in the following table will be supported with the understanding that critical issues may be found that will have to be corrected in a major release of InterSystems IRIS. Those fix es will not be backported to earlier releases of InterSystems IRIS.

InterSystems also requires that browsers support the XML HTTP interface which limits support for some older browser versions.

Platform

Windows

Linux

Android

iOS

macOS

Chrome, Edge, Firefox, Opera

Firefox

Chrome

Safari

Chrome, Firefox, Opera, Safari

Portals

Support for the InterSystems IRIS Management Portal is limited to the browsers listed in the following table. Except where noted, this includes support for InterSystems IRIS® Business Intelligence functionality. New versions released by vendors
are assumed to provide backward compatibility; they are supported as described in Supported Web Browsers and are tested
as they become available.

Web Browser (Platform)

Version

Chrome (Windows, macOS)

Edge (Windows)*

latest released

latest released

Firefox (Windows, macOS, Linux)

latest released

*At this time, InterSystems does not fully support InterSystems IRIS® Business Intelligence functionality on Microsoft
Edge.

### 1.5 ODBC Support

InterSystems products support multithreaded ODBC on most platforms.

The InterSystems ODBC driver on UNIX®-based systems supports the following driver managers:

- The iODBC driver manager (see http://www.iodbc.org) — for use with the Unicode and 8-bit ODBC APIs; works
with the select executable and the following drivers:

- libirisodbc35.so libirisodbciw35.so iODBC 3.5 driver

iODBC 3.5 Unicode driver

The unixODBC driver manager (see http://www.unixodbc.org) — for use with the 8-bit ODBC API only; works with
the selectu executable and the following driver:

libirisodbcuw35.so

unixODBC 3.5 Unicode driver

libirisodbcur6435.so

unixODBC Real Mode built 3.5 driver

### 1.6 Node.js Support

This release supports Node.js clients on the platforms and operating system versions listed in the Supported Server Platforms table. For information about installation and configuration, see Nati ve SDK for Node.js.

### 1.7 Platform Endianness

When restoring a backup or transferring a database, the target system must be the same Endianness (Big-endian or Little-
endian) as the source system; for example, if a backup was created on a Big-endian system, it cannot be restored to a Little-
endian system. For information, see “ Using cvendian to Convert Between Big-endian and Little-endian Systems”.

The following table identifies the Endianness of the supported serv er platforms for this release:

Supported SQL Gateway Databases

Platform

Apple macOS

Microsoft Windows for x86-64

Oracle Linux for x86-64

Red Hat Enterprise Linux for x86-64 or ARM64

SUSE Linux Enterprise Server for x86-64

Ubuntu for x86–64 or ARM64

Endianness

Little-endian

Big-endian

Little-endian

Little-endian

Little-endian

Little-endian

Little-endian

### 1.8 Supported SQL Gateway Databases

The InterSystems IRIS SQL Gateway supports access to external databases from InterSystems IRIS so long as:

- The external database is supported by its manufacturer. For example, InterSystems IRIS can support a connection to Oracle 10g as long as Oracle 10g is still in Oracle's extended maintenance window.

- The connecting driver is compliant with the appropriate protocol. InterSystems IRIS supports ODBC 3.0 through 3.7 as well as JDBC 4.0 through 4.3.

The SQL Gateway provides features for querying external databases using the InterSystems IRIS SQL dialect. InterSystems
regularly tests these features against the latest versions of the following database systems:

- IBM Db2

- IBM Informix

- Microsoft SQL Server

- MySQL

- Oracle

- Sybase Adaptive Server Enterprise

### 1.9 Supported .NET Frameworks

InterSystems supports .NET on Windows, Linux, and macOS. Versions of the .NET Framework are supported only on Windows. All InterSystems assemblies for .NET are installed to the .NET GAC (Global Assembly Cache) when InterSystems IRIS is installed.

You can use any version of Visual Studio that is supported by Microsoft for your .NET development, with the following exception: Entity Framework (EF) development requires specific Visual Studio tools to be installed in order to work with newer versions of Visual Studio. The current EF Provider supports up to VS 2019 for InterSystems IRIS. VS 2022 is not supported.

Note:

The InterSystems IRIS installation procedure does not install or upgrade any version of .NET or .NET Framework. Your client system must have a supported version of .NET or .NET Framework installed in order to use these assemblies.

There is a separate version of the IRISClient assembly (InterSystems.Data.IRISClient.dll) for each supported version of .NET and .NET Framework. These files are located in the follo wing subdirectories of <iris-install-dir>\dev\dotnet (see “Installation
Directory” in the Installation Guide for the location of <iris-install-dir> on your system):

- .NET Framework 3.5: \dev\dotnet\bin\v3.5

- .NET Framework 4.6.2: \dev\dotnet\bin\v4.6.2

- .NET 6.0: \dev\dotnet\bin\net6.0

- .NET 9.0: \dev\dotnet\bin\net9.0 The current default version is .NET 9.0.

Note:

Extra Requirements for XEP

If your application uses both .NET Framework and XEP (see Persisting .NET Objects with InterSystems XEP), you must also declare the InterSystems.Data.XEP.dll assembly.

There is a separate version of this file for each of the follo wing .NET Framework versions:

- .NET Framework 3.5: \dev\dotnet\bin\v3.5

- .NET Framework 4.6.2: \dev\dotnet\bin\v4.6.2 XEP does not require a separate assembly if your application uses .NET 6.0 or higher.

In some applications, the .NET Framework assemblies may be used to load unmanaged code libraries. Both 32-bit and 64- bit assemblies are provided for each supported version, which makes it possible to create gateway applications for 64-bit Windows that can load 32-bit libraries.

If you wish to use a version other than the default for your system, some extra configuration will be required to set the path to your desired language platform.

Note:

InterSystems IRIS .NET clients do not support Kerberos because the .NET Framework does not include direct Kerberos support.

### 1.10 Supported Java Technologies

InterSystems Java products require a Java Development Kit (JDK) from Oracle (or a compatible JDK). This release supports
the following JDKs:

Development Kits

Java SE Development Kit (JDK)

OpenJDK

Versions

## 8 and higher

## 8 and higher

Please contact InterSystems if you would like to take advantage of InterSystems product license sharing when running Java on Windows Terminal Servers.

### 1.11 Other Supported Technologies

This release supports other technologies as specified in the follo wing tables:

Other Supported Technologies

Supported Libraries

ICU

Xerces

Xalan

OpenSSL

* New at this release.

ODBC Driver Managers

unixODBC

iODBC

Version

69.1

3.2

1.12*

Instance-specific; to determine the version in use by
the instance, call
$SYSTEM.Encryption.OpenSSLVersion()

Version

2.3.4

3.52.4

### 1.12 Other Supported Features

InterSystems products support the LDAP protocol, multithreaded callin, T-SQL programming extensions, the MQ Interface, Embedded Python, and IntegratedML as indicated in the following table. (Supported operating system versions are those listed in the Supported Server Platforms table.)

Platform

Supported Features

Version of Python Supported for Embedded Python (2)

Flexible Python
Runtime Support (3)

Apple macOS

IBM AIX® for POWER
System-64

Microsoft Windows for x86-64

Oracle Linux for x86-64

LDAP, T-SQL,
Embedded Python,
IntegratedML

LDAP, T-SQL, MQ
Python

Python

Python 3.11 (installed using homebrew)

Python 3.9.18+ (installed from the AIX Toolbox for Open
Source Software)4

No

No

Python 3.9+

Yes

Python 3.6

Yes

Platform

Red Hat Enterprise Linux for x86-64 or ARM64

SUSE Linux Enterprise for x86-64

Ubuntu for x86–64 or ARM64

Supported Features

Version of Python Supported for Embedded Python (2)

Flexible Python
Runtime Support (3)

Red Hat 8: Python 3.6

Red Hat 9: Python 3.9

Yes

Python 3.6

Yes

Ubuntu 20.04: Python 3.8

Ubuntu 22.04: Python 3.10

Yes

## 1 The minimum version supported by InterSystems IRIS is WebSphere MQ V7.0.

## 2 For more information, see Recommended Python Version.

## 3 Supports the Flexible Python Runtime feature, which allows you to use a version of Python higher than the default version of Python for your operating system.

## 4 Supported on the aixopenssl30 kit only.

Supported Languages

InterSystems IRIS provides National Language Support (NLS) for selected regions in one or more character sets. InterSystems IRIS also includes utility translations for some languages. These localizations exist for the languages as indicated in the following table.

InterSystems IRIS documentation is available in English and Japanese.

### 2.1 InterSystems IRIS

The languages in the following table are supported by InterSystems IRIS in this release:

Language

Arabic

Character Sets

CP1256 (Arabic), Latin/Arabic, Unicode

Chinese (Simplified)

GB18030 (Chinese National Standard), Unicode

Chinese (Traditional)

Unicode

Chinese (Mandarin)

Unicode

Czech

Danish

Dutch

English

Finnish

French

German

Greek

Hebrew

Hungarian

Italian

ASCII †, Latin-1, Latin-9, CP1252 (Western Europe), Unicode

CP1253 (Greek), Latin-G, Unicode

CP1257 (Hebrew), Latin-H, Unicode

Included

Utility
Translation

Included

Included

Included

Included

Included

Supported Languages

Language

Japanese

Korean

Lithuanian

Maltese

Polish

Character Sets

Unicode

Unicode

CP1257 (Baltic), Latin-4, Latin-6, Latin-7, Unicode

Latin-3, Unicode

Portuguese (Brazil)

Utility
Translation

Included

Included

Included

Included

CP1251 (Cyrillic), Latin-C, Unicode

Unicode

Unicode

Included

CP874 (Thai), Latin-T, Unicode

Unicode

Unicode

Included

Russian

Slovak

Slovenian

Spanish

Thai

Turkish

Ukranian

† US English only.

### 2.2 NLP

The following languages are supported by Natural Language Processing in this release:

Dutch

English

French

German

Japanese

Portuguese

Russian

Spanish

Swedish

Ukrainian

- Discontinued Platforms and Technologies

- This page discusses the platforms and technologies that this release no longer supports. For information on InterSystems technologies that are deprecated and discontinued, see Deprecated and Discontinued Features.

- 3.1 Discontinued Server Platforms

- This release is not available for the following server platform versions:

- Platform

- Red Hat Enterprise Linux 8 for x86-64 or ARM64

- Red Hat Enterprise Linux 7.9 for x86-64

- Red Hat Enterprise Linux 7.0 through 7.8

- SUSE Linux Enterprise Server 12 SP3

- SUSE Linux Enterprise Server 12 Ubuntu 18.04 LTS Ubuntu 16.04 LTS

### 3.2 Discontinued Container Platforms

This release is not available for the following container base OS versions:

Container Base OS

Ubuntu 18.04 LTS

Ubuntu 16.04 LTS

version 2021.2

version 2019.1

Discontinued Platforms and Technologies

### 3.3 Discontinued Cloud Platforms

This release is not available for the following cloud platform versions:

Platform

Ubuntu 10.04 LTS

SUSE Linux Enterprise Server 12

version 2019.1

version 2019.1

### 3.4 Discontinued Development Platforms

This release is not available for the following development platform versions:

Platform

Apple macOS 10.13, 10.14, 10.15

CentOS-7

version 2021.2

version 2022.2

### 3.5 Discontinued Java Development Kits

This release is not available for the following Java Enterprise specifications:

Java Development Kit

JDK 1.7

version 2020.1

Supported Version Compatibility

This page describes which components of InterSystems IRIS® data platform can be used across different release versions.

Note:

Throughout this page, “version 2025.1” refers to InterSystems IRIS version 2025.1.

For information about compatibility between InterSystems IRIS and other InterSystems software, see the Inter- Systems IRIS Migration Guide on the WRC distribution site under Docs.

### 4.1 ODBC and JDBC Compatibility

While InterSystems IRIS ODBC and JDBC clients are forward- and backward-compatible with all versions of InterSystems IRIS, it is best practice to keep them updated to benefit from the latest b ug fix es, client/server capabilities, and optimizations.

Customers are advised to upgrade their client libraries before upgrading their InterSystems IRIS server.

The following table describes the version interoperability between ODBC and JDBC clients, and servers.

Client Version

Server Version

2025.1

2024.3

2024.2

2024.1

2023.2

2023.1

### 2018.1 through 2025.1

### 2018.1 through 2024.3

### 2018.1 through 2024.2

### 2018.1 through 2024.1

### 2018.1 through 2023.2

### 2018.1 through 2023.1

### 4.2 Web Gateway Compatibility

The InterSystems Web Gateway is backward-compatible with earlier versions of InterSystems IRIS. However, using an earlier version of the Web Gateway with a newer version of InterSystems IRIS is not supported.

Customers are advised to upgrade the Web Gateway before upgrading their InterSystems IRIS server.

The following table describes the version interoperability between the Web Gateway and InterSystems IRIS.

Supported Version Compatibility

Web Gateway Version

Compatible InterSystems IRIS Versions

2025.1

2024.3

2024.2

2024.1

2023.2

2023.1

### 2018.1 through 2025.1

### 2018.1 through 2024.3

### 2018.1 through 2024.2

### 2018.1 through 2024.1

### 2018.1 through 2023.2

### 2018.1 through 2023.1

### 4.3 Backup Restore Compatibility

Backups should always be restored on an InterSystems IRIS instance that is running the same, or a more recent version, than the instance that created the backup. This is because an older version of InterSystems IRIS may not be able to process newer features.

### 4.4 Journal Restore Compatibility (Upgrade Implications)

Journal file restores are guaranteed to be successful when restored on an InterSystems IRIS instance that is running the , a journal file restore is same, or a more recent version than the instance that created the journal file. More specifically guaranteed to be successful if the target instance uses the same version or a later version of the journal file format, relati ve to the journal file being used. On the other hand, journal file restores are not guaranteed to be successful when restoring to an older instance.

Important:

InterSystems IRIS 2025.1 introduces a new journal file format that is incompatible with earlier v ersions. Journal files created by instances running InterSystems IRIS 2025.1 or later cannot be restored on instances running any version prior to InterSystems IRIS 2025.1.

As a consequence, for a mirrored system, when you upgrade to a version from one version to another that uses a different journal file format, you must tak e care to do the upgrades in the correct order. Specifically , always upgrade backup members before upgrading the primary.

InterSystems strongly recommends always upgrading to the most recent maintenance release available for your InterSystems IRIS version to ensure feature compatibility.

### 4.5 Mirror Compatibility

All members of a mirror must run on the same version of InterSystems IRIS. There are two exceptions:

1. Mirror members may run on different versions for the duration of a mirror upgrade. See Upgrading a Mirror in the

“Upgrading InterSystems IRIS” chapter of the Installation Guide. Once an upgraded mirror member becomes primary, you cannot allow the other failover member or any DR async members to become primary or access the application, until that member has been upgraded.

2. Async members may run on a different version than the other members of the mirror, for the following reasons:

Mirror Arbiter (ISCAgent) Compatibility

- DR async members may continue to run on an older version for an extended period of time, as part of a broader upgrade strategy. For example, to fall back to after upgrading the primary and backup members.

- Reporting async members may run on a newer version to take advantage of a newer reporting features when upgrading the primary and backup members is not warranted.

Mirroring relies on journaling, hence the restrictions and recommendations described in the previous section also apply here.

### 4.6 Mirror Arbiter (ISCAgent) Compatibility

The ISCAgent serving as arbiter does not have to run the same version of InterSystems IRIS as the members of the mirror for which it is configured. We recommend that the arbiter always run a version greater than or equal to the highest version of the mirror members that connect to it. InterSystems recommends that you upgrade the arbiter when you upgrade the mirror members, so you can be sure to have the latest version of the ISCAgent.

### 4.7 ECP Compatibility

ECP is backward and forward compatible between InterSystems IRIS versions. This includes compiled routines and class definitions, which can be passed o ver ECP and run on instances that are running a different version of InterSystems IRIS. However, application code on both ends of an ECP connection must be compatible. For example, if your code performs different business logic on different ECP servers, then your overall application behavior will be unpredictable.

Customers are advised to ensure that their feature usage is compatible with all of their versions of InterSystems IRIS that are connected via ECP. For example, InterSystems IRIS 2021.2 introduced transparent stream compression. If a newer server writes stream data via ECP to an older server, the stream data won’t be readable on servers running versions that don't support transparent stream compression. Such incompatibilities can exist and are typically addressed in Maintenance Releases. InterSystems strongly recommends always upgrading your ECP configurations to the most recent maintenance release available for your InterSystems IRIS version.

Cross-Product Technology Matrix

In general, connectivity components of InterSystems IRIS are not compatible with older InterSystems products. However, there are certain exceptions. For information about cross-product compatibility, see “Coexistence & Compatibility” in the InterSystems IRIS Migration Guide. You can download this guide from the WRC Document Distribution page (login required).
