# InterSystems IRIS Adaptive Analytics

## 1 Overview of InterSystems IRIS Adaptive Analytics

InterSystems IRIS® Adaptive Analytics is an optional extension that provides a business-oriented, virtual data model layer between InterSystems IRIS and popular Business Intelligence (BI) and Artificial Intelligence (AI) client tools. It includes an intuitive user interface for developing a data model in the form of virtual cubes where data can be organized, calculated measures consistently defined, and data fields clearly named. By ha solve the problem of differing definitions and calculations to pro vide their end users with one consistent view of business metrics and data characterization.

ving a centralized common data model, enterprises

Adaptive Analytics provides the following key features:

- The Adaptive Analytics modeler, which makes data accessible for business users without exposing complex data structures, tables, or relationships.

- Publication of data model changes as virtual cubes, preventing disruption caused by lengthy rebuilds.

- Unified access to an online analytical processing (OLAP) model via the BI tool of your choice.

- Live connectivity to all data stored within InterSystems IRIS.

- Automated data structure aggregation for frequently-used queries.

Adaptive Analytics is powered by AtScale®, a product of AtScale, Inc. For documentation of AtScale functionality, consult their official documentation . Note that only users licensed for InterSystems IRIS Adaptive Analytics can view this documentation.

Important:

This version of InterSystems IRIS is compatible with InterSystems IRIS Adaptive Analytics version 2024.1 or later. It is not compatible with earlier versions of Adaptive Analytics.

## 2 Set Up InterSystems IRIS Adaptive Analytics

To set up InterSystems IRIS Adaptive Analytics, you must complete the following steps:

1.

Install or upgrade an instance of AtScale

2. Configure your InterSystems IRIS instance for Adaptive Analytics User-Defined Aggregate Functions

3. Configure AtScale to integrate with your InterSystems IRIS instance

This section describes each step in the setup process in further detail. Troubleshooting provides guidance for common issues you may encounter during this process.

### 2.1 Install or Upgrade AtScale

InterSystems IRIS Adaptive Analytics integrates your InterSystems IRIS instance with an AtScale installation. InterSystems IRIS Adaptive Analytics uses the latest validated version of AtScale. This version is listed on the WRC software distribution page, in the Version column for the Adaptive Analytics package.

Set Up InterSystems IRIS Adaptive Analytics

In order to install or upgrade your instance of AtScale:

1. Download the AtScale installation package appropriate for your operating system from the Components section of the
WRC software distribution page. Search for Adaptive Analytics in the Name column to find the a vailable packages. The filename for the do wnload has the form AdaptiveAnalytics-[AtScaleVersion]-[PlatformVersion].rpm or AdaptiveAnalytics-[AtScaleVersion]-[PlatformVersion].deb. where [AtScaleVersion] is the version of AtScale the package installs, and [PlatformVersion] is the operating system the package is for.

2.

Install or upgrade AtScale and then activate it by following the instructions provided in the official AtScale documentation.

Note: When you purchase InterSystems IRIS Adaptive Analytics, you should receive a separate AtScale license which is applied to the AtScale server. This license is required to activate AtScale. If you have any questions about your license, please contact an InterSystems sales representative.

After you have installed AtScale, import the Adaptive Analytics User-Defined Aggregate Functions to configure InterSystems IRIS Adaptive Analytics as described in the next section.

### 2.2 Configure InterSystems IRIS for Adaptive Analytics

The configuration instructions pro vided here will assume that you have already successfully installed InterSystems IRIS and configured your primary namespace and databases. If you ha ve not done so, consult the instructions in the installation instructions and the Create/Modify a Namespace section of the System Administration Guide. These instructions also assume that you have already successfully installed the appropriate version of AtScale.

In order to leverage Adaptive Analytics User-Defined Aggregate Functions (UDAF), you must first import and re gister
the UDAF class file a vailable from the WRC with the following procedure:

1. Download the latest Adaptive Analytics UDAF Package file ( AdaptiveUDAF.xml) from the Components section of the

WRC software distribution page.

2. On your Adaptive Analytics instance, log in to the Management Portal as a user with administrative privileges and

ensure you are in your Adaptive Analytics namespace.

3. Navigate to System Explorer > Classes and click Go.

4. Click Import. In the modal window, select the My Local Machine option for the The import file resides on field and select

the AdaptiveUDAF.xml file.

5. Check the Compile imported items box and set the Compile flags to cuk. Click Import.

6. Navigate to System Explorer > SQL. Execute the following command:

SQL

CALL AtScaleUDAF.Register()

7. To verify your configuration, na vigate to System Explorer > SQL and execute the following query:

SQL

SELECT ATSCALE_HONEYBEE_VERSION()

The configuration thus f ar will result in a system where aggregates are stored in the same database as source data. InterSystems strongly recommends separating aggregates so that they can be managed and assessed without needing to manually filter
them from a more general data set. To separate aggregates from source data, perform the following steps:

1. Log in to a Terminal session as a user with administrative privileges. Ensure you are in your Adaptive Analytics

namespace.

2. Call the following command to configure your aggre gate database and global mappings:

ObjectScript

write ##class(AtScaleUDAF.Utils).CreateDatabase("/<instancePath>/mgr/AtScale/")

Where <instancePath> is the full path to your Adaptive Analytics instance.

### 2.3 Configuring AtScale for Adaptive Analytics

After you have installed AtScale and configured InterSystems IRIS to use Adaptive Analytics User-Defined Aggregate Functions, configure AtScale according to the procedure described in Adding InterSystems IRIS Data Warehouses.

### 2.4 Troubleshooting Common Setup Issues

#### 2.4.1 Design Center Does Not Load Upon First Login

The Design Center may fail to load the initial setup wizard upon first login, displaying a blank background instead. In such cases, ensure that the atscale.yaml file is properly configured to access the host using a publicly-routable, fully-qualified domain name. For further guidance, refer to the Advanced Configuration section in the AtScale installation documentation.

#### 2.4.2 Service Registry (or Other Service) Fails to Start

An AtScale service may fail to start upon installation if the host has multiple private IP addresses. In such cases, you must bind the malfunctioning service to the specific pri vate IP address which it should use. This can be accomplished by editing
the service’s properties in the atscale.yaml file or by setting an en vironment variable; for detailed instructions, refer to the
Advanced Configuration section in the AtScale installation documentation.

## 3 Exporting InterSystems IRIS Business Intelligence Cubes to AtScale

Adaptive Analytics supports the export of Business Intelligence cubes to Adaptive Analytics cubes. The following procedure for cube export assumes that you have already completed all of the configuration described in the pre vious section. This process does not in any way alter the source Business Intelligence cube.

1. Open a Terminal session on the InterSystems IRIS instance from which you wish to export a cube.

2. Ensure you are in the namespace of the cube you wish to export.

3. Execute the following commands:

ObjectScript

set cube = "CUBENAME" set caltab = "CALENDARTABLE" set file = "PATH/EXPORTFILENAME"

Where CUBENAME is the InterSystems IRIS BI cube name, CALENDARTABLE is the name of your optional calendar table for managing dates, and PATH/EXPORTFILENAME is the target path of the cube export. The following example
places an output file with the cubename and datetime stamp:

ObjectScript

set cube = "HoleFoods" set caltab = "MyCalendarTable"
set file = "/tmp/ cubeExport "_cube_" "_$TRANSLATE($ZDT($h,3)," :","--")_".json"
set sc=##class(%DeepSee.Utils).%AtScaleExportCube(cube,file,caltab)

If no calendar file is used, simply omit the caltab argument from the final command.

Execute the following command to verify that the cube was exported:

ObjectScript

write sc

If the export was successful, this command will return the full file path of the resulting .json file. You will need this path for a later step. You may view this file in your te xt editor or IDE of choice.

4. Log in to your AtScale Design Center and, on the home page, select the Import from InterSystems IRIS Quick Start

option.

5.

In the modal window, click Browse, navigate to the .json cube file observ ed previously, and open it. Back in the primary modal window, click Next.

6. From the Data Warehouse and Schema dropdown menus, select the name of the data warehouse you have configured

for this project and the appropriate schema respectively. Click Next to perform the import.

7.

In the Review Import screen, click Download Report. This report provides details of import performance and recommendations for adjustments to models, if necessary.

8. You may receive warnings on this screen concerning incompatibilities between the structure of the export .json file
and Adaptive Analytics's expected data model. These chiefly concern InterSystems IRIS BI calculated measures and drill-throughs due to use of proprietary MDX operations in InterSystems IRIS BI. InterSystems recommends manually reviewing all calculated measures and drill-throughs and adjust them as needed to ensure compliance with Adaptive Analytics's data model. This review process will be outlined in a later step. Click Next.

Additionally, cubes based on data connectors and cube relationships do not export in this process.

9. Set design-time and run-time permissions according to your needs and click Next to finalize the import process.

10. Review your calculated measures and drill-throughs as follows:

a.

In the AtScale Design Center, navigate to your Adaptive Analytics project.

b. Click on your imported cube to open it in the Main Canvas.

c. Click on the Calculated Measures tool on the Main Canvas.

d. For each Calculated Measure, click Edit and, in the modal window, click Test MDX. Consult the displayed error

messages to determine appropriate adjustments to each MDX definition.

You may now review your imported cube as you would review any other Adaptive Analytics model.

## 4 Integrating Adaptive Analytics with InterSystems Reports

Adaptive Analytics integrates with InterSystems Reports, allowing users to share a common data model—virtual cubes—with other Business Intelligence tools such as Microsoft PowerBI and Tableau. Users can thereby leverage common calculations and definitions across their tool kits.

The following procedure for report generation assumes that you have already completed all the configuration described earlier in this guide, as well as the configuration described in both “InterSystems Reports Designer” and “InterSystems Reports Server with InterSystems IRIS”.

1. Configure the Report Designer to connect to Adaptive Analytics with the Hive Driver:

a. Launch the Report Designer and click on Hive.

b.

c.

In the Create Connection to Hive modal window, select New Catalog. You may set Directory to a path of your
choice; select the catalog you used to create the Dynamic Connection earlier for the Catalog field and click OK.

In the Get JDBC Connection Information modal window, click the Driver checkbox and enter org.apache.hive.JDBC.HiveDriver in the adjacent field. Set the URL to that of your Adaptive Analytics instance, and the User and Password fields to match the administrati ve user of your Adaptive Analytics instance.

d. Click More Options. In the modal window, under the Qualifier tab, select 2-Part Names from the Name Pattern pane

and User Defined from the Quote Qualifier pane, accepting the provided value of ". Click OK.

e. Once the Catalog has been generated, edit the Push Down Group Query field to true. You may now publish reports

based on this catalog as normal with InterSystems Reports.

2. Add a Report User to Adaptive Analytics:

a. Log in to your AtScale Design Center, navigate to Security and click Create User.

b. Enter the desired information for your InterSystems Reports user and, in the Roles pane, select Runtime Query

User. Click Create User.

3. Ensure the Reports Server is configured:

a. On your InterSystems Reports Server instance, log in to the Management Portal as a user with administrative

privileges.

b. Navigate to System Administration > Configuration > InterSystems Reports.

c.

In the table of server definitions, click Configure on the row of the Reports server you wish to connect to Adaptive Analytics. If this server does not exist, follow the configuration instructions in “InterSystems Reports Server with InterSystems IRIS” to create it.

4. Configure the Reports Serv er to access Adaptive Analytics:

a.

In the icon menu, click My Folder.

b. Navigate to Administration > Connections > Dynamic Connections and click New Connection.

c. From the Catalog dropdown menu, select the catalog file you wish to use; if it does not yet e xist, create it following
ve the expected

the instructions in “InterSystems Reports Designer”. Check that the automatically filled fields ha values.

d. Click Add Database User Mapping and, in the autogenerated profile, double-click on the Database User field to edit the name. Replace it with the name of the user you created earlier in the Design Center. Accept the other defaults and click OK..

e.

f.

In the Dynamic Connections list, click on the newly created connection.

In the Properties list, double-click on the name of the connection to edit it to your liking.

g. Navigate to Resources and run the desired report.
