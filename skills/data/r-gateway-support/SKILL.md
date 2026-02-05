# R Gateway Support

The InterSystems R Gateway is an extension of the Java External Server that enables a connection to an R interpreter
through third party software. It incorporates two third party packages:

- Rserve is a binary package that provides a TCP/IP connection to an R interpreter.

- R-Engine is a Java client for Rserve.

These packages allow InterSystems IRIS to access the R interpreter via the InterSystems R Gateway. The R Gateway provides an interface to the R language that can be used in the same way as any other External Server language interface (see Using InterSystems External Servers for more information).

Figure 1: R Gateway System

Note:

Known Limitations

Java differentiates empty string and null string, while the InterSystems IRIS database does not. The Java client maps both Java null and Java empty string to database empty string. InterSystems IRIS empty strings are mapped to Java null. To avoid problems, do not assign different meanings to empty and null strings.

## 1 Installing R and RServe

Requirements

- Java 8 or higher

- InterSystems IRIS 2020.4 or later. The following required resources are included with InterSystems IRIS:

- –

- – the InterSystems %R_Server External Server is installed automatically (see “Controlling Connections with the Management Portal” in Using InterSystems External Servers) the org.rosuda.REngine package is included in intersystems-rgateway-<version>.jar and used by the
External Server.

R interpreter (download a recent instance from https://cloud.r-project.org/)

RServe (must be installed from the R Console, as described below)

Note:

Although it has a similar name, the RGateway posted on GitHub (https://github.com/intersystems-community/RGateway) uses an older technology and is not supported by InterSystems.

Install R interpreter

Download and install the latest version of R: https://cloud.r-project.org/. Be sure to make R accessible to all users.

Install Rserve server

Rserve is a TCP/IP server which allows other programs to use facilities of R (see http://www.rforge.net/Rserve/index.html).

- Set environment variable R_LIBS to a directory accessible to all users. This is to make sure Rserve package is available to all users after installation. Details can be found at https://cran.r-project.org/doc/manuals/Radmin.html#Managing-libraries

- Start the R Console.

- In the R Console, run install.packages(“Rserve”,,"http://rforge.net")

- If prompted to install from sources, answer "Yes". Please refer to Rserve documentation (https://www.rforge.net/Rserve/doc.html) for more details.

## 2 Running the R Gateway

InterSystems IRIS connects to Rserve through an External Server gateway (see Using InterSystems External Servers for
detailed information). To run the R Gateway, you must:

- Launch Rserve (either from the R Console or from ObjectScript, as described below).

- Start the R Gateway from the Management Portal.

- Create the RConnection interface between Rserve and the R interpreter.

- Create an R Gateway and use it to run R commands.

Launch Rserve

Rserve can be started manually on any host and port. It can also be launched programmatically from InterSystems IRIS on localhost.

To start Rserve manually, type the following commands in the R Console:

library(Rserve)
Rserve()

If unsuccessful, try Rserve(args="--no-save --slave") . Please refer to Rserve documentation (https://www.rforge.net/Rserve/doc.html) for more details.

To launch Rserve programmatically from IRIS, issue the following command:

Do
##class(%Net.Remote.Object).%ClassMethod(gateway,"com.intersystems.rgateway.Helper","launchLocalServer",
port)

Start R Gateway

R Gateway can be started from Management Portal: System->Configuration->Connectivity->External Language Servers. A new R Gateway can also be created from this page.

See the %R Server entry in the Configur ation Parameter File Reference for a description of the %R Server parameters found in the [Gateways] section of the CPF.

Create RConnection

RConnection is the interface between Rserve and the R interpreter. Each RConnection corresponds to a R session. Each R session has its own memory space. R sessions are not thread-safe. On UNIX machines, multiple RConnections can be created on a single port. On Windows machines, a single port can only support a single connection. Multiple Windows connections can be established using one port for each connection.

If Rserve is running, RConnection can be created directly:

set c = ##class(%Net.Remote.Object).%New(gateway,"org.rosuda.REngine.Rserve.RConnection")

If you are not sure whether Rserve is running, you can use the helper class to start it automatically. If Rserve is
not running, it will try to start it locally and return an instance of RConnection:

set c =
##class(%Net.Remote.Object).%ClassMethod(gateway,"com.intersystems.rgateway.Helper","createRConnection")

Note that the above calls can take additional parameters, such as host name, port number etc.

Create an R Gateway object and run R statements

You can create an R Gateway object from the default gateway or a named gateway:

- To get the default R Gateway (named "%R Server"): set gateway =
$SYSTEM.external.getRGateway()

- To get a named R Gateway: set gateway = $SYSTEM.external.getGateway("gateway name") When you create an R Gateway object, it provides an interface to the R language that can be used just like other External Server language interfaces (see Using InterSystems External Servers for more information).

$SYSTEM.external is an ObjectScript External Server command interface that simplifies using the R Gate way
from an InterSystems terminal. For usage, type do gateway.Help() in the terminal.
