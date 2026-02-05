# Creating WSGI Applications

This page describes how to create a WSGI application that uses the InterSystems IRIS® database, following the PEP-3333 standard.

## 1 Overview

To create a WSGI application that uses InterSystems IRIS, you need only to install a WSGI framework on the same server on which InterSystems IRIS is running, create a callable application, and configure an InterSystems IRIS web application, as described on this page.

## 2 Requirements for the Callable Application

When defining the callable application, note the follo wing requirements:

- Follow the instructions provided by your WSGI framework.

- Import any Python modules needed by your code.

- Place the program files within a dedicated subdirectory of the InterSystems IRIS installation directory . For reasons of history, many existing web applications are in directories with names of the form <install-dir>/csp/appname, where
appname is a short name for the application; this convention keeps the web application files separate from other sub-
directories in the installation directory.

Whatever you choose, you will use this directory name when defining the web application.

- Use relative links, not absolute links, within your application pages.

It is recommended to use InterSystems IRIS as your web application’s database.

## 3 Configuring the Web Application

An InterSystems IRIS web application will control access to the code and will enable communication with the InterSystems IRIS server. You can configure this web application via the Management Portal or programmatically . For basic information
on configuring web applications, see Create and Edit Applications. The critical settings are on the General tab. In particular:

- Name must be unique. The convention is to use a partial directory name that matches the directory that contains the
program files; for e xample: /csp/appname

- This name determines the default directory in which the web server and the Web Gateway will look for files, relati ve to the InterSystems IRIS installation directory.

- For Namespace selection, select the InterSystems IRIS namespace in which the embedded Python process will run by default.

For the Enable selection, select WSGI.

Troubleshooting

- For Application Name, specify the name of the file that contains the callable application.

- If the callable application does not have the default name (application), enter its name into Callable Name.

- For WSGI App Directory, specify the directory that contains the callable application.

- For Allowed Authentication Methods, do not use Unauthenticated unless unauthenticated access is permitted on this system (specified on the Authentication/Web Session Options page (System Administration > Security > System Security > Authentication/Web Session Options).

If unauthenticated access is not allowed on this system but the application is configured to use unauthenticated access, you will receive 403 errors when trying to access the application.

- Decide how to serve any static files and re view Serve Files in the CSP File Settings section:

–

–

If you want InterSystems IRIS to serve the static files, place them into <application-directory>/static and specify Serve Files as Always.

If you want the web server to serve the static files, specify Serve Files as No. (This is recommended for a production web application.)

Ignore the Session Settings options and the Web Settings options (Recurse, Auto Compile, and Lock CSP Name).

## 4 Troubleshooting

The following brief notes offer some guidance in the case of problems with a WSGI application on InterSystems IRIS:

- If InterSystems IRIS cannot find the WSGI application, double-check the web application configuration. If the web application is correct, try and import your Python module in embedded python to check if there are dependency issues. You can also check messages.log and WSGI.log files in the <install-dir>/mgr directory. These logs may have more details.

- If changes to the Python application do not have any effect, the issue may be caching of the Python modules. To be sure that changes are picked up, restart the InterSystems IRIS instance. If restarting is not an option, temporarily use your framework’s shipped development server to do incremental development on your application.

- If database access is not working, note that it is recommended to use InterSystems IRIS as the database. If you are sure you want to use some other database, make sure to give everyone read/write permissions on the database files.

- If HTML links are not working, make sure that the links are relative rather than absolute. Because InterSystems IRIS acts as a proxy for WSGI applications, you must specify relative links for links to the different endpoints in the web application.

- If you are getting 403 (forbidden) errors, note that if you have installed a normal or higher security instance of IRIS, the unauthenticated option is unsupported by default. Make sure to choose another authentication option when configuring the web application.

- If static files ar e not being served, review the comments above about the Serve Files option in the CSP File Settings for the web application.

## 5 See Also

- Applications

- Overview of Authentication Mechanisms

See Also
