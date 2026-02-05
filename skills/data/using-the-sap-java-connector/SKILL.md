# Using the SAP Java Connector in Productions

Overview of SAP Java Connector

SAP Java Connector (SAP JCo) is a Java-based component that supports communication with an SAP Server in both directions. InterSystems provides components that you can add to a production to enable the production to communicate
with SAP JCo, and thus with an SAP Server. The following picture shows the architecture:

The architecture includes the Java Gateway, which must be running.

To communicate with SAP JCo, the production must include the following items:

- EnsLib.SAP.Operation, which communicates via TCP/IP with the Java Gateway.

- EnsLib.JavaGateway.Service, which starts and stops the Java Gateway.

This business host performs an additional function: its settings indicate the location of the Java Gateway. When correctly configured, the EnsLib.SAP.Operation business host retrieves those settings and uses them. Thus it is not necessary to set any environment variables.

Unlike most business hosts in a production, EnsLib.JavaGateway.Service does not handle any production messages.

Setup Tasks for the SAP Java Connector

Before you can use the SAP components in a production, you must perform the setup activities discussed in this topic.

To access SAP, it is necessary to provide a username and password. This means that you must also create production credentials that contain an SAP username and password. See Defining Production Credentials .

### 2.1 Setting Up the Java Gateway

The Java Gateway server runs within a JVM, which can be on the same machine as InterSystems IRIS or on a different
machine. Complete the following setup steps on the machine on which the Java Gateway will run:

1.

Install the Java Runtime Environment (for example, JRE 1.8.0_67).

2. Make a note of the location of the installation directory for JRE. This is the directory that contains the subdirectories

bin and lib.

This is the value that you would use for JAVA_HOME environment variable. For example: c:\Program
Files\Java\jre8

You use this information later when you configure your production.

3. Also make a note of the Java version. If you are uncertain about the Java version, open a DOS window, go to the bin

subdirectory of your Java installation, and enter the following command:

java.exe -version

You should receive output like the following, depending on your platform:

java version "1.8.0_67" Java(TM) SE Runtime Environment (build 1.8.0_67-b24) Java HotSpot(TM) 64-Bit Server VM (build 23.19-b22, mixed mode)

It is not necessary to set any environment variables. To access the JVM, InterSystems IRIS uses information contained in the production.

Setup Tasks for the SAP Java Connector

### 2.2 Installing the SAP JCo Jar File

Obtain, from SAP, the SAP Java Connector 3.x, as appropriate for your operating system. Generally, this is provided as a compressed file. Uncompress it and place the contents in a con venient location. The directory should contain the following
items:

- examples subdirectory

- javadoc subdirectory

- Readme.txt file

- sapjco3.dll file

- sapjco3.jar file

- sapjcomanifest.mf file

### 2.3 Generating Proxy Classes for SAP JCo

To communicate with SAP JCo, your interoperability-enabled namespace must contain proxy classes that represent SAP
JCo. To generate these classes, do the following:

1. Start the Java Gateway.

The easiest way to do this is as follows:

a. Create a simple production that contains only one business host: EnsLib.JavaGateway.Service. See EnsLib.Java-

Gateway.Service Settings.

b. Start the production, which starts the Java Gateway.

2.

In the Terminal, change to your interoperability-enabled namespace and use the ImportSAP() method of
EnsLib.SAP.BootStrap, as follows:

do ##class(EnsLib.SAP.BootStrap).ImportSAP(pFullPathToSAPJarFile,pPort,pAddress)

Where:

- pFullPathToSAPJarFile is the full path to the SAP Jar file.

- pPort is the port used by the Java Gateway.

- pAddress is the IP address used by the Java Gateway.

### 2.4 Testing the SAP Connection

To test the SAP connection, do the following in the Terminal (or in code):

1. Create an instance of EnsLib.SAP.Utils, which is the class that the SAP business operation uses internally to connect

to SAP.

2. Set the following properties of that instance. These are string properties unless otherwise noted.

Testing the SAP Connection

- SAPClient—SAP Client e.g 000.

- SAPUser—Username that has access to the SAP server.

- SAPPassword—Password for the user.

- SAPLanguage

- SAPHost— Host name or IP address of the SAP server.

- SAPSystemNumber—SAP SystemNumber e.g 00.

- JavaGatewayAddress—IP address or name of the machine where the JVM to be used by the Java Gateway server is located. Or specify this as the name of the external language server for Java and leave JavaGatewayPort black. For external language servers, Managing External Server Connections.

- JavaGatewayPort—Port used by the Java Gateway. Or leave this blank if JavaGatewayAddress is an external language server name.

- SAPTransactionAutoCommit—Specifies whether to e xecute the BAPI "BAPI_TRANSACTION_COMMIT" after a successful BAPI/RFC-call. This property is %Boolean.

3. Call the PingSAP() method of your instance. This method connects to SAP and performs a dynamic invocation of the

STFC_CONNECTION function. It returns a %Status.

Note: When the SAP business operation first connects to SAP (or when you first call the PingSAP() method), the code creates a file that the Ja va Gateway (and SAP Java driver) later need access to. Starting at release 2024.2, this file is written to the install-dir/mgr directory (rather than the working directory for the namespace). Consequently it
is necessary to make sure that the Java Gateway has access to the file; to do this, configure the Ja
Language Server so that the JVM argument settings include information for finding the file. F or example:

va External

-Djco.destinations.dir=c:\InterSystems\mgr\MYNAMESPACE

This topic describes how to add the required components to your production so that it can send requests to SAP. Also see
Setup Tasks.

### 3.1 Basics

Add the following business hosts to your production.

- The business service EnsLib.JavaGateway.Service. Configure this b usiness host as described later in this topic.

- The business operation EnsLib.SAP.Operation.

- Configure this b usiness host as described in the later in this topic.

One or more business hosts that send SAP request messages to EnsLib.SAP.Operation, as needed.

Use the message classes that you generated. Your business hosts should create instances of these classes, set properties as applicable, and send the messages to the instance of EnsLib.SAP.Operation.

Note: When the SAP business operation first connects to SAP , it creates a file that the Ja va Gateway (and SAP Java

driver) later need access to. Starting at release 2024.2, this file is written to the than the working directory for the namespace). Consequently it is necessary to make sure that the Java Gateway
has access to the file; to do this, configure the Ja
va External Language Server so that the JVM argument settings
include information for finding the file. F or example:

install-dir/mgr directory (rather

-Djco.destinations.dir=c:\InterSystems\mgr\MYNAMESPACE

### 3.2 Settings for EnsLib.JavaGateway.Service

Configure the settings for EnsLib.JavaGateway.Service so that it can find the Ja va Gateway. These settings are:

ExternalServerName

The value of this setting should be an external language server name as described in Managing External Server
Connections.

Stop Named Gateway When Stopping

Determines if an attempt will be made to stop the specified named serv er when this business host stops. The default is off.

### 3.3 Settings for EnsLib.SAP.Operation

EnsLib.SAP.Operation sends requests to SAP JCo, via the Java Gateway. For this business host, specify the following settings:

SAPClient

SAP Client e.g 000.

SAPCredentials

This is the name of the set of production credentials to use when accessing the SAP server. See Defining Production
Credentials.

SAPLanguage

SAPHost

Host name or IP address of the SAP server.

SAPSystemNumber

SAP SystemNumber e.g 00.

SAPTransactionAutoCommit

Specifies whether to e xecute the BAPI "BAPI_TRANSACTION_COMMIT" after a successful BAPI/RFC-call.

SAPResponseHandler

Configuration item in this production that should recei ve the SAP response.

JavaGatewayConfigItemName

Name of the (required) configuration item that hosts the Ja va Gateway.

For settings not listed here, see Settings in All Productions.
