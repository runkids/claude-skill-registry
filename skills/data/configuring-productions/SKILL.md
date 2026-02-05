# Configuring Productions

Introduction to Configuration Tasks

Both developers and system administrators configure productions at v arious times. This page provides some background and an overview of the configuration tasks.

### 1.1 Background for System Administrators

A production is a specialized package of software and documentation that integrates multiple, potentially disparate software systems. A production includes elements that communicate with these external systems, as well as elements that perform processing that is internal to the production.

A production consists of a number of business hosts that communicate with each other (and with external systems). There
are three distinct types of business host:

- A business service receives input from outside the production.

- A business process is responsible for communication and logic that is entirely within the production.

- A business operation usually sends output from the production. Business operations can also be used for communication and logic within a given production.

Within a production, all communication is carried out by means of request and response messages between the business hosts.

InterSystems IRIS® data platform permits only one production to be running in a given namespace at any given time.

A running production continues to run even when you close the Management Portal.

For additional background, see Core Concepts.

### 1.2 Introduction to Settings

A major part of configuration is the task of modifying settings. This section provides an introduction.

Settings are configurable v alues that control the behavior of a production. You can modify these while a production is running and the changes take effect immediately. Settings can affect a production in many ways. For example, a setting
can specify:

- The TCP port on which a business service should listen

- How frequently to check for new input.

- The external data source name (DSN) to use.

- The TLS configuration to use when connecting to an e xternal entity.

- How long to stay connected.

- And so on.

You can specify settings separately for the production and for each business host.

Some settings, such as Actor Pool Size, Pool Size and Reply Code Actions, should be decided as part of the production design and usually should not be changed later. Other settings are dependent on the environment, such as TCP/IP addresses or file paths. It is appropriate to modify these settings if the environment changes.

### 1.3 Possible Configuration Tasks

While you are creating a production, you will need to perform the following tasks:

- Creating the production as a starting place.

- Adding business hosts to the production.

- Configuring settings of the production and of its business hosts.

You might also perform some or all of the following tasks:

- Defining reusable items for use in settings : business partners, credentials, and schedule specifications.

- Defining other options: data lookup tables, system defaults, and source control settings.

- Configuring the Enterprise Message Bank and its clients .

- Creating dashboards to display business metrics.

If you are a system administrator, see Creating and Configuring a Production , Configuring Business Hosts , and Defining Reusable Items for Use in Settings.

### 1.4 See Also

- Introduction to the Production Configuration P age Introduction to the Production
Configuration Page

To create and configure interoperability productions, you use the Production Configuration page, introduced here.

Note:

For information on the legacy Production Configuration page, see Introduction to the Legacy Production Configuration Page.

### 2.1 Displaying the Production Configuration Page

To display the Production Configuration page:

1. Log in to the Management Portal.

2. Switch to the namespace you want to work in.

If you are not already in an interoperability-enabled namespace, choose your working namespace from the available interoperability-enabled namespaces.

3. Click Interoperability > Configure > Production.

4. Click Try the new UI.

Within this new integrated application, the left upper area has buttons that enable you to open the new Production Configuration editor, the Rule Editor, and the Data Transformation Editor, as stacked panels in the same window. Below the buttons,
the left area contains the following collapsible groups, to enable you to select items to view or work on:

- Productions, which lists all the productions in the current namespace. Only one can be selected at a time.

- Production Items, which lists all the business hosts in the currently selected production. This group includes additional subgroups: Inbound Hosts (for business services), Process Hosts (for business processes), and Outbound Hosts (for business operations).

- To search for production items by name, type a name or part of a name into the Filter Items box to filter these lists.

- Rule Sets, which lists all the rule sets in the current namespace.

To search for rule sets by name, type a name or part of a name into the Filter Items box to filter the list. When you select a rule set, the application displays that rule set within the Rule Editor.

Data Transformations, which lists all the data transformations in the current namespace.

Introduction to the Production Configuration Page

To search for data transformations by name, type a name or part of a name into the Filter Items box to filter the list. When you select a transformation, the application displays that transformation within the DTL Editor.

The new Production Configuration page pro vides major new features, including the following:

- Split panel view: While looking at a production, you can open other screens in a separate split panel.

- Enhanced filtering: The search box at the top of the Production Configuration page enables you to search across all business components, including multiple categories, DTLs, and subtransforms.

- Expandable routers: Routers can be expanded to view rules, transformations and connections inline.

- Reworked host connections: Direct and indirect connections are now rendered when a business host is selected, allowing you to see the full path a message can take.

### 2.2 Filtering and Sorting the Display

To filter the b usiness hosts in the production diagram, type a string into the filter box abo ve the diagram:

As you do so, the page displays a drop-down list of items that have names or categories matching the text you entered.

Another option is to click the Filter button at the right side of the filter box. This displays the following options

### 2.3 Hiding or Showing the Settings Pane

Click the Settings icon

to hide or show the production or business host settings on the right side of the page.

Accessing Management Options

### 2.4 Accessing Management Options

The Settings window includes links that provide easy access to management options.

These management tabs are as follows:

- Queue > Go to Queues—Click to view a list of the queues related to this production or business host.

- Log > Go to Event Log—Click to view an abbreviated list of Event Log entries for this production or business host.

- Messages > Go to Message Viewer—Click to display the Message Viewer to see messages processed by this production or business host.

- Jobs > Go to Jobs—Click to view jobs related to this production or business host.

Each of these links opens in a new browser tab with more information; see Managing Productions.

### 2.5 See Also

- Managing Productions

- Monitoring Productions This page describes how to create, open, export, generate documentation for, and delete productions.

Note:

If a production is Suspended or Troubled, see Correcting Production Problem States.

For information on creating and opening productions in the legacy UI, see Creating a Production (Legacy UI).

### 3.1 Creating a Production

To create a production:

1. Display the Production Configuration page.

2.

From the Add item

menu, click Production.

The system displays a dialog box.

3. Enter a Package Name, Production Name, and Description.

4. For Production Type, choose Generic or HL7.

5. Click Create.

6. Now you can add business hosts and configure them .

### 3.2 Opening a Production

To open a production:

1. Display the Production Configuration page.

2.

In the Productions list on the left, click the production you want to open.

### 3.3 Exporting a Production

To export a production:

1. Select Interoperability > List > Productions.

2. Click the row for the production to export.

3. Click Export.

4. Select items to export.

5. Click Export.

6. Select whether you want to export the production to the server or to your local machine via the browser’s downloading

capability.

7.

If you are exporting to the server, enter a path and name of the export file. If you are do wnloading to your local machine via the browser, enter the name of the export file.

8. Click OK.

See Deploying a Production for details on exporting and deploying a production.

### 3.4 Generating Production Documentation

To generate production documentation:

1. Select Interoperability > List > Productions.

2. Click the row for the production to export.

3. Click Document.

This displays a dialog box.

4. Now you can do the following:

- Click View HTML to display the online documentation you previously generated (if applicable).

- Click Generate HTML to create new documentation for this production in HTML form.

- Click Generate PDF to create new documentation for this production in PDF form.

- Click Cancel to cancel the operation.

It may take a considerable amount of time to generate documentation for a large production; therefore, you may not want
to generate new documentation if you have not made changes to the configuration of your production.

You can also generate documentation using the following methods in the Ens.Config.Production class:

- CreateDocumentHTML()—creates new documentation in HTML format.

For example, to create documentation for Demo.Loan.FindRateProduction in HTML format:

ObjectScript

Set
status=##class(Ens.Config.Production).CreateDocumentHTML("Demo.Loan.FindRateProduction",1,.URL,.ErrLog)

Deleting a Production

- RemoveDocumentHTML()—removes existing HTML-format documentation from the current namespace.

- CreateDocumentPDF()—creates new documentation as a PDF file.

For example, to create documentation for Demo.Loan.FindRateProduction in PDF format, you can use the method in
a statement similar to the following:

ObjectScript

Set
status=##class(Ens.Config.Production).CreateDocumentPDF("Demo.Loan.FindRateProduction",1,"C:\Temp\Rate.pdf",.Log)

The PDF format requires that you have a PDF renderer installed. It also requires Java.

### 3.5 Deleting a Production

To delete a production:

1. Navigate to the Interoperability > List > Productions page.

2. Click the production that you want to delete.

3. Click Delete.

4. Click OK.

### 3.6 See Also

- Introduction to the Production Configuration P age

- This topic describes how to add business hosts to a production.

- For information on performing these tasks in the legacy UI, see Modifying Business Hosts (Legacy UI).

- 4.1 Introduction

- A business host is any business service, business process, or business operation within a production. These are also referred to generically as configur ation items.

A configuration item is al ways associated with a specific production. It may resemble or duplicate items in other productions. Each production is an entirely closed universe that does not use configuration items from other productions.

### 4.2 Configuration Names

By default, the name of a configuration item is the name of its underlying host class. Ho wever, you can assign a different name, to describe the purpose of the item, for example.

For example, if you have a business service class that communicates with a specific type of serv er, and you use it to communicate with the same type of server in different enterprise locations, you must configure the b usiness service with different settings to communicate with each enterprise location, even though the type of server is the same. Each different configuration of the business service must have a different name.

The following rules govern configuration names:

- The name must consist of at least one character.

- The name can contain letters, numbers, and any printable character except for the following:

- | ; , : [ < > \ / & "

- Neither the first nor the last character can be an y of the following: ! $ .

- The first character cannot be _ The name (if is it one character long) cannot be *

Important:

You cannot change the name of an existing configuration item. If you require a name change, you can copy the item and delete the original item.

### 4.3 Adding a Business Host to a Production

To add a business host to a production:

1.

Identify (or create and compile) the appropriate business host class.

2. Open the production on the Interoperability > Configure > Production page.

3.

From the Add item

menu, select one of the following:

- Inbound Host creates a new business service.

- Process Host creates a new business process.

- Outbound Host creates a new business operation.

4. Continue as described in the following sections.

This process does not generate any new classes. It updates the production class.

### 4.4 Adding a Business Service

To add a business service to a production:

1. Add a business host, choosing the Inbound Host option.

2. For Inbound Type option, choose one of the following:

- General—Use this to create a business service other than the following types.

- HL7—Use this to create a business service for working with HL7 messages.

- X12—Use this to create a business service for working with X12 messages.

- Business Metric—Use this to create a business service for working with business metrics.

3. Then choose one of the following:

- (General) Inbound Class—Choose an existing class.

- (HL7) Input Type—Choose TCP, File, FTP, HTTP, or SOAP, depending on the form of input data.

- (X12) Input Type—Choose TCP, File, FTP, or SOAP, depending on the form of input data.

4. Name—Specify a name; see Configuration Names .

5.

(HL7 and X12) Specify values for settings as provided in these reference sections:

- Settings for the TCP Inbound Adapter

- Settings for the File Inbound Adapter

- Settings for the FTP Inbound Adapter

- Settings for the HTTP Inbound Adapter

- Settings for the SOAP Inbound Adapter 6.

(Business Metric) Metric Class—Select the business metric class to use.

7.

(Business Metric) Call Interval—Specify how often the business metric will recalculate the values of its properties. The Call Interval is in seconds, starting from a minimum of 0.1 seconds. The default is 5 seconds.

8. Display Category—Specify a category name for use in sorting and organizing items within the production. Category
names are case-sensitive, and space characters are allowed. To place an item in multiple categories, list them in the Display Category field separated by commas (with no spaces around these commas).

Adding a Business Process

9. Comment—Specify an optional text description.

10. Enable Now—Optionally select this to immediately enable the item.

11. Click Create.

Also see Settings in All Business Services.

### 4.5 Adding a Business Process

To add a business process to a production:

1. Add a business host, choosing the Process Host option.

2. For Process Type option, choose one of the following:

- General—Use this to create a business process other than the following types.

- HL7—Use this to create a business process for working with HL7 messages.

- X12—Use this to create a business process for working with X12 messages.

- Component—Use this to create a business process as a component.

3.

(General or Component) Process Class—Choose a base class from the list of valid business process classes. If the class you need does not appear on this list, create and compile the class and then return here to choose it.

4. Name—Specify a name; see Configuration Names .

5.

(HL7 or X12) Specify the following details:

- Auto-Create Rule—Select this check box to create a rule definition name based on the b usiness process class name. When this option is selected, you can use the Rule or Package Name field to specify a package name that will be added to the name of the rule created for the new router. If you do not specify a New Rule Package value, the production’s package is used. In most cases, the Rule or Package Name field is ignored if the Routing Process Name field be gins with a package name. However, if the package specified by the Routing Process Name field is the system package name Ens or Enslib, a rule that is auto-created will have a different package name added to the beginning of the rule name. This additional package is determined by the contents of the New Rule Package field. If the package of the production or routing process is used instead of a specified v class name ends with 'RoutingRule'.

alue, the generated rule

6. Display Category—Specify a category name for use in sorting and organizing items within the production. Category
names are case-sensitive, and space characters are allowed. To place an item in multiple categories, list them in the Display Category field separated by commas (with no spaces around these commas).

7. Comment—Specify an optional text description.

8. Enable Now—Optionally select this to immediately enable the item.

9. Click Create.

Also see Settings in All Business Processes.

### 4.6 Adding a Business Operation

To add a business operation to a production:

1. Add a business host, choosing the Outbound Host option.

2. For Outbound Type option, choose one of the following:

- General—Use this to create a business operation other than the following types.

- HL7—Use this to create a business operation for working with HL7 messages.

- X12—Use this to create a business operation for working with X12 messages.

- Workflow—Use this to create a business service for managing workflo w.

3. Then choose one of the following:

- (General or Workflo w) Outbound Class—Choose an existing class.

- (HL7) Outbound Type—Choose TCP, File, FTP, HTTP, or SOAP, depending on the form of input data.

- (X12) Outbound Type—Choose TCP, File, FTP, or SOAP, depending on the form of input data.

4. Name—Specify a name; see Configuration Names .

5.

(HL7 and X12) Specify values for settings as provided in these reference sections:

- Settings for the TCP Outbound Adapter

- Settings for the File Outbound Adapter

- Settings for the FTP Outbound Adapter

- Settings for the HTTP Outbound Adapter

- Settings for the SOAP Outbound Adapter

6. Display Category—Specify a category name for use in sorting and organizing items within the production. Category
names are case-sensitive, and space characters are allowed. To place an item in multiple categories, list them in the Display Category field separated by commas (with no spaces around these commas).

7. Comment—Specify an optional text description.

8. Enable Now—Optionally select this to immediately enable the item.

9. Click Create.

Also see Settings in All Business Operations.

### 4.7 See Also

- Introduction to the Production Configuration P age

- Modifying Business Hosts

- This page describes how to modify business hosts.

- For information on performing these tasks in the legacy UI, see Modifying Business Hosts (Legacy UI).

- 5.1 Selecting a Business Host To select a business host, click it within the production diagram.

If there are a large number of business hosts, you can do the following to find the b usiness host and select it:

1. Expand the Production Items folder on the left.

2. Optionally type the name of the host (or part of the name) into the filter box and then press Return.

3. Click the name of the item in this area.

This selects the item within the production diagram.

### 5.2 Enabling or Disabling a Business Host

To enable or disable a business host:

1. Select the business host.

2.

menu, select Enable or Disable, as applicable.

Equivalently, select or clear the Enabled checkbox in the Basic Settings group. Then click Save.

### 5.3 Copying a Business Host

To create a copy of a business host within a given production:

1. Select the business host.

2.

menu, select Duplicate.

Modifying Business Hosts

A dialog box prompts you to enter a configuration name.

3. Enter a unique name and click Save.

When first created, the cop y has the same host class and settings as the original; only the name is different. Generally your
next step is to configure the cop y to make it unique. For example:

- If you have an incoming TCP business service that receives messages from a client application, and you want to receive messages from a similar application on a different application server, you can copy the first TCP service and configure the copy with the other server address.

- If you have a business process for one message routing interface, and you want a similar one but with alterations for another interface, you can copy the first routing process and configure the cop y to route messages between different sets of business services and business operations.

- If you have an outgoing email business operation that alerts a user, but you want to alert another user at different times of day, you can copy the first outgoing email operation and configure the cop y with the other email address.

The copy has no relationship to the original item; you can configure, enable, and disable each item independently .

Note:

The Copy command works only within the same production. You cannot copy a business host from one production to another.

### 5.4 Deleting a Business Host

To delete a business host:

1. Select the business host.

2.

menu, select Delete.

3. Click OK to confirm the deletion.

This action does not delete the business host class on which the business host is based.

### 5.5 Viewing Connections

When you select a business host, the production diagram displays lines that show the business hosts from which it receives
messages (if any) and the business hosts to which it sends messages (if any). The following figure sho ws an example:

To display only the business hosts that are connected to the currently selected business host, click Show Connected Hosts

Only

.

Viewing Connections

This topic describes how to configure settings for production and business hosts.

For information on performing these tasks in the legacy UI, see Configuring Settings (Le gacy UI).

### 6.1 Configuring Settings

To configure settings for a b usiness host:

1. Click the business host.

2.

Click the Settings icon

.

3. Expand the Properties group.

4. Within that group, expand and collapse the groups as needed to see the settings.

5. Edit values as needed.

6. Click Save.

InterSystems IRIS® validates the values for settings. If you provide a string value for a setting that requires a numeric value, InterSystems IRIS does not apply that value.

Similarly, to configure settings for the production, first click the production name in the step returns the focus to the production. Then continue as described in the previous steps.

Productions list on the left. This

In both cases, the changes are immediately saved and take effect immediately.

### 6.2 Color Coding

The setting names are color coded as follows:

Color

Black

Green

Source

Setting value comes from the production definition—the value you enter and apply in the configuration page.

Setting value comes from the class definition; it is the default value for the property as defined
in the class.

Blue

Setting value comes from the system defaults table.

### 6.3 Getting Help for Settings

This page provides context-sensitive help. Click the setting name to display the help text in a separate pop-up window.

### 6.4 See Also

- Understanding the Color Coding for Settings

- This topic describes how to configure a production to alert users about important events, such as events that require user intervention.

- 7.1 About Alerts An alert sends notifications to applicable users while a production is running, in the e vent that an alert event occurs. The intention is to alert a system administrator or service technician to the presence of a problem. Alerts may be delivered via email or other mechanism.

The alert mechanism works as follows:

- As part of the development process:

– Within business host classes for the production, the developers include code that generates alerts when applicable.

For information, see Generating Alerts.

–

The developers define an additional b usiness host class called an alert processor (also called an alert target). The alert processor contains the logic to contact each user in the most appropriate way.

The developers might also develop business operations for the alert processor to call.

For information, see Defining Alert Processors.

- You configure the production to include the alert processor , along with any business services that it requires. For details, see the next section.

All alerts also write messages to the Event Log, with the type Alert.

### 7.2 Configuring an Alert Processor

Each time any alert is sent, the alert text is added to the Event Log. This mechanism might be too passive for the most urgent messages. If you want the production to also actively seek the user, you must define and configure a b that has the ability to contact a user device. This business host is known as an alert processor or an alert target.

usiness host

To add the alert processor to the production:

1. Add the business host class to the production. This class is a business operation or business process class, depending

on its implementation.

2. For the configuration name, specify Ens.Alert

3.

If the alert processor has settings such as email addresses and telephone numbers, configure those.

4. Add any business services that the alert processor calls.

Note:

Any production can include no more than one alert processor.

### 7.3 Configuring Alerts on Errors

A production can send alerts automatically whenever a business host encounters an error condition. The Alert On Error setting controls this behavior. If Alert On Error is True, then whenever the business host encounters an error, InterSystems IRIS triggers an alert.

Note that business hosts provide an optional grace period that enables the business host to retry before triggering the alert. Depending on the kind of business host, this grace period is specified by the setting Alert Grace Period or Alert Retry Grace
Period.

### 7.4 Configuring Alerts on Queue Buildups

A production can send alerts when a business host’s queue has too many messages or has messages that have waited too
long. To enable these alerts, specify the following settings with nonzero values:

- Queue Count Alert—When the number of items in the queue exceeds this threshold, an alert is triggered. This alert has the prefix QueueCountAlert: (not localized). This alert is useful in situations where large queues are building up.

- Queue Wait Alert—Length of time that a message can wait in the queue or be the active message before an alert is triggered. This alert has the prefix QueueWaitAlert: (not localized). This alert is useful in situations where a queue is not processing messages.

### 7.5 Other System Alerts

A production generates alerts on other occasions, including the following:

- When a job is marked as dead.

This alert is prefix ed with the non-localized text: DeadJobAlert: for simplified routing and handling.

- When a business host is marked as inactive, according to its Inactivity Timeout setting.

- When a business operation suspends its current message.

### 7.6 See Also

- Generating Alerts

- Defining Alert Processors

- Event Log Defining Reusable Items for Use in
Settings

This topic describes how to define certain reusable items for use as v alues of settings in a production.

You might also need to define TLS configurations. F or information, see InterSystems TLS Guide.

Also see Defining System Def ault Settings.

### 8.1 Defining Business Partners

InterSystems IRIS® data platform provides a way to add additional information to a production to help with the management of a production. A business partner profile is information about an or ganization or application connected to your InterSystems IRIS system. For each business partner, you can provide information such as the partner name, notes, primary and alternative contacts, and contact details. Defining a profile has no ef fect on the behavior or running of the production. It simply gives you a means to store more information.

For example, suppose your production talks to ABC Hospital and XYZ Hospital. You can enter profiles for both of these along with contact information. When you configure items that talk to these or ganizations, you can specify the defined Partner Name for each business host.

The Interoperability > Configure > Business Partners page allows you to view and edit profiles to store information about your business partners for use in your productions.

The page lists any Business Partner Profiles you ha ve already defined and allo ws you to enter a new profile or edit an existing one in the right pane of the page.

Enter the required unique Partner Name and optional Description and then the following information for a Primary Contact
and Alternate Contact:

- Name

- Title

- Email address

- Phone Number

- Mobile Phone Number

- Notes Defining Reusable Items for Use in Settings Click Save to store this information in the current namespace. When you are configuring productions, this names appears in the Business Partner configuration setting list, which you can choose to use in your production enabling you to cate gorize business host items in your production by business partner.

To delete a specific b usiness partner profile, select it from the list so it appears in the right pane and then click Remove.

### 8.2 Defining Credentials

Some remote systems require a username and password to log in to that system. A username-password pair is a login cre-
dential. InterSystems IRIS permits you to store login credentials in a centralized, secure table for use by productions; these
are known as production credentials. Only users with appropriate access to the Management Portal can view and edit this table.

The Interoperability > Configure > Credentials page displays the Credentials table for the current namespace.

Each entry in the Credentials table has an ID which you use as the value of the Credentials setting when configuring b usiness services or business operations for the production. Adding an entry to the Credentials table for a production consists of assigning an ID to a username-password pair. You can also store an informational business partner name with the credential.

The Credentials page displays a list of defined credentials associated with the current namespace. Each ro w in the table has
the following columns:

- ID—Unique string that identifies this username-passw ord pair; the name you use in the Credentials setting when con-
figuring a b usiness service or business operation to establish a remote connection.

- User name—Username with which to log on to the remote system.

- Password—Password corresponding to the logon username.

- Business Partner (Optional)—Name of the business partner profile associated with this item.

When editing, you can choose a profile from the list and vie w its details by clicking the magnifying glass. You can also create or edit a profile by clicking the Business Partners Configuration Page link.

When you select a Credential row, the right pane displays the current settings. If you do not select a row, the right pane shows empty fields for you to create a ne w credential. Enter values in the fields as outlined in the table description. You
have the choice of two actions to perform in the Credentials Viewer:

- Click Save to store the updated or new values as a credential and display it in the table.

- If you choose to edit a row and change the ID, when you click Save, you must verify that you want to rename the credential.

Click Remove to delete the selected credential.

CAUTION: You cannot undo the Remove operation.

### 8.3 Defining Schedule Specifications

The default scheduling for business hosts is for them to run whenever the production is running. However, a finer control is possible. Not only can you enable and disable business hosts, but the Interoperability > Configure > Production page also provides a Schedule setting for each business host. This is an optional command string that schedules the item to be stopped

Defining Schedule Specifications

and started at specific times and on specific days of the week, month, or year
the scheduler starts it; when it is time to stop, if the item is running, the scheduler stops it.

. When it is time to start, if the item is enabled,

The Interoperability > Configure > Schedule Specs page aids you in creating a string to use in this configuration setting. Once you create a schedule string and give it a name, you can use this string as a value for the Schedule configuration setting.

#### 8.3.1 Schedule Specifications

The Schedule string is a comma-separated list of event specifications. Each e vent specification has the follo wing format:

action:YYYY-MM-DDThh:mm:ss

Where each item in the event specification, from left to right, has the described v alues:

Item

action

:

Possible Values

START or STOP indicates the desired action

Required separator

YYYY-MM-DD

Either:

- YYYY is the year as 4 numerals

- MM is the month as 2 numerals DD is the day of the month as 2 numerals Any of these fields may be the single character * (asterisk) indicating all years, all months, or all days

- Or:

- YYYY is the word WEEK

- MM is the specific occurrence of the day of the week (indicated by DD) in the month (01 = first occurrence of the specific day of the week in the month, 02 = second occurrence in the month, etc.)

- DD is a specific day of the week (00 = Sunday, 01 = Monday, etc.)

- MM may be * for all occurrences and DD may be * for all days Once a field is specified as *, all fields to the left of it are also assumed to be *. Thus, if the DD value is *, the MM value is treated as * even if it has a specific numeric value. Similarly, if MM is *, YYYY is treated as *.

T

Required separator

hh:mm:ss

Hour, minute, and second

,

Use the comma separator only if there is another event specification after the current one. Do not use it at the end of the Schedule string.

If you set a schedule specification to be deplo yable, then the specification can be included when you e xport the production. When you are exporting the production, select Deployable Settings and select the Ens.Util.Schedule setting.

See Ens.ScheduleHandler for more information.

The following sections provide examples, details on Daylight Saving Time considerations, and the intended use and limitations of the setting.

Defining Reusable Items for Use in Settings

#### 8.3.2 Examples

If your schedule contains recurring events, the Schedule setting requires both START and STOP actions. If your schedule setting is an absolute one time event, then you need only use the appropriate single START or STOP action. In most cases, Schedule strings should contain both a START and a STOP action.

Some examples of Schedule strings follow:

- Start the business host every day at 8 a.m. and stop it every day at 5 p.m.

- START:*-*-*T08:00:00,STOP:*-*-*T17:00:00

- Stop every year on January 2 at 7 a.m. and start again on January 3 at 7 a.m.

- STOP:*-01–02T07:00:00,START:*-01-03T07:00:00

- Start every month on the second day of the month at 8 a.m. and stop every month on the tenth day of the month at 8:30 p.m.

- START:*-*-02T08:00:00,STOP:*-*-10T20:30:00

- Stop every Sunday at 10 a.m. and start every Monday at 8:30 a.m.

- STOP:WEEK-*-00T10:00:00,START:WEEK-*-01T08:30:00 Start every third Tuesday at 9 a.m. and stop every third Friday at 4 p.m.

START:WEEK-03-02T09:00:00,STOP:WEEK-03-05T16:00:00

Stop on December 31, 2010 just before midnight.

STOP:2010-12-31T23:59:59

Start on January 3, 2011 at 6:45 a.m.

START:2011-01-03T06:45:00

The following two strings are equivalent: Start every day at 2 a.m.

START:*-*-*T02:00:00
START:WEEK-*-*T02:00:00

#### 8.3.3 Scheduling and Daylight Saving Time

When daylight saving time (DST) begins, clocks skip an hour that day, usually from 2:00 a.m. to 3:00 a.m. Any item you have scheduled that falls into that nonexisting hour takes place at the beginning (which is also the end) of that hour. For example, on the day DST begins, an event scheduled to take place at 2:15 a.m. takes place at 2:00 a.m. (which is also 3:00 a.m.).

When DST ends, an hour of the day repeats, usually from 1:00 a.m. to 2:00 a.m. Any item you have scheduled that falls in that repeated hour takes place only once. Whether the event takes place on the first occurrence of the scheduled time or the second occurrence in the repeated hour depends on the operating system, but it only takes place once. For example, on a Windows system on the day DST ends, an event scheduled to take place at 1:15 a.m. takes place at the second occurrence of 1:15 a.m.

#### 8.3.4 Intended Use and Limitations

The Schedule setting starts and stops production business hosts according to a schedule; it is not a task scheduler. The
schedule string defines a square w ave in time declaring during what time intervals the item should be running, in between which it should be not be running. InterSystems IRIS cannot prevent scheduled transitions from being interrupted or superseded by other production events.

The scheduler wakes up periodically (it sets its own alarm clock for when any scheduled item next expects a transition) and attempts to start or stop any items that are not currently in the expected state according to their schedule strings. It runs the UpdateProduction() method of the Ens.ScheduleHandler class and checks what event it needs to schedule next.

There are two general classes of things that can prevent transitions from taking place as the schedule string indicates:

- The scheduler might be unable to cause the intended state change; that is, the UpdateProduction() method fails to
affect the relevant items.

- For example, an item could be in a Read timeout or some other busy state that lasts longer than the Update timeout. Another example is a business host the scheduler starts cannot be stopped by the scheduler if the item is in the middle of a synchronous call. The business host must wait for a response to the call before the scheduler stops it.

The scheduler might not be able to wake up at the intended time. Examples of conditions that could cause this: the CPU is busy, a queue builds up of the alarm clock messages for the scheduler, the scheduler is itself disabled or crashed, the production is down, etc. The scheduler is not guaranteed to wake up during any particular interval, and when it does wake up it only looks at the intended state for the current moment, not at any history of when it should have woken up.

Use of the schedule setting is not intended or designed as an event signaling device. It is intended to accommodate planned outages and scheduled intervals of activity or inactivity. If you have events that you must trigger at a particular time or as
soon as possible thereafter, InterSystems IRIS provides better alternatives:

- You can configure your b usiness service to use an inbound adapter with the implemented OnTask() method where you call the business service. InterSystems IRIS provides classes for many types of inbound adapters. See Ens.InboundAdapter and the books in the Application Development: Using Adapters and Gateways in Productions set for details.

- If you do not want to use an adapter, you can call the business service programmatically and schedule it to run using the System Operations > Task Manager page in the Management Portal. This gives you finer control in situations such as the system being down at 1:00 a.m.

The recommended approach is to configure the b usiness service with Pool Size = 0 and then use the Task Manager to launch a task that calls CreateBusinessService() on it and invokes ProcessInput() on the resulting service instance object. The advantage of calling a business service this way is that you call it at the time you want and it runs only once. If InterSystems IRIS happens to be down at that time, your task can register an error. See the following sections
for details:

– Using the Task Manager

–

Invoking a Business Service Directly

### 8.4 See Also

- This page describes how to define data lookup tables to support the Lookup() and Exists() utility functions.

### 9.1 Editing a Lookup Table

The Lookup Tables portal page allows you to create and configure data tables to support the Lookup() and Exists() utility functions. The Lookup() utility function is provided so that you can easily perform a table lookup from a business rule or DTL data transformation. To avoid possible complications when exporting a lookup table, it is recommended that you avoid using special characters when naming the lookup table. As an exception, it is safe to use periods (.) in the name.

The Lookup() function works only after you have created a lookup table and have populated it with data. You can do this selecting Interoperability, Configure, and Data Lookup Tables. If you click Open, a dialog box lists the lookup tables that
are defined in the namespace. Select a lookup table and InterSystems IRIS® displays the follo wing form:

To edit entries in a lookup table, you can:

- Delete an entry by selecting the red X icon. The entry is deleted when you save the table. Until you have saved the table, you can restore the entry by selecting the green + icon that is displayed to the left of the entry.

- Update an entry by entering the same key as the entry and a new value in the form on the right and then selecting Apply. After you update the value, the original value is displayed in the Original Value column until you save the lookup table. Selecting an existing entry populates the form on the right with the entry’s current values.

- Add a new entry by entering a new key and its value in the form on the right and selecting Apply.

- Undo the previous action by selecting the curved arrow in the menu bar.

Note:

Selecting an entry has only one effect: initializing the values in the form on the right. Selecting Apply acts on the entry specified in the Key field not on the selected entry . If the key field matches an e xisting entry, that entry is updated. If the key field does not match an e xisting entry, then a new entry is added. Selecting the green + icon on the menu bar or selecting Discard clears the form but does not have any other effect.

You can take an action by selecting one of the following buttons:

- New—Displays a form so that you can name the lookup table and then displays the empty table. Add entries to the table by entering in key and value pairs and selecting Apply for each pair. You must select Save to make the lookup table permanent.

- Open—Displays the lookup tables defined in the current namespace and allo ws you to select one.

- Save—Saves the current lookup table with any edits that you have applied. Clears the Original Value column and removes deleted records.

- Save As—Saves the current table entries to a new table. Specify the new table name and select OK. Clears the Original Value column and removes deleted records.

- Delete—Deletes the current table. If you have made any edits to the table since opening it, InterSystems IRIS asks if you want to leave the page. To delete the table, select Leave Page. If you select Stay on Page, InterSystems IRIS treats the current table as if it were a new table.

- There are two ways to import lookup tables: Import Legacy and Import . An important difference between them is that when you are importing a lookup table with the same name as an existing lookup table, Import Legacy merges the existing table with the data from the file and Import replaces the existing lookup table with the data from the file.

–

–

Import Legacy—Imports the lookup tables defined in the file. If an imported lookup table has the same name as an existing table, the values are merged. If a key is defined in the file, it o in the lookup table.

verwrites any existing value of that key

Import—Adds new lookup tables that are defined in an XML file. If an y of the new tables have the same name as an existing table, the new table replaces the old one. Select Browse to specify an XML file, then select Open. The form displays the LookUp Table (LUT) document or documents defined in the file. You can select all of the lookup tables or some of the lookup tables listed, then select Import to import the lookup table(s). The Import button can only import the new file format (see follo wing note).

Note:

There are two lookup table file formats: a ne w format and the legacy format. The new format contains additional XML Document tags. Import Legacy can handle both the new and the legacy format, but Import can only handle the new format. The new format is exported by Studio and by the Export portal button. The old format is exported by the Ens.Util.LookupTable.%Export() method. See Lookup Table File Format for a description of the lookup table file formats.

- Export—Exports the current table to an XML file. Although you can specify the name of the file, the lookup table exported has the same name as the current lookup table and does not use the file name. You can export only using the
current XML format; you cannot export the legacy XML format with this release.

If you used special characters when naming the lookup table, you may encounter issues when exporting the table. As a workaround, you can export the entire ^Ens.LookupTable global rather than an individual table. For details, see Exporting Globals. Alternatively, you can export the global subscript that corresponds to the name of a lookup table.
For example, to export the lookup table My/Lookup/Table, call:

set st = $SYSTEM.OBJ.Export("Ens.LookupTable(""My/Lookup/Table"").GBL","filename.xml")

CAUTION: You cannot undo the Delete, Import, or Import Legacy operation.

Note:

If there is an existing lookup table with the same name, the Import button has a different behavior from the Import Legacy button. The Import button completely replaces the contents of the existing lookup table. In contrast, the Import Legacy button merges the new values with the existing values.

For information on working with lookup tables in programs, see Programmatically Working with Lookup Tables.

Lookup Table File Format

### 9.2 Lookup Table File Format

There are two XML formats that describe lookup tables: the new format and the legacy format.

The new Lookup Table XML format consists of one or more XML Document elements, for example:

<?xml version="1.0" encoding="UTF-8"?>
<Export
ts="2014-10-21 11:52:51">
<Document name="AlertTable.LUT">
<lookupTable> <entry table="AlertTable" key="BadMessageHandler">temp_1@company.test</entry> <entry table="AlertTable" key="Extra_Observations">temp_5@company.test</entry> <entry table="AlertTable" key="MsgRouter">temp_3@home.test</entry> <entry table="AlertTable" key="Priority_FileOperation">temp_5@home.test</entry> <entry table="AlertTable" key="Regular_FileOperation">temp_4@company.test</entry> </lookupTable>
</Document>
</Export>

The XML elements have the following syntax:

- Each Document element must has a name attribute that specifies the lookup table name and has a file type .LUT .

- Each Document element contains one lookupTable element.

- Each lookupTable element contains a list of entry elements.

- Each entry element has a table attribute that specifies the same table name as specified in the Document name, specifies a key attribute, and specifies the v alue of the entry as text.

The legacy format exported by the Ens.Util.LookupTable.%Export() method does not have the Document element. It consists of just a single lookupTable element and the entry elements that it contains. It can contain entries for multiple lookup tables by specifying different names in the table element.

### 9.3 Importing Flat Files as Data Lookup Tables

You can import a flat file as a data lookup table, if the file is as follo

ws:

- It can include a header row.

- It must include three values, separated by spaces, commas, tabs, or another delimiter.

- From left to right, the three values must correspond to the Value column of a lookup table, the Key value of a lookup table, and the desired name of the lookup table.

To import such a file as a lookup table, use the Data Import Wizard, as described in Importing Data from a Text File. For the schema name, use Ens_Util. For the table name, use LookupTable.

### 9.4 See Also

- Utility Functions for Use in Productions

- Programmatically Working with Lookup Tables Defining System Default Settings This page discusses system default settings for productions and how to define them.

### 10.1 Introduction to System Default Settings

The purpose of system default settings is to simplify the process of copying a production definition from one en vironment
to another. In any production, the values of some settings are determined as part of the production design; these settings
should usually be the same in all environments. Other settings, however, must be adjusted to the environment; these settings
include file paths, port numbers, and so on.

System default settings should specify only the values that are specific to the en vironment where InterSystems IRIS® data platform is installed. In contrast, the production definition should specify the v alues for settings that should be the same in all environments. System default settings are stored in the system defaults table, which is independent of any production.

System default settings are specific to the namespace in which the y are defined. They can be applied to all productions, business hosts, and business host classes or a subset of these. InterSystems IRIS uses the most specific match for that setting name. For example, you could create a system default setting for all business hosts within a single production or for a single business host in all productions. You can define a system def ault for setting A (value A1) for all productions and also define a system default for setting A for a single business host (value A2). If you do so, A1 is the default everywhere except for that business host (which uses the default A2).

Release 2023.3 introduced a special kind of system default setting, namely a system override. These are possible for a specific group of settings by name . If these settings have values within the system defaults table, those values take precedence over the value specified within the production definition. InterSystems IRIS uses the most specific match for that setting name within the system defaults table.

Overall, to find the v alue for a setting, InterSystems IRIS checks as follows:

1.

It checks whether this specific setting can be a system override. If so, and if the system defaults table contains a value (even an empty string) for the setting, InterSystems IRIS uses that value and stops further checking.

2. Otherwise, it checks whether the production definition pro vides a value (even an empty string). If so, InterSystems

IRIS uses the value provided by the most specific match for that setting and stops further checking.

3. Otherwise, it checks whether the system defaults table provides a value (even an empty string). If so, InterSystems

IRIS uses the value provided by the most specific match for that setting and stops further checking.

4. Finally, if it hasn’t found a value elsewhere, it uses the value of the setting as specified in the applicable class definition,

if there is a default.

The production configuration page uses color-coding for the settings to indicate how the values are set.

Defining System Default Settings

### 10.2 Settings That Can Act As System Overrides

For productions, the settings that can act as system overrides are as follows:

- ActorPoolSize

- TestingEnabled

For business hosts, the settings that can act as system overrides are as follows:

- Enabled

- PoolSize If you define v alues for these settings within the system defaults table, those values take precedence and cannot be modified within a production. Additionally, any productions in the given namespace are automatically updated to use the override values.

### 10.3 Displaying the System Default Settings

To access the System Default Settings page, select Interoperability > Configure > System Default Settings. This page displays the system defaults table for the current namespace.

Here you can do the following:

- Create a new system default setting. To do so, click New. Then see creating or editing a system default setting.

- Edit an existing setting. To do so, select the setting and click Edit. Then see creating or editing a system default setting.

- Delete a setting. To do so, select the setting and click Delete.

Note:

Security privileges may restrict you from creating, editing, or deleting some of the system default settings. See Security for System Default Settings.

### 10.4 Creating or Editing a System Default Setting

If you are creating a new setting or editing an existing one, InterSystems IRIS displays a page where you enter or edit the
following information:

- Production—Optionally specifies the production to which this def ault applies. If set to *, this default applies to all productions in the namespace.

- Item Name—Optionally specifies the b usiness host to which this default applies. If set to *, this default applies to all hosts in the production or in all productions.

- Host Class Name—Optionally specifies the class of the b usiness host to which this default applies. If set to *, this default applies to all hosts in the production or in all productions.

- Setting Name—Specifies the name of the property to set. Note that property names do not include spaces. In most cases, the property name is similar to the setting name, with the spaces removed. For example, the setting Log Trace Events is based on a property called LogTraceEvents.

Using System Default Settings

Tip: You can see the property name within the popup window that displays descriptive text for the setting.

- Setting Value—Specifies the v alue to assign to the property. If this field is blank; it sets the def ault to an empty string.

- Description—Optionally specifies a description of the def ault.

- Deployable—If set, the setting can be deployed to another production. For more information about deployment, see Deploying a Production.

The page also displays a tree of productions and other classes. This allows you to find e xisting settings and drag the names and values to the form. The Expand Tree and Contract Tree buttons and the plus and minus icons allow you to explore the tree to locate the property you are seeking.

While you can use an asterisk (*) in the Production, Item Name, and Host Class Name fields to apply a setting to all the productions in a namespace, you cannot use other wildcard input such as EnsLib*. Additionally, you can specify only one value in each of these fields.

Note:

Your security privileges determine which system default settings appear in the tree. For information about these security privileges, see Security for System Default Settings.

When you have completed defining or updating the setting, click Save. The Cancel button discards any changes and returns to the list of settings without creating or updating a setting. The Restore button returns to fields to their initial v alues and allows you to edit the values.

### 10.5 Using System Default Settings

When using a wizard to create the business service or operation, use the Default applies if no value check box to specify that you want to use system default settings when available. This option is selected by default.

Without the Default applies if no value option, the business host is created with blank values, not the system defaults.

### 10.6 See Also

- Security for System Default Settings

- Understanding the Color Coding for Settings

- (which are more general settings)

- This page describes a small number of settings that apply either to the entire instance or to an entire namespace.

### 11.1 Configuring Settings in the Portal

The Management Portal lets you configure some of these settings, as follo ws:

1. Select Interoperability > Manage > Configuration > Interoperability Settings.

2.

If you want to set a namespace-specific setting, change to that namespace.

3. For the setting you want to change, select or clear the check box as needed.

4. Click Apply.

The namespace-specific settings are as follo ws:

- Exclude Production Configuration Page from Source Control—If this setting is selected, then the page Interoperability > Configure > Production does not provide source control options, even if the namespace otherwise is under source control.

- Disable Inactivity Timeout for Interoperability Pages—If this setting is selected, then the pages within the Interoperability menu will not time out due to inactivity.

- Enable Journalling of deleted data values when purging—If this setting is selected, then InterSystems IRIS does not
write the old values to the journal file, when pur ging data; in this case, the journal file contains only the ne w values,
and it is not possible to roll back the changes. If this setting is cleared, then the journal file includes both the ne w and the old values, as usual.

There is also a setting that applies to all namespaces:

- Permit Enabling Automatic Refresh of Management Portal Pages—If this setting is selected, the Management Portal pages are automatically refreshed (so that they display any new information available from the server).

### 11.2 Configuring Source Control Settings

You can configure source control settings for each interoperability-enabled namespace. F or information on this, see Integrating InterSystems IRIS with Source Control Systems. In addition, there is a flag to indicate whether the source control
system requires a project context to be supplied to work correctly. The flag is acti vated as follows:

Set ^%SYS("Ensemble","SourceControl", $namespace, "ProjectContext") = 1

Also, existing user templates used as dialog windows in Studio must include the Ens_SourceControl.js in /csp/broker/ensemble/ (which can be referenced by the path ensemble/Ens_SourceControl.js) to manage your browser-based interactions. This inclusion is required for any web pages. Depending on the context required by your source control hooks, you may need to add some extra data to certain returns.

#### 11.2.1 Portal Pages Affected by Source Control

When source control is in use, source control buttons appear on the following pages:

- Interoperability > Configure > Production

Note:

If a production is under source control and you do not have it checked out for update, you cannot modify the production definition. You can temporarily Stop, Start, and Restart business hosts by using the buttons on the Action tab. These buttons temporarily stop or start the host but do not modify the production definition. A business host can only be temporarily stopped if it has a pool size greater than 1 or in the case of Business Processes and Business Operations are invoked Queue and not InProc.

However, you can exclude this page from source control; see Configuring Settings in the Portal

.

- Interoperability > Configure > Business Partners

- Interoperability > Configure > Schedule Specs

- Interoperability > Configure > Data Lookup Tables Tables

- Interoperability > Build > Business Processes

- Interoperability > Build > Data Transformations

- Interoperability > Build > Business Rules

- Interoperability > Build > Record Maps

- Interoperability > Build > Complex Record Mapper

- Interoperability > Manage > Workflow > Roles

- Interoperability > Manage > Workflow > Users

### 11.3 See Also

Settings Applicable to Data Purges

Integrating InterSystems IRIS with Source Control Systems

- Configuring a Mirror Virtual IP as the
Network Interface

- If you set up a mirror virtual IP (VIP) in your environment, you can optionally specify the VIP as the destination for connections from some production components. Specifically , you can use the VIP for outgoing connections when the production component has a Local Interface setting. For example, TCP adapters have a Local Interface setting, which you can set to the
VIP.

- Configuring the Enterprise Message Bank and Its Clients The Enterprise Message Bank is an optional remote archiving facility where you can collect messages, Event Log items, and search table entries from multiple InterSystems IRIS® data platform client productions. This topic describes how to configure the Message Bank and its client systems.

### 13.1 Configuring the Message Bank

After defining the Enterprise Message Bank production, you may need to perform additional configuration, described here.

Specifically , the Ens.Enterprise.MsgBank.TCPService component on the Message Bank server helps process the incoming messages from the Message Bank client productions. If you have configured enterprise systems, the TCPService uses the information that you defined to associate the incoming message with the enterprise system. See Identifying Enterprise Systems for Viewing and Monitoring for details on configuring enterprise systems. If you do not identify the enterprise system, the monitor service identifies the incoming message based on the elements of the message.

There are two cases where there may be conflicting information to identify the enterprise system sending the message:

1.

If the enterprise system has multiple IP addresses and the system restarts it may be sending messages from a different IP address. To instruct the Message Bank to recognize that these messages are coming from the same enterprise system as the earlier messages, select the Ignore Client IP Changes check box on the Ens.Enterprise.MsgBank.TCPService.

2. Although it is not a recommended configuration, it is possible to terminate an enterprise system and restart a ne w one

with the exact same configuration and name b ut resetting the message IDs. Since the message IDs are not related to the ones in the messages sent by the previous enterprise system, the Message Bank should treat it as a new enterprise system. In this case you should clear the Ignore Client IP Changes check box on the Ens.Enterprise.MsgBank.TCPService.

The Ignore Client IP Changes check box does not affect how the Message Bank treats enterprise systems that are part of an InterSystems IRIS mirror set (see Mirroring Architecture and Planning).

Configuring the Enterprise Message Bank and Its Clients

### 13.2 Configuring the Message Bank Link on a Client System

You can configure each applicable client system to include a con venient link to the Message Bank, for easier access. This link does not affect the flo w of messages.

To configure this link on a client system:

1. Display the Interoperability > Configure > Message Bank Link page for the applicable namespace.

2. On this page, provide the following information so the InterSystems IRIS® can connect to the Message Bank (if

defined):

- Web Server IP Address—Specify the IP address of the machine on which the Message Bank is running.

- Web Server Port Number—Specify the port number used by the web server that is configured for use with Inter - Systems IRIS on that machine.

- Instance Prefix—Specify the path for the instance of InterSystems IRIS on the web server. This is required if you are using HealthShare Health Connect as the target Message Bank. Also, if you are using a different web server, potentially with other instances of InterSystems IRIS using the same web server, you must specify this prefix so that the Message Bank can construct URLs that connect with the correct InterSystems IRIS instance through the web server.

- Message Bank Production Namespace—Specify the InterSystems IRIS namespace in which the Message Bank production is running.

- Use SSL To Connect To The Message Bank Web Server—Select this to use TLS to connect to the Message Bank.

### 13.3 Configuring a Client Production to Send Messages

You must configure each desired client production to send messages to the Message Bank. F or each client production,
perform the following configuration steps:

1. Add the specialized message bank operation (Ens.Enterprise.MsgBankOperation) to the production and configure it as

needed.

Note:

For this business host, Operation Name must be the Message Bank operation class name. Either leave this blank to use the default class name or enter Ens.Enterprise.MsgBankOperation.

See the following subsection for configuration details.

2.

If you have not yet done so, configure the link to the Message Bank, as described in the previous section.

Or navigate to the Interoperability > View > Enterprise Message Bank page. The first time you enter the Enterprise Message Bank page, InterSystems IRIS prompts you for information to define the link. This information is the same as described earlier.

Now the production is configured to send messages to the Message Bank.

Configuring a Client Production to Send Messages

Important: While the Enterprise Message Bank can receive messages without having the sending production listed as an enterprise system, it cannot resend messages without access to the credentials. Identifying Enterprise Systems for Viewing and Monitoring has instructions on enabling access to productions, so that messages can be resent.

#### 13.3.1 Configuring a Message Bank Business Operation

Configure the follo wing settings specifically for the Message Bank:

Enable Archiving

Set to True. This starts messages queuing from all business hosts in the client production. Note that this queueing continues even if you disable the operation and while it is not able to connect to the Message Bank. The operation forwards any queued messages to the Message Bank server whenever it is enabled.

If set to False, the operation does not queue any messages for the Message Bank.

IP Address

IP address of the Message Bank production. Note that this does not include the web server port number.

Port

TCP port number used by the Message Bank production input service (9192 is the default).

Optionally configure the follo wing additional settings:

Archive Items

Controls which messages to send to the Message Bank. The default behavior is to archive everything except
scheduler messages as shown by the value:

*[*],-Ens.ScheduleService[*],-Ens.ScheduleHandler[*]

See the following subsection.

Event Log Interval

How frequently should we check for conforming Event Log events that may need to be forwarded to the Message Bank server. 0 means check only when messages are being forwarded.

Force Keepalives

If set to True, send empty event submissions periodically if no conforming events need to be submitted.

MyForceIPAddr

IP address to report to the Message Bank server. If you do not specify a value, the business operation queries the local system and reports the local IP address.

You may choose to specify an IP address for several reasons:

- The client machine is a member of a cluster with a common cluster IP address. If you specify the cluster IP address, the Message Bank server responds to the cluster rather than to the client machine.

- The client machine is multi-homed and associated with more than one local IP address. In this situation, you can specify which local IP address the business operation reports to the Message Bank server. Doing so prevents the Message Bank server from generating multiple Node Id values for the client machine.

Configuring the Enterprise Message Bank and Its Clients

You can modify the MyForceIPAddr setting only from the ObjectScript shell by defining the MyForceIPAddr node
of the ^Ens.MsgBank global, for example:

set ^Ens.MsgBank("MyForceIPAddr") = "192.0.2.23"

Specifying the MyForceIPAddr setting may prevent the Message Bank server from automatically recognizing that a client has been upgraded or otherwise modified. Additionally, the setting may prevent the Message Bank from generating new Node Id values for client machines that report the same Node Id value. If multiple client machines contribute messages under the same Node Id, message ID collisions in the Message Bank repository may occur.

For information on other settings, see the following:

- Settings in All Productions.

- Reference for TCP Adapter Settings. (The Ens.Enterprise.MsgBankOperation class uses a TCP adapter and thus inherits settings from it.)

#### 13.3.2 Details for the Archive Items Setting

The Archive Items setting controls which messages the production sends to the Message Bank. It is a comma-separated list of configuration names of items whose messages are to be archi ved to the Message Bank server.

Archive log events for each item using the following colon-separated syntax:

item[evtype1:evtype2:Trace_cat]

Within the event type brackets, you can use the following characters in your selection list:

Pattern
character

Placement

Resulting action

include all event types

at the front of an item

exclude the type from archiving entirely

at the end of an item

exclude message bodies from archiving

at the end of an item

exclude search table entries from archiving

at the end of an item

exclude message headers from archiving

for events of type Trace

optionally used to select a particular category of trace event. Event type Trace without a suffix means Trace events of all categories.

*

-

!

$

-

_

For example:

- *[*]—Archive everything

- *$[*],Ens.Alert![-*]—Archive all events, headers, and bodies but not SearchTable entries; but do not archive
bodies or events from item Ens.Alert.

Note:

InterSystems IRIS only archives trace events if it has logged them. You can use these settings only to restrict which logged events get archived, not to archive any events that you did not configure to be logged.

### 13.4 See Also

- Defining an Enterprise Message Bank

- Identifying Enterprise Systems for Viewing and Monitoring (describes how to configure enterprise systems so that you can resend messages from the Message Bank)

- Using the Enterprise Message Bank Identifying Enterprise Systems for Viewing and Monitoring On systems with the Enterprise Message Bank, Enterprise Message Viewer, or Enterprise Monitor, you should identify the productions that you are monitoring or whose messages you are viewing. Also, when you are using the Enterprise Message Bank, you must configure the client systems so that they permit access to the monitoring code.

### 14.1 Configuration on Message Bank Server or Enterprise Message Viewer

The client productions—the productions being monitored or sending to the Message Bank, are called Enterprise Systems.

When you identify a production you specify its system address and the credentials needed to access it. To use the Enterprise Message Viewer or Enterprise Monitor for a production you must identify the production in the Enterprise System list. Although the Enterprise Message Bank can receive messages without having the sending production listed as an enterprise system, it cannot resend messages without access to the credentials. Although you can monitor messages on the Message Bank without configuring the enterprise systems, you should configure an enterprise system for e very production sending messages to the Message Bank.

To enable access to the productions, do the following in the Management Portal on the Message Bank Server or on the
system with the Enterprise Message Viewer:

1. Create production credentials that have an InterSystems IRIS® username and password for a user that has sufficient

privileges to access the production.

For information, see Defining Credentials .

2.

If needed, create a TLS configuration to connect to this client production.

For information, see InterSystems TLS Guide.

3. Navigate to the Interoperability > Configure > Enterprise Systems page. InterSystems IRIS then displays the list of

systems that are currently defined.

Identifying Enterprise Systems for Viewing and Monitoring

4. Click the New Connection

The page then displays an editing area.

5. Enter the following information:

- Name—A convenient short name for this client production. You must specify a value if you want to resend messages to this production.

- Web IP Address—The server IP address and the web server port used by InterSystems IRIS on that server (separated by a colon). For example: enserver1:80 Namespace—Namespace in which the client production is running.

Queue Threshold—The threshold for queues for the Enterprise Monitor.

Service Web Application Path—The URL path to the client’s web application for the service %CSP.Monitor.Server. The URL path must end with / and should not include http(s)://. Leave blank to use the default /csp/namespace/. For HealthShare, an example could be /csp/healthshare/namespace/services/.

SOAP Credentials—Credentials to use for accessing the system. Select the production credentials created in step 1.

SSL Configuration—TLS configuration to use for vie wing messages with the Enterprise Message Viewer or for resending messages from the Enterprise Message Bank.

- 6. Click Save.

- 7. To edit or delete an existing entry, select edit or delete.

- Note:

- If you are using the Enterprise Message Bank, when the bank receives a message from a new namespace, it creates an entry for that system. You can edit this entry to add a name, the SOAP credentials, and the TLS configuration so that you can resend messages to this system.

- 14.2 Enabling Monitoring on Client Systems When you are using the Enterprise Message Bank, you must enable monitoring on the client systems. To do so, create a
class access rule for the application specified in the Service Web Application Path with the following settings:

Type: AllowPrefix

Class name: %CSP.Monitor.

- Allow access: True (box selected)

- Add this same access to ALL applications: False (box cleared)

- Be sure to include the trailing period in the Class name as shown.

- Enabling Monitoring on Client Systems This section provides reference information on settings that are present in all productions and all business hosts.

Provides reference information for settings that are available in all productions.

Summary
All productions have the following settings:

Group

Settings

Description

Shutdown Timeout, Update Timeout

Development and Debugging

Testing Enabled, Log General Trace Events

Number of system jobs available in a public pool of jobs for use by business processes that have no private pool of jobs. Allow enough for requests to keep moving through the message queues, but no more.

For a full discussion of appropriate pool sizes for different types of production, see Pool Size and Actor Pool Size.

Description
Comments that describe the production.

Log General Trace Events Trace messages are informational text messages that InterSystems IRIS can deliver to the Terminal window and, optionally, to the Event Log. Trace messages are unrelated to Visual Trace, which provides a graphical view of production message objects as they travel through a production.

By default, the Log General Trace Events check box is clear. When selected, it enables logging of all trace messages issued by production elements that are not business hosts. Logging means that InterSystems IRIS automatically stores copies of these trace messages in the Event Log.

Each business host has its own Log Trace Events setting, which controls logging of trace messages from that business host. There is no overlap or interaction between these settings. Log General Trace Events does not override or provide a default value for Log Trace Events.

Shutdown Timeout
How long in seconds to wait while attempting to shut down a production before forcing the shutdown. The value must be between 0 and 3600 (or one hour). The default value is 120.

Testing Enabled
Select this check box to enable use of the Testing Service pages to test this production. Clear this check box to disable the testing service.

Update Timeout
How long in seconds to wait while attempting to update the configuration for a production that is b usy, before abandoning the update. The value must be between 0 and 3600 (or one hour). The default value is 10.

Provides reference information for settings that are available in most or all business services. You can configure these settings after you have added a business service to your production.

Summary
All business services have the following settings:

Group

Settings

Comment, Category, Class Name, Description, Adapter Class Name, Adapter Description, Business Partner

Enabled

Schedule, Pool Size, Throttle Delay, GenerateSuperSessionID

Alert Grace Period, Alert On Error, Inactivity Timeout

Development and Debugging

Foreground, Log Trace Events, Archive IO

Adapter Class Name Common to business services and business operations. The class name for the inbound adapter associated with this business host, if any. This field is read-only and is determined by the b usiness host class definition.

Adapter Description
Common to business services and business operations. Comments that describe the adapter class. This field is read-only and displays the first line of the class annotation in the code.

Alert Grace Period Specifies an optional grace period during which errors relating to e xternal connections do not trigger alerts (even if Alert
On Error is True). If the error condition still exists after the grace period, the business service triggers an alert; otherwise
no alert is triggered.

Business processes and operations have a similar setting.

Alert On Error Common to all business hosts. When this setting is set to True, as soon as the business host encounters any type of error condition it automatically triggers an alert. An alert writes a message to the Event Log and can also send notification to a user via email or other mechanism. For details, see Configuring Alerts.

Archive IO
Common to business services and operations. If True, the adapter associated with this business service or operation logs in the I/O archive each input and output communication it shares with the external system.

Business Partner
Common to all business hosts. Specifies an optional b usiness partner applicable to this business host. Select a business host profile , if available.

A business partner profile is information about an or ganization or application connected to your InterSystems IRIS system. For each business partner, you can provide information such as the partner name, notes, primary and alternative contacts,

and contact details. Defining a profile has no ef means to store more information.

fect on the behavior or running of the production. It simply gives you a

For example, suppose your production talks to ABC Hospital and XYZ Hospital. You can enter profiles for both of these along with contact information. When you configure items that communicate with these or ganizations, you can specify the defined b usiness partner for each business host.

For information on defining these profiles, see Configuring Business P artners.

Category
Common to all business hosts. An optional text label that you can use to visually group business hosts within the production diagram. Category names are case-sensitive and can contain space characters.

The Category drop-down list contains all the categories that are used in the current production. Specify this setting as follows:

- To specify one category, either type the category name or select it from the Category drop-down list. If you type a category name and it does not yet exist, InterSystems IRIS creates it.

- To specify multiple categories, select the check box for each desired category from the Category drop-down list. Or type a comma-separated list of categories.

To delete a category, remove that category selection from all business hosts that use it. If the Category drop-down list still displays the category, that means that the category is still in use. In this case, filter the display to sho w only business hosts that use that category. Then for each of the business hosts that you see, edit the Category to remove the category.

Class Name
Common to all business hosts. The business host class name. This field is read-only .

Comment
Common to all business hosts. An optional text description.

Description
Common to all business hosts. Comments that describe the business host class. This field is read-only and displays the first line of the class annotation in the code.

Enabled
Common to all business hosts. Enables the business host, so that it processes messages whenever the production runs. You can also double-click a business host in the diagram to toggle between enabling and disabling it.

When the Enabled check box is clear, the business host is still present in the configuration, and its queue continues to accept messages, but none of these messages are processed until the business host is enabled again.

This setting is useful, for example, if there is a communications breakdown on the external side. For example, if an email server goes down, or something similar happens, you can disable the associated business service until throughput is restored.

The Enabled check box is a setting stored in the production class definition. If the production is read-only due to being managed by source control, you cannot change this setting unless you have checked the production out of source control. If the production is in source control, you can manage the item using the Stop, Start, and Restart buttons on the Action tab without checking the production out of source control. The action of these buttons does not change the production class.

Foreground
Common to business services and operations. By default, this check box is clear. Select it for debugging or diagnostic purposes only. Jobs in operational systems almost never run in the foreground. When you select the Foreground check box,

any system jobs used by the business service run in a Terminal window at the front of the console display. This allows InterSystems IRIS to display debugging or trace messages in that window. See Testing and Debugging Productions.

Generate SuperSession ID This setting controls whether the message will have a SuperSessionID, which can be used to identify messages that cross from one production to another. For details, see Supersessions.

Inactivity Timeout
Common to all business hosts. A business host has an Inactive status after it has not received any messages within the number of seconds specified by the Inactivity Timeout field. The production Monitor Service periodically reviews the status of business services and business operations within the production, and marks the item as Inactive if it has not done anything within the Inactivity Timeout period.

The default value is 0 (zero). If this setting is 0, the business host will never be marked Inactive, no matter how long it stands idle.

Log Trace Events Common to all business hosts. Trace messages are informational text messages that InterSystems IRIS can deliver to the Terminal window (if you select the Foreground check box) and, optionally, to the Event Log. Trace messages are unrelated to Visual Trace, which provides a graphical view of production message objects as they travel through a production.

By default, the Log Trace Events check box is clear. When selected, it enables logging of all trace messages issued by this business host. Logging means that InterSystems IRIS writes the trace messages to the console Terminal window (if your job is running in the foreground) and it also stores copies of these messages in the Event Log.

Common to all business hosts. Specifies ho w many system jobs to allocate to run this business host.

Notes specific to b usiness services:

- For business services, the default is 1.

- You must use a value of 0 if the business service is being invoked via the Ens.Director method CreateBusinessService();
this is called an adapterless business service.

- You may use a value greater than 1 with File or FTP inbound adapters if you want multiple jobs competing to pull files from the same input directory , or if you have a TCP Service configured with an e xclamation point (!) to make it initiate the connection.

For a full discussion of appropriate pool sizes, see Pool Size and Actor Pool Size.

Schedule
Common to all business hosts. An optional command string that schedules stop and start times for the business host. The
string is a comma-separated list of event specifications, each of which has the follo wing format:

action:YYYY-MM-DDThh:mm:ss

Where action is either START or STOP to indicate the desired event. Type a schedule string or select an existing schedule specification.

For details on the schedule string, see Configuring Schedule Specifications

.

Throttle Delay
Common to business services and business operations. Specifies a period of forced idleness before processing the ne xt message, in milliseconds. The default is 0.

For a business service, the delay occurs before each call to the adapter's OnTask() method. For a business operation, the delay occurs before each attempt to dequeue a new message.

This setting does not apply to SOAP services in CSP mode and other services invoked externally via CreateBusinessService(). It applies on a per-job basis so that operations with Pool Size greater than 1 and services with JobPerConnection as true can still generate multiple messages within the interval.

Provides reference information for settings that are available in most or all business processes. You can configure these settings after you have added a business process to your production.

Summary
All business processes have the following settings:

Group

Settings

Notes

Comment, Category, Class Name, Description,
Business Partner

See these settings for business services

Enabled

FIFO Message Grouping

Group Calculation, Group Completion Hosts

Schedule,

Pool Size, Reply Code Actions

Alert Retry Grace Period, Queue Count Alert, Queue
Wait Alert

Alert On Error, Inactivity Timeout

Development and
Debugging

Log Trace Events

See this setting for business services

See Maintaining First-In
First-Out (FIFO)
Processing

See this setting for business services

See these settings for business services

See this setting for business services

Common to business processes and operations. Specifies an optional grace period during which errors relating to e xternal connections do not trigger alerts (even if Alert On Error is True).

This grace period starts only after the first occurrence of an error .

If the error condition still exists after the alert period expires, the business operation triggers an alert; otherwise no alert is
triggered.

Note that depending on how long it takes the adapter or business operation to return errors, the business host may avoid triggering an alert even when the Failure Timeout expires. For instance, suppose the Retry Interval is 5 seconds, Failure Timeout is 15 seconds, and Alert Retry Grace Period is 14 seconds. If it takes the adapter or business operation more than 1 second to return the error, then the Alert Retry Grace Period goes beyond the Failure Timeout and the alert may not be triggered, depending on how long the adapter/operation takes to return after retrying.

Business services have a similar setting.

Common to all business hosts. Specifies ho w many system jobs to allocate to run this business host.

Notes specific to b usiness processes:

- A business process shows no pool size if its private pool size is 0 (zero), meaning that it gets its jobs from the public actor pool shared by all business processes in the production.

- Larger numbers are not necessarily helpful; see Pool Size and Actor Pool Size.

Important: When you disable a business process, it must have a Pool Size = 1 or greater if you want all instances of

only this business process to stop. If the business process has a Pool Size = 0, the action disables all business processes that share the actor pool. See Pool Size and Actor Pool Size.

Queue Count Alert Common to business processes and operations. Specifies an alert threshold for the number of items in the queue of this business host. An alert is triggered when this threshold is exceeded.

InterSystems IRIS sends an alert when the number of items in a business host’s queue reaches the threshold set by this setting for that business host. This alert has the prefix QueueCountAlert: (not localized). This alert is to detect large queues that are building up.

The service that checks the queue count runs every fiv e seconds, so the granularity of the checking is somewhat limited, but should still provide timely warnings about processing and flo w problems.

To disable this alert, specify this setting as 0.

For information on alerts, see Configuring Alerts.

Queue Wait Alert Common to business processes and operations. Specifies the length of time that a message can w ait in the business host’s queue or be the active message before an alert is triggered.

This alert has the prefix QueueWaitAlert: (not localized). This alert is useful to detect whether a queue is processing messages.

To disable this alert, specify this setting as 0.

The service that checks the wait periods runs every fiv e seconds, so the granularity of the checking is somewhat limited, but should still provide timely warnings about processing and flo w problems.

If a Queue Wait alert has been triggered, then the clearing of the known delay happens when the queue delay time for the item at the head of the queue is less than 80% of the Queue Wait Alert time setting. This is to prevent false re-alerting as a queue is drained. It is possible to change the default 80% with the API: Do
##class(Ens.MonitorService).setQWTPct(0.9)

For information on alerts, see Configuring Alerts.

Reply Code Actions Common to business processes and business operations. Specifies one or more rules that specify what the b usiness host should do on receipt of various reply status conditions, particularly error conditions. Specify a comma-separated list of code-action pairs.

Important:

Independent of the value of this setting, the adapter automatically retries in the case of errors such as timeout or failure to connect.

The format of the list is:

code=actions,(code,code)=actions, ... code=action

The following table lists the types of reply status condition identified by code.

Code

E

Meaning

Error status returned from message handler.

E#statuscode

Error status returned from message handler has status code equal to statuscode.

E*text

Error status returned from message handler contains text string text.

There is no reply message object at all.

The following values for action may be used alone or combined to form strings.

Action

Meaning

W

R

S

F

Treat the document as Completed OK.

Log a warning but treat the document as Completed OK.

Retry the message according to the configured Retry Interval and Failure Timeout settings; finally Fail,
unless a different action is also specified. Note that the final status of the message is Completed. (This means that if you need the final status of the message to indicate an error, you should combine this action code with the F action code.)

Suspend the message, log an error, and move on to try the next message.

Disable the business process or operation, log an error, and restore the outbound message to the front of the business host queue. When you choose the disable action for a business process, you must configure the business with a Pool Size = 1 or greater if you want all instances of only this business process to stop. If the business process has a Pool Size = 0, the disable action disables all business processes that share the actor pool. See Pool Size and Actor Pool Size.

Fail or retry, depending on the Retry property of the business host (which is not exposed as a setting,
but which may be set programmatically):

- If the Retry property is 0, the F option means that the business host will fail the message with an error and then move on to the next message in its queue.

- If the Retry property is 1, the F option means that the business host will retry the message,
subject to the configured RetryInterval and FailureTimeout settings; if the retry fails, the business
host will fail the message with an error and then move on to the next message in its queue.

For example:

E#6301=R,E*ErrGeneral=R,E=F

The default value for the Reply Code Actions string is E=F

All codes where the actions consists of only W (log a Warning) are evaluated and warnings generated if they trigger. Other codes are evaluated in left-to-right order, executing the first one that triggers that has a non-w arning actions value. For example if the reply code action has the value E=RD, the business process or operation first retries to send the message until Failure Timeout setting and then, if the failure continues, it disables the business process or operation.

Settings in All Business Operations

Provides reference information for settings that are available in all business operations. You can configure these settings after you have added a business operation to your production.

Summary
All business operations have the following settings:

Group

Settings

Comment, Category, Class Name, Description, Adapter Class Name, Adapter Description, Business
Partner

Enabled

FIFO Message Grouping

Group Calculation, Group Completion Hosts

Schedule, Pool Size

Reply Code Actions

Retry Interval, Failure Timeout

SendSuperSession

Throttle Delay

Queue Count Alert, Queue Wait Alert

Alert On Error, Inactivity Timeout

Development and
Debugging

Foreground, Log Trace Events, Archive IO

Notes

See these settings for business services

See Maintaining First-In
First-Out (FIFO)
Processing

See these settings for business services

See this setting for business processes

See this setting for business services

See these settings for business processes

See these settings for business services

See these settings for business services

Common to business processes and operations. Specifies an optional grace period during which errors relating to e xternal connections do not trigger alerts (even if Alert On Error is True).

If the error condition still exists after the alert period expires, the business operation triggers an alert; otherwise no alert is
triggered.

Business services have a similar setting.

Failure Timeout
Total number of seconds to keep trying to connect with a destination outside InterSystems IRIS. After this number of seconds has elapsed, the business operation discards the message data and returns an error code. To ensure that no message is ever

Settings in All Business Operations

skipped, enter a Failure Timeout value of –1, which means never time out. Use a setting of –1 when complete data delivery is critical, for example in healthcare applications.

Retry Interval
Number of seconds to wait between attempts to connect with a destination outside InterSystems IRIS.

SendSuperSession
Controls whether to include the SuperSessionID property in the outgoing message; except for HTTP and SOAP, custom
coding is also needed. For details, see Supersessions.

Pool Size and Actor Pool Size

Provides conceptual and reference information for the Pool Size and Actor Pool Size settings.

The choice of Actor Pool Size for the production, and Pool Size for each business host, determines how many jobs are available to perform which types of work for the production. These numbers are an essential part of the production design and are unlikely to need adjustment once the production is deployed live.

You can use pool size to force first-in first-out (FIFO) processing, b
FIFO Processing.

ut another option is also available; see Maintaining

Each business service, business process, or business operation can have its own, private pool of allocated jobs. You can configure the size of this pool, the Pool Size setting, in the Management Portal. InterSystems recommends setting Pool Size equal to the number of CPU cores. If the business hosts spend a significant amount of time w aiting or idling, a higher value can improve performance. However, a Pool Size higher than the number of CPU cores causes problems when there is a sudden peak in the workload: the operating system then allocates memory for each process, swap activity escalates, and often the OOM killer intervenes, terminating processes, including InterSystems IRIS itself.

Pool Size as Zero InterSystems IRIS uses a Pool Size of 0 for an adapterless business service. This is a business service that is invoked directly from outside InterSystems IRIS, rather than receiving its requests in the usual way, via an inbound adapter. An adapterless business service may be invoked via InterSystems IRIS language bindings, CSP pages, SOAP, or a routine invoked from the operating system level. For details, see Invoking a Business Service Directly.

If you set a business operation to run in process as opposed to queued, InterSystems IRIS does not create a background job or message queue for the business operation. Instead, whenever a request is sent to this business operation, the production instantiates the business operation within the caller’s job, and invokes its methods within that job, as well. Consequently, no job pool is necessary, and you must set the business operation Pool Size to 0.

For all other types of business service or business operations, if you set the Pool Size to 0, the business host does not run.

Unlike other types of business host, a business process has the option of sharing jobs from a public pool; this pool is called
the actor pool or Ens.Actor. You can configure the Actor Pool Size for the production. Actors in the production-wide actor pool have no affiliation with or kno wledge of a specific b usiness process. Any business process that has a private Pool Size of 0 can use jobs from the public actor pool.

The choice as to whether or not a business process should use its own private pool or the public pool depends on the needs of the production. Any nonzero value for a private Pool Size ensures that the business process only uses jobs from its private pool. If you want any business process to use jobs from the actor pool, its private Pool Size must be 0. The default production configuration allo ws 1 job in the private pool for each business host, and 2 jobs in the production-wide actor pool. This
means that if you want business processes to share the actor pool it does not happen automatically; you must set their
individual Pool Size settings to 0.

When you disable a business process, the result depends on the private Pool Size configuration setting:

- Business process Pool Size > 0:

- The business process only uses jobs from its private pool; you can disable just this process by clearing the Enabled
check box on the configuration page of the b usiness process.

Business process Pool Size = 0:

Pool Size and Actor Pool Size

You cannot disable a business process with a pool size of 0 because it would stop all business processes using the shared actor pool. If you want to disable a business process, first set the pool size > 0 so it uses its o wn dedicated queue. If you do want to stop all business processes using the shared actor pool, set the Actor Pool Size to 0 in the production settings tab.

Effect of Changing Pool Size for a Business Process When a business host has a Pool Size of 1 or more, the queue for that business host is named the same as the business host.
If you modify Pool Size for a business process, setting it to 0, the business process now uses the shared queue Ens.Actor;
this can be confusing if you are accustomed to looking at the queue.

Considerations and Trade-offs Except in cases where you use a pool size of 1 to force FIFO processing, private pools of a size 1 or greater can be useful for fast-running business processes in a production that also includes slow-running business processes. A fast-running business process can have a private pool to ensure that its requests never get stuck in the public actor queue behind accumulated requests for the slow-running business processes.

If every business process in your production has a private pool, then the Actor Pool Size for the production can be 0. On the other hand, if your production includes many business processes that use the public actor pool, you can raise the Actor Pool Size for the production from the default of 2 to prevent bottlenecks when many business processes are running. Inter- Systems recommends that, as a maximum, you set the Actor Pool Size equal to the number of CPUs in your InterSystems IRIS server machine. You could set the number higher, but at any one time there are only as many jobs available as there are CPUs.

- Maintaining First-In First-Out (FIFO) Processing Maintaining First-In First-Out (FIFO) Processing Describes options for maintaining first-in first-out (FIFO) processing of messages.

In some scenarios, it is necessary to preserve FIFO processing of messages. The prime example is healthcare applications. Suppose a patient enters a hospital and requires care. System A sends out an admit event, followed by a treatment order, but System B receives the order first. System B cannot process the order without an admit, so upon recei ving the order, it produces an error. This may delay patient care or require the information system to execute complex logic to associate admit with the order after the admit finally arri ves at System B.

There are two general approaches to preserve FIFO processing in a production, both described on this page:

- Force overall FIFO processing by preventing parallel activities.

- Programmatically define groups of messages that require FIFO processing.

Forcing Overall FIFO by Preventing Parallel Activity In this approach for maintaining FIFO order, you simply limit each business host to use at most one job at any time.

If all the business hosts in the production have only one job available, only one message can be processed at a time by each host. This gives each message from a given source only one possible path through the production, so each message is guaranteed to arrive at its configured destination in the same order in which it w as sent. (In contrast, with a business host that has multiple jobs, a message from a particular source could skip over other messages from the same source by using a faster, parallel job to arrive at its destination sooner.)

In this approach, you set the Pool Size setting to 1 for every business service, business process, and business operation, and you set the Actor Pool Size for the production to 0. Also, to guarantee FIFO for a BPL business process, in addition to setting
its Pool Size to 1, do one of the following:

- Make calls using a <code> SendRequestSync() call

OR

- Do not make calls from conditional branches of your business process logic and only make calls to elements that are themselves FIFO.

Defining FIFO Groups In this approach for maintaining FIFO order, you identify and use data within the messages to place the messages into groups. For example, you might use the MRN of a patient, available in specific locations in the messages. This approach requires more work than overall FIFO but permits parallel activity (such as processing different patient messages at the
same time). In this case, do the following:

1. Gather information:

- Identify the field or fields that you can use to group messages. Determine ho w you will use these fields to create a unique identifier for the FIFO group.

- Determine if the processing of one group is dependent in any way on the completion of another group.

- Considering the path that the messages will take through the production, identify the business host (called the starting host) where the FIFO group is first needed. F or example, many business services may generate production messages in a single-threaded fashion, sending these production messages to a business process for routing. We can use this business process as the starting host, and define FIFO groups for the inbound messages that come to this business host.

Maintaining First-In First-Out (FIFO) Processing

- Also identify the business host or hosts where FIFO processing is no longer required for this group (the completion
host). The completion host or hosts can release messages from their FIFO group; internally this removes identifiers
from the message that force them to be grouped.

2. Create a DTL transformation whose purpose is to compute the FIFO group identifier . For this DTL, the source object
will be the request type (as available at the business host where you will define the FIFO groups). The target must be
of type Ens.Queue.FIFOMessageGroup.Data. In this DTL, set the following properties of the target:

- Identifier—Required. This is the string that identifies the message group.

If it is not possible to determine a group, use the special value $$$EnsFMGSingleThreadIdentifier, which
evaluates to "_SingleThreadOverride". This value enables this message to be processed but disables parallel processing while the message is being processed. That is, no additional messages will be taken from the queue until this message has been processed.

Internally if the production encounters an error when using this DTL for a message, the system will use this special value for the message, for the same reason.

- Dependencies—Optional. This is a comma-separated list of other possible message groups that this group must wait on, if those groups are in the queue.

- CompletionHosts—Optional. This is a comma-separated list of hosts responsible for releasing the hold on the particular message group identifier . The first matching host will be the one to release this hold (enabling multiple messages in this group to be processed at the same time). This is used as an alternative to the host setting (see below).

In this DTL, use new for the target. Also, for this DTL, aux is not defined.

3. Add this DTL to the production.

4. Configure the starting host (identified abo

ve) by specifying values in FIFO Message Grouping as follows:

- Group Calculation (FMGCalculation)—Specify the name of the DTL you created previously.

- Group Completion Hosts (FMGCompletionHosts)—Optionally specify a comma-separated list of the completion hosts.

Maintaining FIFO Groups in Custom Code Rather than use a DTL transformation as described above, you can define FIFO groups in custom code. Instead of specify values for the Identifier, Dependencies, and CompletionHosts properties of the target, use syntax like the following, which
uses macros defined for this purpose:

Set $$$EnsThisFIFOMessageGroup = identifier
Set $$$EnsThisFIFOMessageGroupDependencies = dependencies
Set $$$EnsThisFMGCompletionHosts = completionhosts

Where identifier is the FIFO group identifier , dependencies is a comma-separated list of other message groups (if needed), and completionhosts is a comma-separated list of completion hosts (if needed).

If needed, you can use SetFIFOMessageGroupData() function.

Also, Ens.Queue.FIFOMessageGroup provides class methods to release a hold by one or more message headers in the queue. These methods can be also invoked as SQL procedures.

ReleaseHoldForHeaderId()

ClassMethod ReleaseHoldForHeaderId(pMsgHeaderId As
%String, pSignalQueue As %Boolean=1) as %Status

Clears the hold on the FIFO group associated with the given message header.

ReleaseHoldForAll()

ClassMethod ReleaseHoldForAll(pQueueName As
%String, pOnlyCompletedSessions As %Boolean=1) as %Status

Given a message queue, loops through all message headers in the queue that are marked as being active in the FIFO group pipeline and clears them.

The default is to clear only headers that belong to sessions that are considered Complete. If pOnlyCompletedSessions is 0, then all message headers are cleared.

Supersessions

Supersessions

Describes how to configure supersessions and pro vides reference information on the Generate SuperSession ID and Send- SuperSession settings.

In a production, any session is unique to the production. In some cases, a production sends messages to other productions. In such cases, it can be useful to define a supersession that connects the activities across the productions. To do so, you use the Generate SuperSession ID and SendSuperSession settings.

When supersessions are defined, the supersession ID is displayed as SuperSession property of the message header within the message traces.

Note:

The Visual Trace displays only one production at a time. To see supersessions, use the Enterprise Message Viewer and search for a specific supersession.

Configuring Productions to Use Supersessions Supersessions are relevant when multiple productions communicate with each other, so generally you perform this configuration within multiple productions.

Setting up supersessions is easiest when the productions communicate via HTTP (which includes SOAP), because there is a default system that relies on a private InterSystems HTTP header. In such cases, to configure a production to use supers-
essions:

- Enable the Generate SuperSession ID setting in all applicable business services (all business services that generate activity that will result in messages being sent to another production).

- Enable the SendSuperSession setting in all applicable business operations (all business operations that send messages to the other productions).

Wherever the communications between productions do not use HTTP, however, additional work is needed. Specifically:

- Define a con vention to represent the supersession ID in the messages that pass between productions.

- For a business operation, add custom code as following:

1. Call the IncludeSuperSession() of the business operation. This method returns 1 if the SendSuperSession setting

is enabled and if the %SuperSession property of the business operation has been set.

2. When generating the outbound message, use the %SuperSession property as the supersession ID in that message.

If SendSuperSession is 1, the business operation will automatically use the %SuperSession property in headers for
response messages within the production; no custom code is needed.

Also, if you want to customize the supersession identifiers, implement the OnGenerateSuperSession() callback in the business services. See Ens.Host, from which this callback is inherited. This method receives the message header, Ens.MessageHeader, as input and should return the supersession ID. The business service will then automatically use your custom value as the supersession identifier .

Supersession Processing Details If you have to write custom code to implement supersessions, it is helpful to understand the overall flo w in more detail. If
Generate SuperSession ID is enabled for a business service, then on receiving input:

1. As an initial step, if the business service uses an adapter that uses HTTP, it looks for the

VND.InterSystems.Ensemble.SuperSession HTTP header. If this header is not null, the business service uses its value to set its own %SuperSession property.

For other business services, there is no equivalent step.

2. After any initial processing, if the %SuperSession property of the business service is null, the business service calls

the OnGenerateSuperSession() callback. If that method returns a value, the business service uses that value to set its own %SuperSession property.

3. The business service sets the SuperSession value in all message headers, including the response to the caller.

Similarly, if SendSuperSession is enabled for a business operation, then on receiving input:

1. The business operation checks the received message header for a non-null value of the SuperSession property.

2.

3.

If SuperSession is not null, the business operation uses that value to set its own %SuperSession property, where it can be used by adapter methods.

If the associated adapter uses HTTP, it automatically retrieves the %SuperSession property of the business operation and uses that value in the outgoing HTTP header, specifically VND.InterSystems.Ensemble.SuperSession

It also uses the same value as the SuperSession property in its response headers

Provides reference information for time stamp specifications for filenames.

Details
While configuring b usiness operations and business services that transmit data to and from files, you can often specify input and output filenames in a string that includes date and time format codes, such as %Y%m%d%H%M%s_%f.txt. At runtime, the format codes within this string resolve dynamically based on the current date and time.

InterSystems IRIS ® data platform supports the following rules for composing a time stamp specification string :

- The string may contain literal characters and any of the format codes listed in the following table.

- Characters that are not part of a format code appear in the resulting time stamp unchanged.

- All format codes are optional.

- Each format code consists of a % character, an optional # character, and a conversion character.

- InterSystems IRIS converts the time to a specific time zone or locale if the %K or %L format codes appear at the beginning of the string.

Symbol

%a

%A

%b

%B

%c

Locale’s abbreviated weekday name (Sun, Mon, ..., Sat)

Locale’s full weekday name (Sunday, Monday, ..., Saturday)

Locale’s abbreviated month name (Jan, Feb, ..., Dec)

Locale’s full month name (January, February, ..., December)

InterSystems IRIS date and time representation as provided by the local machine, except that in forming the time stamp, InterSystems IRIS replaces certain characters in the usual date and time format. It replaces spaces with underscores (_), slashes (/) with hyphens (-), and colons (:) with dots (.).

The result is something like:

MM-DD-YY_hh.mm.ss

The %c specifier can have parameters. %c(dformat,tformat,precision) formats the date and time
according to your specifications, where:

- dformat is a number indicating date format.

- tformat is a number indicating time format.

- precision is the number of decimal places used to represent subseconds.

See $ZDATETIME for a list of all possible dformat and tformat values.

%d

%#d

%D

%#D

Two digits indicating the day of the month (01-31)

Day of the month without leading zeros (1-31)

Date; equivalent to %m/%d/%y

Date; equivalent to %#m/%#d/%y

Symbol

%f

Name indicating the source of the data. The source is usually the input filename (for File and FTP) or a concatenation of the IP address and port number (for data that arrived via TCP).

In substituting a value for the format code %f, InterSystems IRIS strips out any of the characters
|,?,\,/,:,[,],<,>,&,,,;,NUL,BEL,TAB,CR,LF, replacing spaces with underscores (_), slashes (/) with
hyphens (-), and colons (:) with dots (.).

%#f

Only use the part of the input filename up to but not including the last period. For example:

- With Input filename “Summary.docx”, %#f is replaced with “Summary”.

- With input filename “MyData.txt.dat”, %#f is replaced with “MyData.txt”.

%$f

%F

%#F

%$F

%h

%H

Only use the part of the input file name from the last period to the end of the filename (the file
extension). For example, if the input filename is “MyData.txt.dat”, %$f is replaced with “.dat”.

As for %f, but with all alphabetic characters converted to uppercase.

As for %#f, but with all alphabetic characters converted to uppercase.

As for %$f, but with all alphabetic characters converted to uppercase.

Locale’s abbreviated month name. Equivalent to %b.

Two digits indicating the hour in 24-hour format (00-23)

%#H

Hour in 24-hour format without leading zeros (0-23)

%I

%#I

%j

%#j

Two digits indicating the hour in 12–hour format (01-12)

Hour in 12–hour format without leading zeros (1-12)

Three digits indicating the day of the year as a number (001-366)

Day of the year as a number without leading zeros (1-366)

%K(n)

Use the %K(n) format code only at the beginning of the time stamp specification string. %K(n) produces no output, but specifies a base time zone to convert to before formatting the time stamp.

n is the time zone, and can be one of the following (case-insensitive):

- Server—(Default) Time on the server where the executing code resides.

- UTC— Universal Time Coordinated (UTC)

- [+]n—Number of hours after (east of) UTC time. n may have a fractional value expressed as
a decimal; for example, 4.5

- -n—Number of hours before (west of) UTC time (n may be fractional)

- [+]hhmm—Hours and minutes after (east of) UTC time, in the ISO 8601:2000 standard format

- -hhmm—Hours and minutes after (west of) UTC time in ISO format Two digits indicating the month number (01-12) Month number without leading zeros (1-12)

Two digits indicating minutes (00-59)

Minutes without leading zeros (0–59)

%m

%#m

%M

%#M

Symbol

%N

%p

%#p

%P

%#P

%q or %q()

%q(0)

%q(1)

%q(2)

%q(3)

%q(4)

%q(5)

%Q

Three digits indicating the number of milliseconds (000-999)

Locale’s a.m. or p.m. indicator for a 12-hour clock (lowercase, with dots)

Locale’s am or pm indicator for 12-hour clock (lowercase, without dots)

Locale’s A.M. or P.M. indicator for a 12-hour clock (uppercase, with dots)

Locale’s AM or PM indicator for a 12-hour clock (uppercase, without dots)

HL7 format date and time; equivalent to %Y%m%d%H%M%S or %q(0)

HL7 format date and time; equivalent to %Y%m%d%H%M%S or %q

ODBC format date and time; equivalent to %Y-%m-%d %H:%M:%S.%N

ISO 8601:2000 standard date format; equivalent to %Y-%m-%d

InterSystems IRIS $HOROLOG format

InterSystems IRIS $ZTIMESTAMP format

Creates a GUID

ODBC format date and time; equivalent to %Y-%m-%d %H:%M:%S.%N or %c(3,,3) or %q(1)

%Q(n)

Equivalent to %q(n)

%r

%#r

%R

%S

%t

%T

%u

%#u

%U

Time with seconds in 12-hour format using a.m. or p.m. notation; equivalent to %I:%M:%S %p

Time with seconds in 12-hour format using am or pm notation without whitespace or dots;
equivalent to %I:%M:%S%#p

Time in 24-hour notation; equivalent to %H:%M

Two digits indicating seconds (00-60) (60 for leap seconds)

Produces a <tab> character

Time with seconds in 24-hour notation; equivalent to %H:%M:%S

Day of the week as a number (1-7). Monday=1, Tuesday=2, ..., Sunday=7.

Equivalent to %u

Two digits (00–53) indicating the current week within a week-based year convention that does not conform to the ISO 8601:2000 standard.

The rules are as follows:

- The week numbers are 00-53

- Sunday is the first day in each week.

- The first Sunday of January is the first day of week 1

- Days in the new year before the first Sunday are in week 0.

%#U

Number indicating the current week within a week-based year that follows the rules described for %U, except the output does not include leading zeros (0-53).

%w

Day of the week (Sunday=0, Monday=1, ..., Saturday=6)

Symbol

%#w

%W

Equivalent to %w

Two digits (00–53) indicating the current week within a week-based year convention that does not conform to the ISO 8601:2000 standard.

The rules are as follows:

- The week numbers are 00-53

- Monday is the first day in each week

- The first Monday of January is the first day of week 1

- Days in the new year before the first Monday are in week 0.

%W is equivalent to %U(1).

%#W

Number indicating the current week within a week-based year that follows the rules described for %W, except the output does not include leading zeros (0-53). %#W is equivalent to %#U(1).

%y

%Y

%z

%#z

Two digits indicating the year within a century (00-99). For example, the year 1983 produces the
number 83 in the time stamp; 2019 produces 19.

Four digits indicating the year (0000-9999)

Time zone as an offset from Universal Time Coordinated (UTC) in the ISO 8601:2000 standard format (+hhmm or -hhmm). For example, -0430 means 4 hours 30 minutes behind UTC (west of Greenwich). If InterSystems IRIS cannot determine the time zone, it ignores the %z code in the time stamp specification string.

Time zone as an offset from Universal Time Coordinated (UTC) in hours with leading +/- and without leading zeros. Trailing decimals may appear. For example, -4.5 means 4 hours 30 minutes behind UTC (that is, west of Greenwich). If InterSystems IRIS cannot determine the time zone, it ignores the %#z code in the time stamp.

Symbol

%+(nn)

Inserts a counter and tests for filename uniqueness on a local file (not FTP) where nn is a string of alphanumerics and other characters.The alphanumeric characters in the string are incremented from the right-most character. Nonalphanumeric characters are included unchanged in the output file specification. Numeric characters are incremented from 0 to 9 and alphabetic characters are incremented from a to z or from A to Z.

For example, if the filename string specification is “%f_%+(1)” and the input file is “NewFile.txt”, then InterSystems IRIS first checks if “NewFile.txt_1” exists. If it exists, it checks “NewFile.txt_2” through “NewFile.txt_9” and then “NewFile.txt_10” and so on. It creates the file with the first filename that doesn’t yet exist.

If the filename string is “%f_%+(a.1), it first increments the 1 digit and then, after reaching 9, it
increments the a; first testing the strings “NewFile.txt_a.1” through “NewFile.txt_a.9” and then
“NewFile.txt_b.0” through “NewFile.txt_b.9” and then “NewFile.txt_c.0” and so on. After it reaches “NewFile.txt_z.9”, it prepends an 1 to the string. In this case, it tests “NewFile.txt_1a.0” next.

Typically, the counter is used in conjunction with a timestamp to reduce the possibility that filenames are duplicates even if they are created with the same timestamp. Combining a timestamp with a counter makes it extremely unlikely that filename collisions will occur.

You can use the %+ counter specification only once within a filename specification.

The counter format can be modified by inserting any of the following symbols between the percent
sign and the plus sign:

- Dollar sign ($)—Allows the counter to be used for remote FTP filenames. Always increment a static counter and use the resulting value. For local files, the uniqueness check is then made.

- Exclamation point (!)—Only append the counter if the filename without the counter would not be unique.

- Number sign (#)—Omit leading zeroes and omit leading a’s if they are not required to make a unique filename.

If the dollar sign ($) is not specified, the counter always restarts from the initial value specified in nn. If used with a timestamp, the counter is typically incremented a small number of times before a new timestamp value ensures uniqueness. If you are using the counter without a timestamp and expect it to be incremented many times, you should specify the dollar sign to avoid continually rechecking the filenames that you have already created.

Consider the format “%#F_%Q_%+(a0)%$f”. If the input filename is “NewFile.txt” and three files
are created with the same timestamp, these files are named:

- NEWFILE_2014-09-12_16.43.15.895_a0.txt

- NEWFILE_2014-09-12_16.43.15.895_a1.txt

- NEWFILE_2014-09-12_16.43.15.895_a2.txt Literal % percent sign Literal ( left parenthesis

Reserved token (do not use). This sequence passes through unchanged.

%%

%(

%_

The previous table describes all the format codes that you can use when specifying time stamps for use with an inbound or outbound file adapter . These codes conform to POSIX, IEEE, and ISO standards for time format codes. The following table lists the time stamp format codes that do not conform to these standards, or that conform to other standards.

Symbol

Unique Meaning Within a Filename Specification

%#

%c

%E

%F

%K(n)

%L(n)

%O

%P

%q,%Q

InterSystems IRIS® supports (and extends) certain Microsoft extended semantics, such as the %# prefix.

This indicates the InterSystems IRIS time stamp provided by the local machine.

InterSystems IRIS does not support the %E code.

InterSystems IRIS supports %F as an uppercase replacement string, not an ISO format date. InterSystems IRIS supports the ISO format date as %q(2) or %Q(2).

The user defines the time zone by providing the %K(n) code at the beginning of the file specification string. The %K(n) code produces no output, but specifies a base time zone to convert to before formatting the time stamp.

The user defines the locale by providing the %L(n) code at the beginning of the file specification string. The %L(n) code produces no output, but specifies a base locale to use with locale-dependent format codes.

InterSystems IRIS does not support the %O code.

InterSystems IRIS defines this code as uppercase AM or PM.

InterSystems IRIS defines some of these codes according to standards other than POSIX, IEEE, or ISO, such as HL7 or ODBC.

%(

InterSystems IRIS defines this code as a literal ( character.
