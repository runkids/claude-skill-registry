# Using the Legacy Production Configuration P age

Note:

Starting with 2025.1, you can use a new integrated application to configure productions (and also edit rule sets and DTL data transformations).

To create and configure interoperability productions, you use the Production Configuration page, introduced here.

### 1.1 Displaying the Production Configuration Page

To display the Production Configuration page:

1. Log in to the Management Portal.

2. Switch to the namespace you want to work in.

3. Click Interoperability > Configure > Production.

This page then displays the currently selected production (if any) in that namespace.

For example, the following figure sho ws a sample production.

The main area of the page displays the production, and the Settings tab on the left displays settings relevant to the currently selected item, as well as additional tabs that provide easy access to management options.

Introduction to the Legacy Production Configuration Page

If you click Production Settings above the diagram, the options apply to the entire production. Similarly, if you click a business host, the options apply to that business host.

### 1.2 The Update Button

While you are developing new code and configuring the production, it sometimes happens that when you start the Management Portal, InterSystems IRIS detects a discrepancy between the production as defined in the code, and the status of the running
production. Examples would be if:

- A specific b usiness host experienced an error and has died (the most likely cause).

- You changed a configuration parameter for a b usiness host in a running production, such that the host now needs to be restarted.

- You enabled or disabled an item in a production, and this action requires the production to be stopped and restarted.

- A production typically opens a Terminal window, but this window was closed by a user action while the production was still running.

When such discrepancies occur, the Update button appears on the Production Configuration page. If you click the button, InterSystems IRIS updates the production to resolve the discrepancy. If you prefer for the system to attempt to resolve the discrepancy automatically, you can add a business service based on the Ens.ProductionMonitorService class to the production. For more information, see Using the Production Monitor Service.

### 1.3 Controlling the Display

This section describes how to filter the display, sort the display, how to display alternative views of the production, how to control the refresh of the display, and how to hide the production or business host settings.

#### 1.3.1 Filtering the Display by Category

To filter the b usiness hosts in the production diagram, use the Category list.

Select a value from this list. When you do so, the diagram display only those business hosts that have been assigned to the given category. Or click All to view all the business hosts in the production.

Note that a business host can be assigned to multiple categories.

For details, see Category in the reference Settings in All Productions.

#### 1.3.2 Sorting Business Hosts

To sort the business hosts in the production diagram, use the Sort options:

- Name—Sorts items alphabetically within each column.

- Status—Sorts items within each column by status as follows: disabled, enabled, error, inactive.

- Number—Sorts items as listed in the production class (which, by default, represents the order in which they were added to the production). To modify this order, you can edit the production class in an IDE.

Controlling the Display

#### 1.3.3 Choosing a View Type

To view the business hosts in a different way, use the View options:

These view types are as follows:

- The listing view If the name of a business host is truncated due to the width of the columns, you can hover over the business host to view its full name.

- displays the business hosts in lists, within the Services, Processes, and Operations columns.

The listing view is used in most of the documentation.

The monitor view attention. Here, click a circle to see a box with details for the business host.

represents each business host in a larger circle where you can easily see items that may need

Introduction to the Legacy Production Configuration Page

- The service bus view setting.

is relevant only if you configure business partners and enter values in the Business Partner

This view displays the business hosts grouped by their associated business partners.

#### 1.3.4 Controlling the Refresh

Click the circular arrow to refresh the diagram once or click on to reload a fresh copy of the production diagram every 60
seconds; the refresh timer is off by default.

Note that InterSystems IRIS checks the status of individual business hosts (on a shorter interval) and refreshes the display for individual hosts as needed, regardless of the setting of auto-refresh.

#### 1.3.5 Hiding the Settings Pane

Click the Hide Settings Tabs icon

to hide the production or business host settings.

### 1.4 Understanding the Color Coding

When in list or monitor view, the Production Configuration page displays a circular status indicator next to each business
host. The color of this circle indicates the state of the business host, as follows:

- Pale green means that the business host is enabled but is not running.

- Dark green means that the business host is running.

- Gray means that the business host is disabled.

- Red means that the business host is in an error state.

- Purple means that the business host is retrying its activity.

- Yellow means that the business host is inactive.

The page includes the Legend link, which you can use to display this information.

Note:

You can increase the visibility of the error states by specifying that the Error, Retry and Inactive states are to be indicated by a colored ellipse, not a circle. To do this append &VISUALAID=1 to the URL for the Production Configuration page.

Accessing Management Options

### 1.5 Accessing Management Options

The Production Configuration page includes tabs that pro vide easy access to management options.

These management tabs are as follows:

- Queue—Click to view a list of the queues related to this production or business host.

- Log—Click to view an abbreviated list of Event Log entries for this production or business host.

- Messages—Click to view an abbreviated list of messages processed by this production or business host.

- Jobs—Click to view jobs related to this production or business host.

Each of these tabs provides a link to a management page (which opens in a new window) with more information; see
Managing Productions.

On the Jobs tab, you can also manage active jobs; see Aborting Messages, Suspending Messages, and Stopping Jobs.

### 1.6 See Also

- Introduction to Configuration Tasks

- Managing Productions

- Monitoring Productions This page describes how to use the legacy Production Configuration page to create, open, export, generate documentation for, and delete productions.

For information on performing these tasks with the new UI, see Creating a Production.

Note:

If a production is Suspended or Troubled, see Correcting Production Problem States.

### 2.1 Creating a Production

To create a production:

1. Display the Production Configuration page .

2. Select New to create a new production.

3. Enter a Package Name, Production Name, and Description.

4. Choose Generic production.

5. Click OK.

6. Now you can add business hosts and configure them .

### 2.2 Opening a Production

To open a production:

1.

If you are not already in an interoperability-enabled namespace, choose your working namespace from the available interoperability-enabled namespaces.

2. Navigate to the Interoperability > List > Productions page, and then select Go, if necessary.

3. Select Open to open an existing production.

To open a production or create a new production when you currently configuring a production on the Production Configu-
ration page:

1.

If you have clicked anywhere within the diagram, click Production Settings.

This step returns the focus to the production and changes the options on the Actions tab.

2. Select the Actions tab.

3. Select Open on the Actions tab to open an existing production or select New on the same tab to create a new production.

### 2.3 Exporting a Production

To export a production from the Production Configuration page:

1.

If you have clicked anywhere within the diagram, click Production Settings in the right-hand pane.

This step returns the focus to the production and changes the options on the Actions tab.

2. Click Export on the Actions tab.

3. Select items to export.

4. Click Export.

5. Select whether you want to export the production to the server or to your local machine via the browser’s downloading

capability.

6.

If you are exporting to the server, enter a path and name of the export file. If you are do wnloading to your local machine via the browser, enter the name of the export file.

7. Click OK.

See Deploying a Production for details on exporting and deploying a production.

### 2.4 Generating Production Documentation

You can navigate to the Production Documentation page from the following places in the Management Portal:

- From the Interoperability > List > Productions page, select a production name and click Document.

- From the Interoperability > Configure > Production page, on the Actions tab for the production, click Document.

From the Production Documentation page for a production, you can generate or view the production documentation, which
includes a list of all the business hosts and their settings. Perform one of the following actions:

- Click View to display the online documentation you previously generated. If you click View and no HTML documentation exists, you can choose to generate it.

- Click Generate to create new documentation for this production using a background job.

- It may take a considerable amount of time to generate documentation for large productions; therefore, you may not
want to generate new documentation if you have not made changes to the configuration of your production.

Cancel to cancel the operation.

You can also generate HTML documentation and, additionally, PDF documentation using the following methods in the
Ens.Config.Production class:

Deleting a Production

- CreateDocumentHTML()—creates new documentation in HTML format.

For example, to create documentation for Demo.Loan.FindRateProduction in HTML format:

ObjectScript

Set
status=##class(Ens.Config.Production).CreateDocumentHTML("Demo.Loan.FindRateProduction",1,.URL,.ErrLog)

- RemoveDocumentHTML()—removes existing HTML-format documentation from the current namespace.

- CreateDocumentPDF()—creates new documentation as a PDF file.

For example, to create documentation for Demo.Loan.FindRateProduction in PDF format, you can use the method in
a statement similar to the following:

ObjectScript

Set
status=##class(Ens.Config.Production).CreateDocumentPDF("Demo.Loan.FindRateProduction",1,"C:\Temp\Rate.pdf",.Log)

The PDF format requires that you have a PDF renderer installed. It also requires Java.

### 2.5 Deleting a Production

To delete a production:

1. Navigate to the Interoperability > List > Productions page.

2. Click the production that you want to delete.

3. Click Delete.

4. Click OK.

### 2.6 See Also

- Modifying Business Hosts (Legacy UI)

- Deploying a Production

- This topic describes how to use the legacy Production Configuration page to add business hosts to a production.

- For information on performing these tasks with the new UI, see Adding Business Hosts.

### 3.1 Introduction

A business host is any business service, business process, or business operation within a production. These are also referred to generically as configur ation items.

A configuration item is al ways associated with a specific production. It may resemble or duplicate items in other productions. Each production is an entirely closed universe that does not use configuration items from other productions.

### 3.2 Configuration Names

By default, the name of a configuration item is the name of its underlying host class. Ho wever, you can assign a different name, to describe the purpose of the item, for example.

For example, if you have a business service class that communicates with a specific type of serv er, and you use it to communicate with the same type of server in different enterprise locations, you must configure the b usiness service with different settings to communicate with each enterprise location, even though the type of server is the same. Each different configuration of the business service must have a different Name in the diagram (except see Working with Multiple Versions of a
Business Host).

The following rules govern configuration names:

- The name must consist of at least one character.

- The name can contain letters, numbers, and any printable character except for the following:

- | ; , : [ < > \ / & "

- Neither the first nor the last character can be an y of the following: ! $ .

- The first character cannot be _ The name (if is it one character long) cannot be *

Important:

You cannot change the name of an existing configuration item. If you require a name change, you can copy the item and delete the original item.

### 3.3 Adding Business Hosts to a Production

To add a business host to a production:

1.

Identify (or create and compile) the appropriate business host class.

2. Open the production on the Interoperability > Configure > Production page.

3. Click plus-sign icon next to the Services, Processes, or Operations column heading.

4. Use the wizard; the details are different for the Business Service Wizard, the Business Process Wizard, and the Business

Operation Wizard.

5. Click OK to add the process to the production.

6. Configure the b usiness process as needed.

This process does not generate any new classes. It updates the production class.

### 3.4 Business Service Wizard

The Business Service Wizard provides multiple tabs, which correspond to different types of business service classes to use.
Click a tab and then specify values as follows:

- If you click the All Services tab, specify the following values:

– Choose a host class from the Service Class list. If the class you need is not listed, create and compile the class in

–

–

an IDE, and then return here to choose it.

Specify a configuration Service Name. For rules, see Configuration Names .

Enter a text label in the Display Category field to sort and or ganize items within the production. Display Category names are case-sensitive, and space characters are allowed. To place an item in multiple categories, list them in the Display Category field separated by commas (with no spaces around these commas).

–

Comment is an optional text description.

- If you click the X12 Input tab or HL7 Input tab (if available), specify the following values:

– Choose a messaging protocol to select an existing specialized host class.

–

Specify a configuration Name. For rules, see Configuration Names .

– Use the Target Name field to identify the b usiness process or business operation to which this business service

will send the messages that it receives.

If you select the Create New Router option, you can use the New Rule Package field to specify a package name that will be added to the name of the rule created for the new router. If you do not specify a New Rule Package value, the production’s package is used.

Business Process Wizard

–

Select the Default applies if no value check box if you want blank settings to be replaced with the system default settings when the business service is created. Fields identified by an asterisk ( *) will be replaced with the system

default values. Click

to view the possible default values.

- If you click the Business Metric tab, specify the following values:

– Choose a host class from the MetricClass drop-down list. If the class you need does not appear on this list, create

the class in an IDE, then return to choose it.

See Creating Business Metrics.

Specify a configuration Name. For rules, see Configuration Names .

Enter a text label in the Category field to sort and or ganize items within the production. Category names are casesensitive, and space characters are allowed. To place an item in multiple categories, list them in the Category field separated by commas (do not allow spaces around these commas).

Comment is an optional text description.

Call Interval determines how often the business metric will recalculate the values of its properties. The Call Interval is in seconds, starting from a minimum of 0.1 seconds. The default is 5 seconds.

–

–

–

–

### 3.5 Business Process Wizard

The Business Process Wizard provides multiple tabs, which correspond to different types of business process classes to
use. Click a tab and then specify values as follows:

- If you click the All Processes tab, specify the following values:

–

–

Business Process Class—Choose a base class from the list of valid business process classes. If the class you need does not appear on this list, create and compile the class and then return here to choose it.

Specify a configuration Name. For rules, see Configuration Names .

The wizard defaults to the business process class name if you leave this blank.

–

Specify other values as given after this list.

- If you click the X12 Router tab or HL7 Router tab (if available), specify the following values:

–

–

–

Auto-create Rule—Select this check box to create a rule definition name based on the b usiness process class name. When Auto-create rule is selected, you can use the New Rule Package field to specify a package name that will be added to the name of the rule created for the new router. If you do not specify a New Rule Package value, the production’s package is used. In most cases, the New Rule Package field is ignored if the Routing Process Name field be gins with a package name. However, if the package specified by the Routing Process Name field is the system package name Ens or Enslib, a rule that is auto-created will have a different package name added to the beginning of the rule name. This additional package is determined by the contents of the New Rule Package field. If the package of the production or routing process is used instead of a specified v alue, the generated rule class name ends with 'RoutingRule'.

Routing Rule Name—Use the field to identify the name of the routing rule set to which this b usiness process sends the messages that it receives. Only appears if the previous check box is cleared.

Once you select a rule name, you can click the magnifying glass to open the Rule Editor.

Specify a Routing Process Name. For rules, see Configuration Names . To specify a package for the new routing process, use the format package.name in the field.

The underlying business process class is EnsLib.MsgRouter.VDocRoutingEngine depending on which type of router you choose.

–

Specify other values as given after this list.

- If you click the Component tab, specify the following values:

–

–

–

Component Class—Choose a base class from the list of valid business process classes designated as components.

Component Name—Enter a configuration name for this item. F or rules, see Configuration Names . The wizard defaults to the component class name if you leave this blank.

Specify other values as given after this list.

Note that all types of business process share the following optional fields:

- Display Category—Enter a text label in the field to sort and or ganize items within the production. Category names are case-sensitive and space characters are allowed. To place an item in multiple categories, enter a comma-separated list.

- Comment—Enter a brief comment about the business process to appear in the informational settings.

- Enable Now—Select this check box if you want this business process to begin processing messages immediately when
the production runs; clear it for the process to be initially disabled.

### 3.6 Business Operation Wizard

The Business Operation Wizard provides multiple tabs, which correspond to different types of business operation classes
to use. Click a tab and then specify values as follows:

- If you click the All Operations tab, specify the following values:

– Choose a host class from the Operation Class list. If the class you need does not appear on this list, create the class

in an IDE, then return here to choose it.

Specify a configuration Name. For rules, see Configuration Names .

Enter a text label in the Display Category field to sort and or ganize items within the production. Display Category names are case-sensitive, and space characters are allowed. To place an item in multiple categories, list them in the Display Category field separated by commas (do not allo w spaces around these commas).

Comment is an optional text description.

Specify other values as given after this list.

–

–

–

–

- If you click the X12 Output tab, specify the following values:

– Choose TCP, File, or FTP to determine the host class. Each class already exists and requires no programming.

Simply choose one.

– Give the item a configuration X12 Operation Name. For rules, see Configuration Names .

–

–

Specify other values as given after this list.

Select the Default applies if no value check box if you want blank settings to be replaced with the system default settings when the business operation is created. Fields identified by an asterisk ( *) will be replaced with the system

default values. Click

to view the possible default values.

- If you click the Workflow tab, specify the following values:

– Choose a host class from the Operation Class drop-down list. If the class you need does not appear on this list,

create the class in an IDE, then return here to choose it.

– Give the item a configuration Operation Name. For rules, see Configuration Names .

– Choose whether or not to auto-create a workflo w role.

–

Specify other values as given after this list.

All types of business operation share the following optional fields:

- Display Category—Enter a text label in the field to sort and or ganize items within the production. Category names are case-sensitive and space characters are allowed. To place an item in multiple categories, enter a comma-separated list.

- Comment—Enter a brief comment about the business operation to appear in the informational settings.

- Enable Now—Select this check box if you want this business operation to begin processing messages immediately
when the production runs; clear it for the operation to be initially disabled.

### 3.7 See Also

- Modifying Business Hosts (Legacy UI)

- This topic describes how to use the legacy Production Configuration page to modify business hosts.

For information on performing these tasks with the new UI, see Modifying Business Hosts.

### 4.1 Enabling, Disabling, or Restarting a Business Host

You can either enable, disable, or restart business hosts individually or for a selection of business hosts.

To enable, disable, or restart a single business host, do one of the following:

- Double-click a host item. InterSystems IRIS displays a dialog box that allows you to enable, disable, or restart the host
item depending on the current state of the production and the host item:

–

–

–

If the production is running and the host item is enabled, the dialog box gives you the option to disable the host item, restart the host item, or to cancel the request.

If the production is not running and the host item is enabled, the dialog box gives you the option to disable the host item or to cancel the request.

If the host item is disabled, the dialog box gives you the option to enable the host item or cancel the request.

- Select or clear the Enabled setting (as appropriate) and then click Apply. To restart a host item, first disable it and then enable it.

- Use the Stop, Start, and Restart buttons on the Action tab. Because the setting controlled by the Enabled check box is a setting stored in the production class definition, you cannot use it to stop, start, or restart a production that you cannot edit, for example because you lack sufficient pri vileges, or it is marked read-only due to being managed by source control system. The Stop, Start, and Restart buttons on the Action tab perform these actions without modifying the production class definition.

To enable, disable, or restart a selection of business hosts, do the following:

1. Select multiple business hosts in the Production Configuration page by using the Ctrl and Shift k eys. The Ctrl key

keeps any existing selection and either adds or removes the item from the selection. The Shift key allows you to select a contiguous set of one kind of business hosts—either Business Services, Business Processes, or Business Operations.

2. Once you have selected multiple business hosts, the right panel automatically switches to the Actions tab, which will

include Enable, Disable, and Restart buttons.

3. Select the button to enable, disable, or restart the selected business hosts.

Note:

You cannot disable a business process with a pool size of 0. The management portal does not allow this action because disabling it would stop all business processes with a pool size of 0, which use the same shared actor queue. If you want to disable only a single business process, you must first set its pool size to 1 or more. After you apply the settings, you can disable it. If you do want to stop all business processes using the shared actor pool, select Production Settings and set the Actor Pool Size to 0. Also see Pool Size and Actor Pool Size.

### 4.2 Changing the Class That a Business Host Uses

To modify a business host so that it is based on a different class:

1. Display the Production Configuration page:

2. Click the business host in the diagram.

3. Click the Actions tab.

4. Click Change Class. This button is visible only when you can edit the business host.

5. Select a new class.

### 4.3 Copying a Business Host

To create a copy of a business host within a given production:

1. Display the Production Configuration page:

2. Click the business host in the diagram.

3. Click the Actions tab.

4. Click Copy. This button is visible only when you can edit the business host.

5. Click Copy to create a copy of the selected business host.

A dialog box prompts you to enter a configuration name.

6. Enter a unique name and click OK.

When first created, the cop y has the same host class and settings as the original; only the name is different. Generally your
next step is to configure the cop y to make it unique. For example:

- If you have an incoming TCP business service that receives messages from a client application, and you want to receive messages from a similar application on a different application server, you can copy the first TCP service and configure the copy with the other server address.

- If you have a business process for one message routing interface, and you want a similar one but with alterations for y to route messages between different another interface, you can copy the first routing process and configure the cop sets of business services and business operations.

- If you have an outgoing email business operation that alerts a user, but you want to alert another user at different times of day, you can copy the first outgoing email operation and configure the cop y with the other email address.

The copy has no relationship to the original item; you can configure, enable, and disable each item independently .

Note:

The Copy command works only within the same production. You cannot copy a business host from one production to another.

Deleting a Business Host

### 4.4 Deleting a Business Host

To delete a business host within a given production:

1. Display the Production Configuration page:

2. Click the business host in the diagram.

3. Click the Actions tab.

4. Click Delete. This button is visible only when you can edit the business host.

This process removes this item from the production configuration. This action does not delete the business host class on which the business host is based.

### 4.5 Repairing an Error

If the class for a given business host is not available, the diagram displays the item with a red background. To fix the error:

1. Select the item.

2. Click the Actions tab.

3. Now either click Delete to remove the item or click Change Class to choose a class. This button is visible only when

you can edit the business host.

### 4.6 Viewing and Configuring Connections

When you click the status indicator of a business host, lines connect items as defined by the v alues in the Target Config Names setting or, in the case of a routing process, as defined by the associated Business Rule Name. The following figure
shows an example:

You can assign a business service Target Config Names by clicking its status indicator and dragging the pointer to a business process or operation until you see its status indicator highlighted. When you do so, the Production Configuration page displays

a dialog window requesting you to confirm the connection. If you confirm the connection, the page displays a applied message and the item is added to the list in the Target Config Names setting.

Settings

### 4.7 Working with Multiple Versions of a Business Host

During development, it can be convenient to include multiple versions of a business host in the production and then switch among them for testing.

Only one of them can be enabled at any time; when you enable one, InterSystems IRIS automatically disables any previously
enabled version.

To create and work with multiple versions of a host:

1. Add the first b usiness host as usual.

2. Add the next business host and provide the same configuration name as for the first one.

The production configuration still sho ws only one business host with the given name.

3.

If you are not in listing view, click the listing view icon

.

4. Select the business host.

Now the diagram displays a small box that indicates the number of items that have this name, as follows:

Also, the area above the diagram shows a drop-down list that you can use to select the specific item to w ork with:

By default, the enabled version is selected. If no host is enabled, the selected version is the first b usiness host that you added.

5. Use the Item list to select the version that you want to configure. Specify configuration details as usual and apply them.

6. Repeat if needed.

To understand why this is useful, consider the following: when testing or troubleshooting the production you might want to send messages by typing them at the console command line, or by reading data from files. But when running the production, you might intend for these messages to arrive from an external application via a TCP connection. Each means of obtaining input for the production requires a different business service host class.

### 4.8 See Also

- Configuring Settings (Legacy UI)

- This topic describes how to use the legacy Production Configuration page to configure settings.

- For information on performing these tasks with the new UI, see Configuring Settings .

### 5.1 Configuring Settings

To configure settings for a b usiness host:

1. Click the business host.

2. Click the Settings tab.

3. Expand and collapse the groups as needed to see the settings. You can also search for a setting.

4. Edit values as needed.

- Some configuration settings, tak e comma-separated lists to define their possible v alues. You can change these items either by editing the list directly or by selecting the check boxes of the desired values in the associated dropdown list. When you edit settings that use drop-down lists, be sure to click outside of the list to close it.

- Some configuration settings ha ve a magnifying glass icon next to them. You can click this to see more details of a selected value, or to open a new portal page for entering additional information. This depends on the type of setting you are editing.

See Settings in All Productions. Also see information on specific adapters and b usiness hosts.

5. Click Apply.

If the apply command is successful, you receive a Settings applied message.

InterSystems IRIS® validates the values for settings. If you provide a string value for a setting that requires a numeric value, InterSystems IRIS does not apply that value.

Similarly, to configure settings for the production, first click Production Settings. This step returns the focus to the production and changes the options on the Actions tab. Then continue as described in the previous steps.

In both cases, the changes are immediately saved and take effect immediately.

Configuring Settings (Legacy UI)

### 5.2 Color Coding

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

### 5.3 Searching for a Setting

To find a setting more easily , use the Search option. Enter text to show all settings whose name, type, category, or value contains the search string. Click the X icon to clear the contents of the Search box.

### 5.4 Getting Help for Settings

This page provides context-sensitive help. Hover the cursor over any setting name to display its help text as it appears in the Class Reference for the associated class property or click the setting name to display the help text in a separate pop-up window.

The property name appears beneath the localized setting name in this window if the name is different.

Also see Settings in All Productions, as well as other pages that discuss specific adapters and b usiness hosts.

### 5.5 Restoring a Setting to Its Default Value

To restore a setting to its default value:

1.

Click the default setting icon

on the Settings tab.

InterSystems IRIS then displays a dialog box with a table that displays the following columns:

Column

Description

Select check box

Shown only if the current value is not the default.

Setting

Target

Value

Name of the setting as displayed in the Management Portal.

Indicates if the setting applies to a host or to an adapter. This is blank for a production setting.

Current value of the setting.

Column

Description

Value Source

Source of the current value:

- class definition—the value is specified in the class on which this item is based.

- default setting—the value is a system default setting.

- production definition—the value is specified in the production definition.

Default

Default value for this setting.

Default Source

Source of the default value:

- class definition—if you see this, there is no system default for this setting.

- default setting

2. For each setting that you want to change, select the check box.

See the notes for Value Source.

3. Click OK. The property label changes color depending on the Default Source. See Understanding the Color Coding for

Settings.

Or, if you make a mistake and want to return to the original values, click Cancel; the settings refresh to the previous
values and the dialog box closes.

4. Click Apply to save all your changes.

### 5.6 See Also

- Defining System Def ault Settings

- Understanding the Color Coding for Settings

- Settings in All Productions
