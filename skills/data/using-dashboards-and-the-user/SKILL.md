# Using Dashboards and the User Portal

This page introduces the InterSystems IRIS® data platform User Portal, which is meant for end users of InterSystems IRIS
Business Intelligence.

Be sure to consult InterSystems Supported Platforms for information on system requirements.

### 1.1 Purpose of the User Portal

The User Portal is intended for direct use by end users and is designed to enable you to do the following tasks:

- View and use dashboards and pivot tables, all containing key information. This information can include production business metrics. For Business Intelligence users, this information presents aggregated views of your data that you can investigate in various ways.

- You can organize these items into folders for easier management. Also, you can attach keywords to these items, so that you can find items ag ain more quickly.

- Share your dashboards and pivot tables with other users.

- The User Portal is a shared environment. That is, the same items are visible to all users who have access to the User Portal for a given namespace.

- Create dashboards, which generally display pivot tables and other elements such as meters and scorecards. Dashboards are typically intended to address specific b usiness needs.

Access the Analyzer, in which you can create pivot tables or perform ad hoc analysis of data.

Share and access links to web pages.

- Manage your workflo w tasks.

### 1.2 Logging On to Business Intelligence

In a supported browser, go to the following URL, using the <baseURL> for your instance:

http://<baseURL>/csp/samples/_DeepSee.UserPortal.Home.zen

Where samples is the namespace that you are using. When prompted, enter your InterSystems IRIS username and password.

#### 1.2.1 Selecting a Preferred Language

This user interface can be displayed in different languages. Initially, the default preferred language (that is, the session language) is the language specified for the bro wser, or English if the browser language is not supported.

To select your preferred language, select About and then select an option in the list Preferred language for this session.

Note that after you select a language here, the system continues to use that language even if you change the language used by the browser.

### 1.3 Introduction to the User Portal

The following shows an example of the User Portal:

Notice the following elements in this page:

- The left area contains worklists, which are rectangular areas that contain tools. For details, see Using Worklists in the
User Portal.

- The main area on the right shows the public Business Intelligence pivot tables, dashboards, and other items.

Here you can open items, delete items, and mark items as favorites. You can also expand or collapse the folders. The top area provides a search option.

For a dashboard, this area displays the title of the dashboard, if it has a title; otherwise, this area displays the name of
the dashboard.

This area does not display items that are marked as private.

For workflo w users, the main area also displays an item labeled Workflow Inbox.

The Menu link in the upper left contains options to create and open dashboards and pivot tables and perform other tasks in Business Intelligence.

If you are assigned to the %Developer role, this menu includes an option to access the Management Portal.

About Pivot Tables and Dashboards

The Home link at the top displays this page.

The Logout link enables you to log out.

- The User Portal is a shared environment. Many of the items you see are also visible to other users.

- 1.4 About Pivot Tables and Dashboards

- Pivot tables are central to Business Intelligence; they select and aggregate data. The following figure sho ws an example
pivot table that shows the number of patients and the average allergy count per patient, grouped by age and gender.

Using this example as a reference, let us discuss the key terms in Business Intelligence:

- A level is used to group the source data. A level has members. Each member, in turn, corresponds to a specific set of records in the source data.

- For example, the Age Group level has the members 0-29, 30-39, and 60+. The Gender level has the members Female and Male.

A measure is a value displayed in the body of the pivot table; it is based on values in the source data. For a given
context, a measure aggregates the values for all applicable source records and represents them with a single value.

For example, the measure Patient Count is the number of patients, and the measure Avg Allergy Count is the average number of allergies per patient.

The preceding example shows a preview of a pivot table within the Analyzer, which provides a large set of tools for modifying the pivot table, exporting to Microsoft Excel, toggling to a chart format, and so on.

You typically see a pivot table within a dashboard, as follows:

Notice that this dashboard includes multiple filters (sho wn in the Filters box), which you can use to filter the items on this dashboard.

Dashboards can include other kinds of elements, including meters and scorecards. A scorecard shows multiple rows of
data in a tabular format that also includes features such as value-dependent lamps and arrows. For example:

A meter shows one or more values in graphical objects like the following:

Summary of Options in the User Portal

For more information on dashboards, see Using Dashboards.

### 1.5 Summary of Options in the User Portal

In the User Portal, you can do the following tasks, depending upon your permissions:

- Send alerts to other users.

- Note:

- These alerts are unrelated to production alerts.

Review alerts that you have received.

Send email to other users (if your system is configured for this).

- Manage workflo w tasks.

- Mark items as favorites, for easy access.

- Create, modify, view, and work with dashboards.

- For information on creating and modifying dashboards, see Creating Dashboards.

- Create, modify, view, and work with pivot tables.

- For information on creating and modifying pivot tables, see Using the Analyzer.

- Add links to web pages.

Delete public items displayed in the User Portal.

Display the Analyzer and perform additional analysis there. See Using the Analyzer.

### 1.6 Security

The system has a formal mechanism for managing access to Business Intelligence functionality, Business Intelligence items, and your data. This mechanism is based on the underlying InterSystems IRIS security framework. This section summarizes how this mechanism affects you.

For details, see the Implementing InterSystems Business Intelligence.

#### 1.6.1 Security for Functionality

The User Portal and the Analyzer are secured as separate entities. You may or may not have read and write access to both these components. For example, you might have both read and write access for the User Portal (which would let you view and create dashboards), but only read access for the Analyzer (which would let you change a pivot table but not save the changes).

#### 1.6.2 Security for Pivot Tables and Dashboards

Pivot tables, dashboards, and other items displayed in the User Portal are known as folder items and can be secured via
resources. This works as follows:

- An administrator performs the following setup:

– Creating resources in the Management Portal.

– Creating roles in the Management Portal. These roles can have either READ permission on a resource or both

READ and WRITE permissions on a resource.

– Assigning users to roles, which enables them to read (or read and modify) the items or items associated with a

resource.

The administrator should then notify the Business Intelligence users about the available resources and how they are to be used.

- When you save a folder item, you can type the name of the applicable resource into the Access Resource field.

#### 1.6.3 Security for Model Elements

Business Intelligence model elements can also be secured via resources. This works as follows:

- An administrator creates resources and roles, and assigns users to roles as described in the previous section.

- Developers specify the resource (if any) that secures each cube, subject area, and KPI (key performance indicator).

This page describes how to use the basic features of the InterSystems User Portal.

Note:

Alerts in the User Portal are unrelated to production alerts.

### 2.1 Displaying Folder Items

The main area of the User Portal displays the dashboards and pivot tables in this namespace, with different icons for dashboards and pivot tables. This item can also display links to web pages. All these items are known as folder items, because they can be grouped into folders (which are used primarily for security).

At the top of this area, use the Covers and List options to display Covers View and List View, respectively.

You can also use Menu > Find Dashboard... to open a dashboard.

#### 2.1.1 Covers View

The following shows an example of the Covers View:

When you hover the cursor over a cover, the system displays an arrow on the cover, as follows:

If you select the cover arrow, the system displays the dashboard or other item.

If you select anywhere except for the arrow, the system displays an informational dialog box like the following:

Displaying Folder Items

To close this dialog box, select the X in the upper right or select the screen outside of this dialog box.

#### 2.1.2 List View

The following shows an example of the List View:

This view groups folder items by the folders to which they belong.

#### 2.1.3 Options Available in the Main Area of the User Portal

In the main area of the User Portal (the right area), you can do the following:

- (Only in List View) Expand or collapse a folder. To do so, select the triangle to the left of the folder.

Covers View does not display folders.

- View an existing folder item. To do so, select the cover arrow (in Covers View) or select the name of the item (in List
View).

- Then, for dashboards, see Using Dashboards for information on your options. If you have the appropriate permission, you can then edit the dashboard. See Creating Dashboards.

- Or, for pivot tables, if you have the appropriate permission, you can then edit the pivot table. See Using the Analyzer.

- Search for an item. To do so, type your search text into the box at the top of the right area and then select Go.

- The system finds all items whose names or k eywords include the given text; the search is not case-sensitive.

Display different groups of folder items.

For details, see the next section.

Delete a folder item. In Covers View, select the cover and then select the X button. In List View, select the X button in the row for that item.

In either case, the system prompts you to confirm this action.

Mark a folder item as a favorite. In Covers View, select the cover and then select the Favorites button View, select the Favorites button in the row for that item.

. In List

### 2.2 Visibility of Folders and Folder Items

The User Portal lists only a subset of the folders and folder items. You can use the Show options to display different groups of folder items.

The options are as follows:

- All — Shows all public folders and items. This is controlled by the Public setting of an item.

Important:

Note that the Public setting controls only whether the item is displayed in the User Portal. It does not otherwise control access.

- Personal — Shows all public items that you own. This is controlled by the Owner setting of an item. Note that, by default, the owner of an item is the InterSystems IRIS® data platform user who created it.

- Shared — Shows all public items that you do not own and that have assigned resources to which you have permission. This is controlled by the Resource setting of an item.

- Public — Shows all public items that you do not own and do not have assigned resources.

The following table lists all the possible variations and indicates the visibility of the folders and folder items, depending
on what you choose for Show:

Marked as
Public?

Yes

Yes

Yes

Yes

No

Owner

Resource

User Portal Displays Item to You?

You

Any

Yes (if you select All or Personal)

Someone else

No resource

Yes (if you select All or Public)

Someone else

Resource that is available to you

Yes (if you select All or Shared)

Someone else

Other resource

No

Any

Any

No (but the item might be available via the Menu, depending on its owner and resource)

Similarly, to define an item so that only you can see it, do the follo wing:

- Set yourself as the Owner.

- Specify a Resource that is available only to you.

- Optionally select Public to display the item in the User Portal.

For background information, see Security in Business Intelligence.

### 2.3 Customizing Covers

When you display the Covers View in the User Portal, the system displays a rectangular cover for each item, and there is
a default cover for each type of item. For example, the default cover for a dashboard looks like the following example:

To customize a cover:

- If you are currently viewing the User Portal, first select the View Covers option. Then select the cover (but do not select
the arrow that is temporarily shown in its bottom area). the system displays an information dialog box:

Then select the Cover Design button

.

- (For a dashboard) If you are currently viewing the dashboard, select Menu > Design Book Cover.

In either case, the system displays the Book Cover Editor, which looks like this:

Note the following:

- To customize part of a cover, either select a tab at the top or select an area in the cover preview. In either case, the left area then displays a list of options.

- To control the size of the cover preview, use the 1x, 2x, and 3x buttons at the right.

- To undo a change, select Undo (not shown here).

- To clear all customizations and restore the default cover, select Clear.

- To close the editor without saving changes, select Cancel.

- To save changes and close the editor, select Save.

- To upload an image file, select Upload Image.

- The system copies the image files to the directory InterSystems IRIS namespaces.

install-dir/CSP/broker/covers. The image files are a vailable in all

To hide the list of options on the left, select the < button.

#### 2.3.1 Cover Parts

A cover has the following parts that you can customize separately:

- Background — The entire area within the rectangle, including the areas behind the header and footer (which can be hidden).

- Header — A rectangle at the top. By default, this is shown in a contrasting color and displays the type of the item (dashboard, pivot, and so on).

- Title — By default, this is displayed below the header and displays the name of the item (dashboard, pivot, and so on).
For a dashboard, this displays the dashboard title, if any; otherwise it displays the dashboard name.

- Image — An image included on the cover. By default, this image is in the middle of the page. The system uses a default image for each type of folder item.

- Subtitle — By default, this is blank. The default position is below the image.

- Footer — A rectangle at the bottom. By default, this is shown in a contrasting color and displays the owner of the item.

#### 2.3.2 Cover Options

The following table summarizes the options available for each part:

Option

Notes

Available for
Background?

Available
for Image?

Available for
Header,
Title,
Subtitle, and
Footer?

Visible

Text

Color

Image

Background

Make Image Full Size

Font

Font Size

Text Style

Align

Top

Optionally clear this option to hide this element

Type a string or select a token to represent specific text from the selected item

yes

no

Select a color to use for the text

no

Select an image or type the URL of an image

Select a color for the fill pattern for this element

Select this option to make the image fill the background, if it does not already do so

Select a typeface

Use the slider to specify the font size or select the check box to reset to the default

Select a text style

Select an option to make this element left-aligned, centered, or right-aligned

Use the slider to specify the top position of this element or select the check box to reset to the default

yes

yes

yes

no

no

no

no

yes

yes

yes

yes

no

yes

no

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

no

yes

yes

yes

yes

yes

Option

Notes

Left

Height

Width

Margin

Padding

Opacity

Radius

Use the slider to specify the left position of this element or select the check box to reset to the default

Use the slider to specify the height of this element or select the check box to reset to the default

Use the slider to specify the width of this element or select the check box to reset to the default

Use the slider to specify the margin around this element

Use the slider to specify the padding around this element

Use the slider to specify the opacity of this element

Use the slider to specify the radius of the corners of this element

Customizing the Covers View

Available for
Background?

Available
for Image?

Available for
Header,
Title,
Subtitle, and
Footer?

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

yes

### 2.4 Customizing the Covers View

You can customize the font and colors used in the background of the Covers View in the User Portal. For example:

To do so:

1. Select the < button at the left.

It is not necessary to be in Covers View.

2. Select Background.

3. Specify the following options:

- Color — Specify the font color for labels in the background (such as the default category name, All, shown here).

- Background — Specify the color for the background.

- Font — Specify the typeface for labels.

- Font Size — Specify the font size for labels.

- Text Style — Specify the text style for labels.

Or select Reset Styles to remove all customizations.

These changes are visible to all users in this namespace.

### 2.5 Using Worklists in the User Portal

The home page of the User Portal always includes two worklist areas on the left, and these display different worklists depending on your site configuration. F or any worklist area, the upper right corner might display icons to indicate which
worklists it can display. For example:

If no icons are shown, this worklist area can display only one worklist.

The highlighted icon indicates which worklist is currently displayed in the worklist area. You can select a different icon to display the corresponding worklist in this area instead.

For the User Portal, the available worklists are as follows:

- The Alerts worklist displays recent alerts sent to you. For example:

Using Worklists in the User Portal

For information, see Viewing Alerts.

- The Details worklist displays details for a pivot table or dashboard. For example:

To display details for an item, select the icon to the left of the item name in the main area of the User Portal. Then the system refreshes the Details worklist.

- The Favorites worklist displays any items that you have marked as favorites. For example:

- The Recent items worklist displays items that you have recently accessed, in descending order by the date you accessed
them. For example:

In all cases, to open an item, select it. To remove an item from a worklist, select the X button.

### 2.6 Hiding or Showing the Worklists

The upper right corner of the main area displays a << button that you can use to toggle the display of worklists:

Select the << button to hide the worklists. Then select the >> button to display them again if needed.

### 2.7 Registering or Unregistering for Alerts

To change whether you are registered for alerts:

1. Access the User Portal home page.

2. Select Menu > Register for Alerts.

3. Specify the following options:

- Full name — Type the full name that you want other users to see when they send alerts.

- Alerts enabled — Select this option to receive alerts.

4. Select OK.

### 2.8 Sending an Alert

You can send alerts to other InterSystems IRIS Business Intelligence users, if those users have registered for alerts. To do
so:

1. Open a dashboard that contains the data about which you want to send the alert.

2. Select Menu > Send Alert.

3. Specify the following options:

- Send to — Select each user who should receive this alert.

- Subject — Optionally type a short message to display in the Alerts worklists of the other users.

- Priority — Optionally select a priority; this affects how the alert is displayed. The default is Normal priority.

- Comments — Optionally type a longer message.

Viewing Alerts

4. Select OK.

### 2.9 Viewing Alerts

To view your alerts:

1.

In a worklist area, select the Alerts button

.

You might see something like this:

Note the following items:

- A star on the left indicates that you have not yet opened this alert.

- High-priority items are shown in red font, normal-priority items are shown in black font, and low-priority items are shown in gray font.

2. Select anywhere in the row for an alert to open it. The system then opens the associated dashboard and displays the

alert details in the Alert Details worklist, as follows:

### 2.10 Sending Email

From within a dashboard, you can send email that contains a link to the dashboard, if your system is configured for this.
To do so:

1. Open a dashboard that contains the data about which you want to send the alert.

2. Select Menu > Send Email.

If this option is not present, then your system is not configured to support email.

3. The system then does one of the following:

- Displays the default email client on your machine, with a message that contains a link to the dashboard.

- Edit the message, specify one or recipients, and send it as usual.

Displays a dialog box.

Type the email address of the recipient, type a brief message to include along with the generated link, and select
OK.

If you have previously sent email, you can choose a recipient from the Send to drop-down list.

#### 2.10.1 How Business Intelligence Supports Email

Your can be configured to support email in either of tw o ways:

- It can use client-side email. In this configuration, when you send email, the system accesses the def ault client-side email program such as Microsoft Outlook. You use this to send email in the usual way, and you have access to your address books.

- It can use server-side email. In this configuration, when you send email, you must type the email address of the recipient. The system routes the message to the configured email serv er.

It can also be configured not to support email. Consult your implementers, who should read Implementing InterSystems
Business Intelligence.

### 2.11 Managing Workflow Tasks

If you are a workflo w user, the main area of the User Portal displays an item labeled Workflow Inbox.

You use this to manage your workflo w tasks. If you select Workflow Inbox, the User Portal displays something like the
following:

Managing Workflow Tasks

This list shows all unclaimed workflo w tasks (marked as NEW) and all open tasks assigned to you.

To manage a workflo w task, select it to see its details, which are then displayed in the lower area of the page:

This example shows the built-in buttons and one custom editable field ( Comments); you might see additional buttons and
fields, depending on the task definition.

For a selected task, you can do any of the following:

- Take ownership of the task. To do so, select Accept (not shown in the previous figure, in which the task has already been accepted). This indicates that you intend do perform the associated work. The task becomes assigned and is not longer visible in the Workflo w Inboxes of other users.

- Give up ownership of the task. To do so, select Relinquish. This causes the task to become unassigned and thus visible to all users in the same workflo w role.

- You can do this action and the following actions only if you own the task.

Indicate that you completed the task. To do so, select Corrected.

The task is then removed from the list.

The workflo w process might then generate additional tasks, depending on how it is defined.

- Mark the task as ignored. To do so, select Ignored.

The task is then removed from the list.

- You use this option to indicate that you have encountered an error condition (such as not being able to contact the customer) and therefore the task cannot be completed.

- Perform other actions by selecting other buttons in this area. The preceding figure sho ws only the built-in action items.

Enter values into editable fields. The preceding figure sho ws one custom editable field ( Comments).

The purpose of these fields is to con vey information to the next person who receives the task, to add information to the permanent record, or both. Therefore, be sure to provide meaningful entries.

### 2.12 Creating Links to Web Pages

In the User Portal, you can also create links to web pages. To do so:

1. Select the + button at the top.

Or select the < button at the left and then select Add.

2. Select Add Link.

3. Specify the following options:

- Folder — Specify the folder to contain this item.

- Also see Preparing for Folder Item Localization in Implementing InterSystems Business Intelligence.

Name — Specify the name of this item.

Also see Preparing for Folder Item Localization in Implementing InterSystems Business Intelligence.

Note that this name is used (along with Folder) as the logical name of the item; the system displays this logical
name when you use the Save As option, for example.

- Title — Specify the title of the dashboard.

If you specify a title, the main area of the User Portal displays the title. Otherwise, it displays the name.

Also see Preparing for Folder Item Localization in Implementing InterSystems Business Intelligence.

Link URL — Specify the URL.

Owner — Specify the InterSystems IRIS user who owns this item. If an item has an owner, then only the owner
can specify the Access Resource value for the item; see the next item.

Access Resource — Specify the resource that is used to control access to this item. See Visibility of Folders and
Folder Items.

Public — Select this option to control whether this item is displayed in the User Portal main area.

Important:

This option does not control access to the item. Access is controlled instead by the Owner and Access Resource options, discussed earlier in this list.

Description — Briefly describe the item.

Keywords — List any keywords or phrases to help you find this item later . Specify a comma-separated list of keywords or phrases.

These keywords are displayed in the User Portal in List View.

Category — Specify the category to which this item belongs.

- If you specify categories for items, Covers View groups items by category. For example:

- Creating Links to Web Pages

- This page reviews the contents of the dashboards that you may already have in your system. It is intended as an orientation to the possible contents of your dashboards. For information on using the elements described here, see Using Dashboards.

- 3.1 Overview of Dashboards

- The following example shows a sample dashboard:

- A dashboard consists of the following areas:

- The upper left displays the name of the dashboard and (if defined) its title.

- Depending on the system configuration and on the indi vidual layout of a dashboard, a dashboard can include zero, one, or two worklist areas on the left. For any worklist area, the upper right corner displays icons to indicate which
worklists it can display. For example:

- The highlighted icon indicates which worklist is currently displayed. You can select a non-highlighted icon to display the corresponding worklist in this area instead.

The Filters worklist is specific to the dashboard. To access this, select the Filters icon

. For example:

- The right area contains one or more widgets. Each widget is a rectangular panel that displays data in some form.

### 3.2 Widget Variations

This section shows the contents of different types of widgets that you might see in your dashboards.

#### 3.2.1 Pivot Table Widgets

A pivot table widget displays data in one of three formats:

- As a table with aggregated values. For example:

- As a chart. For example:

- As a listing, which is a table of the lowest-level values. For example:

If there are more than 100 rows, the bottom area displays buttons that you can use to page through all the rows.

#### 3.2.2 Scorecard Widgets

A scorecard widget displays one or more rows of data in a tabular format that also includes features such as value-dependent
lamps and arrows. For example:

#### 3.2.3 Meter Widgets

A meter widget displays one or more values, each in a graphical object as follows:

The preceding picture shows a speedometer. The system also supports text meters. For example:

#### 3.2.4 Map Widgets

A dashboard can include a map widget like the following:

The highlighted points typically correspond to locations that are relevant to your business.

#### 3.2.5 Calendar Widgets

A dashboard can include a calendar widget like the following:

This widget is included purely as information; it is not connected to your data.

#### 3.2.6 Controls Widgets

A controls widget consists only of toolbar controls and has no main body content. The following shows an example:

#### 3.2.7 Custom Widgets

A dashboard can also include custom widgets called portlets. The following shows an example:

### 3.3 Data Sources for Widgets

Most widgets use a data source, which is one of the following:

- A pivot table. Pivot tables are created in the Analyzer. A pivot table is a query that is created by drag and drop actions.

- In some cases, you can launch the Mini Analyzer and make local changes to the pivot table. Changes do not affect other widgets, other dashboards, or other users. For details, see Other Tasks.

A KPI (key performance indicator). A KPI is a more advanced query created by a programmer.

All of these data sources can be displayed in pivot table widgets, scorecard widgets, and meter widgets.

### 3.4 Widget Basics

A widget might or might not include a title bar with buttons, as follows:

The title bar may or may not include a title.

Most widgets include scroll bars when necessary. A pivot table instead includes paging buttons like the following example:

If a pivot table displays nested rows and if there are more than 100 rows, the system initially accesses the first 100 ro ws and displays the Show All button instead of these paging buttons. If you select the Show All button, the system accesses all the rows and then displays the paging buttons.

Depending on how the dashboard is configured, the lo wer right corner of each widget can include a resize handle:

Locations of Controls and Buttons

### 3.5 Locations of Controls and Buttons

A dashboard can include controls and graphical buttons. Depending upon the dashboard design, you see these items in
either or both of the following locations:

- In the Filters worklist of the dashboard. For example:

These items typically affect the entire dashboard.

- In the toolbars of the widgets included in the dashboard. For example:

These items typically affect only the widget in which they are displayed, but they could possibly affect other widgets.

Using Dashboards provides information on using these options.

### 3.6 Empty Widgets

There are two scenarios in which you might see empty widgets.

In the first scenario, a widget (or the underlying pi vot table, if applicable) has been deliberately configured not to automatically execute when you open the dashboard. (This configuration can be useful when a pi vot table uses a long-running

query.) In this scenario, the widget should include a refresh button contents. If there is no such button, contact the owner of the dashboard.

, which you use to force the widget to display its

In the second scenario, if the system cannot find some of the data that the dashboard uses, the system displays as much of
the dashboard as possible. For any affected widget, the system displays something like this:

This typically indicates that someone has either renamed or deleted the data source used by this widget; it could also indicate
that you do not have permission for the data in this widget. Contact the creator of the dashboard or reconfigure the widget
yourself; see Creating Dashboards.

This page describes how to work with the dashboards that you may already have.

### 4.1 Toggling the Display of the Worklists

Depending on the system configuration and the configuration of the dashboard, a dashboard might include zero, one, or two worklist areas on the right.

You can temporarily toggle the display of any worklists in the dashboard you are currently viewing. To do so, select Menu > Hide/Show Worklists. If you save the dashboard, this change is not saved.

### 4.2 Managing the Widget Windows

This section describes how to manage the size and placement of widgets. All these changes are discarded unless you do
one of the following:

- Select Menu > Save My Settings. This option saves your changes locally so that only you can see them.

- Save the dashboard itself, as described in Creating Dashboards.

#### 4.2.1 Window Buttons

In all widgets, to control the display of the widget window, use the buttons in the title bar:

Button

Action

Temporarily hide the widget. (To restore it, redisplay the dashboard.)

Maximize the widget.

#### 4.2.2 Resizing Widgets

To resize a widget, drag its resize handle in the lower right corner, if present:

Your ability to resize widgets is also affected by the Scalable Grid; see the next section.

#### 4.2.3 Moving Widgets

Depending on how the dashboard is configured, it may be possible to mo ve the widgets on it. There are three different
possibilities:

- The Scalable Grid option is enabled. In this case, there is an invisible grid of possible positions for the widgets. You can move widgets and resize them according to this grid.

- If you resize the dashboard, all the widgets are automatically resized. Scalable Grid is the only option that supports this behavior.

- The Snap Into Place option is enabled. In this case, if a dashboard contains only one widget, that widget is automatically positioned in the upper left and cannot be moved. If a dashboard contains at least two widgets, you can reposition them. To move a widget to the right, left, top, or bottom of another widget, select in its top bar and drag.

Neither option is enabled. In this case, you can freely reposition and resize widgets.

### 4.3 Filtering Data

Many dashboards include controls that you can use to filter the data sho wn in one or more widgets. Typically, if a control is in the Filters worklist, it affects the entire dashboard. In contrast, if it is in a widget toolbar, it typically affects only that widget.

Most filter controls are sho wn as searchable controls. The details depend on the type of data used in the control, as well as
the source of the data; the following sections explain the variations.

Note:

In some cases, a filter control might be read-only . In this case, its purpose is simply to tell you how the data is filtered.

#### 4.3.1 Using a Filter Control

A filter control might initially be lik e this:

To use this control, select the Search button

. In most cases, the system then displays something like this:

If this menu includes the word Required, then it is necessary to choose at least one item. In this case, the drop-down menu
does not list the All choice. The following shows an example:

In this case, if you try to close the drop-down menu without selecting an option, the system displays a pop-up message saying that a value is required.

The Range option is not available if the data source for the widget is a KPI. The following subsections show other variations.
In these filter controls, depending on their e xact nature, you can do the following:

- Type into the search box and press Tab.

If you do, the control is refreshed to display only members that include the string that you typed. For example:

- Select an item or hold down the Ctrl key and select multiple items.

- In some cases, it is not possible to select multiple items.

- Select Exclude to exclude the selected item or items.

Select Range and then specify an inclusive range of members. When you select Range, the control changes to display two drop-down lists. In each drop-down list, select a member.

When you are done, select the check mark button to accept your selections. Or select the X button to discard them.

The widget or dashboard may or may not be refreshed immediately, depending on the dashboard configuration. Look for

a standard Refresh button you must select that button to see the change due to the filters.

or a button labeled Refresh, Rerun, or so on. If the dashboard has such a button, typically

#### 4.3.2 Filter Control for a Time Level

Depending on the data source, if the filter refers to a time le vel, the list includes a NOW member, which always refers to the date on which the pivot table was run. (More specifically , NOW refers to the applicable member of the time level for the date on which the pivot table was run. For a year filter , NOW refers to the year, for a year and month filter , NOW refers to the year and month, and so on.)

For example, consider the following:

In this case, the NOW member refers to the current year, when this pivot table is run. For another example:

In this case, the NOW member refers to the current year and current month, when this pivot table is run.

Note:

The NOW option is not available if the data source for the widget is a KPI.

Day levels are handled differently; see the next subsection.

For some kinds of time levels, if you click the NOW member and click Range, the system displays the following:

Here, you can specify a range of dates relative to the current date. To do so, type into the boxes shown on the right. For each box, to specify a date in the past, enter a minus sign (-), followed by an integer n. This specifies a date n time units in the past, where the time unit is determined by the kind of time level (in this case, years). Similarly, to specify a date in the future, specify a plus sign (+) followed by an integer n.

For example, the following filter selects a range of dates from fiv

e years in the past until now:

#### 4.3.3 Filter Control for a Day Level

Depending on the data source, if the filter refers to a day le vel, the system shows the following control instead of a list:

If you select Range, the system displays two calendars, side by side. Below each calendar, the filter displays a NOW option. NOW represents the current date (that is, the date when the dashboard queries are executed. The following shows the NOW
options:

If you select NOW, you can specify an optional offset, which specifies an inte ger number of days before or after NOW. For example, NOW – 365 represents the date that is 365 days before the dashboard query was executed.

#### 4.3.4 Filter Control for a Measure

If the filter refers to a measure, the system sho ws the following control instead of a list:

In this case, select an operator from the drop-down list and type a value into the box to its right.

#### 4.3.5 Filter Control for a Computed Dimension

If the filter refers to a computed dimension, the system sho ws the following control instead of the usual drop-down list:

In this case, you can either select and item in the list or select Reset to clear the selection.

A computed dimension is a dimension whose members are defined at runtime, typically via SQL SELECT statements.

#### 4.3.6 Filtering via OnClick

In some cases, if you select a row in a widget, that widget filters another widget. This is a type of onclick control.

For example, consider the following dashboard:

For this dashboard, when you select a ZIP code row in the left widget, the system automatically refreshes the right widget.
For example:

To clear the selection, select the left column header (for example, select above the 32006 cell).

#### 4.3.7 Data Source Differences

For any widget that includes filter controls, if the data source is a KPI, a filter control has some or all of the follo wing
limitations:

- Does not include a Range option.

- Cannot be displayed in the calendar format.

- Does not include the system NOW option. (It is possible, however, for a KPI to include a filter option labeled NOW with similar behavior.)

- Does not necessarily enable you to select multiple items.

### 4.4 Understanding the Effects of Filters

In most cases, a filter includes or e xcludes members of a level. Each member is a set of base records, so a level filter includes
or excludes records that correspond to the members you choose; the behavior is the same regardless of the contents and
organization of the pivot table.

For example, consider the following dashboard:

This dashboard contains three pivot table widgets, each of which displays a different pivot table. Each pivot table includes
a total line. Each widget includes a level filter that uses the ZIP level (this is for demonstration purposes; more commonly,
the Filters box would include a single filter that applied to all widgets).

Consider what occurs when we choose the same ZIP code in each of these widgets:

Understanding the Effects of Filters

The first widget sho ws patients grouped by ZIP code. This widget now shows one row, corresponding to the selected ZIP code. The other ZIP codes are no longer shown, because this pivot table is not configured to display null ro ws.

The second widget shows patients grouped by home city. This widget now shows the three cities that correspond to the selected ZIP code. The other cities are no longer shown, because this pivot table is not configured to display null ro ws.

The third widget shows patients grouped by age groups. This widget displays all age groups, because the selected ZIP code includes patients of all ages.

Notice that the total count is the same in each pivot table.

In each case, when we select a ZIP code, the system selects only patients whose home address is in that ZIP code.

A measure filter refers to the v alue of a measure, instead of referring to members of a level. For example:

A measure filter e xamines each base record and includes or excludes it, depending on its value for the given measure. For
example, consider the following dashboard:

Consider what occurs when we filter by Test Score in the same way in both widgets:

The first widget sho ws patients grouped by patient group. This widget no longer shows the patients in group None, which
contains the patients who have no test score; this row is gone because this pivot table is not configured to display null ro ws.

The second widget shows patients grouped by favorite color. This widget shows all the same rows it used to show, because there are patients with the selected score or higher in all these groups.

Notice that the total count is the same in each pivot table.

### 4.5 Sorting Data

In a pivot table widget, you can sort the rows by the values shown in any data column. To do so, double-click the column
header. For example:

The first time you double-click the column header , the table is sorted in ascending order, by the values in that column, as shown in the preceding example.

If you double-click the column header again, the table is sorted in descending order instead. If you double-click a third time, the sorting is removed and the default order is restored.

In some cases, you might see a drop-down list that you use to control the sorting of the rows or column. Select Decreasing, Increasing, or Sort (removes the sorting). In this case, the control considers the values in the first data column or the first data row, as appropriate.

### 4.6 Specifying the Row or Column Count

In some widgets, you can specify how many rows or columns are shown. For example:

For another example:

Changing the Display Type

Type or select a value as needed.

### 4.7 Changing the Display Type

In some widgets, you may be able to toggle the display between table format and chart format. To do so, use the following
buttons:

Button

Action

Displays the widget in table format.

Displays the widget in chart format.

Note that for a chart, only the first hundred chart items are displayed.

Or the widget might include a control that lets you choose the chart type. For example:

In this case, select an option from the drop-down list. The widget is then redisplayed in the selected format.

Or the widget might include buttons that let you switch to specific types. F or example:

In this case, when you click a button, the widget is redisplayed in the selected format. From left to right, the buttons shown here display the data as a pivot table, a bar chart, or a column chart. There are similar buttons for other chart types.

### 4.8 Using the Chart Zoom Feature

For some kinds of charts, you can zoom in and out, to see more or less data at once. To do so, select the zoom in button
(+) in the lower left corner:

The chart then shows less data and includes arrow buttons that you can use to scroll left and right. For example:

### 4.9 Using Combo Charts

A combo chart provides two features that are not available in other charts:

- It can have multiple y-axes.

- It can use different display types for different measures.

The following chart demonstrates both features:

Using Combo Charts

Notice that the y-axis is labeled Patient Count. The bars that display the Patient Count measure are scaled to match the values on this axis. In contrast, the bars that display Avg Enc Count do not correlate with the y-axis — these bars are correctly proportioned with respect to each other, but are scaled overall to fit within the chart.

To use a combo chart, select the box next to the name of a series, in the key. For example, if we select the box next to Avg
Enc Count, the labels on the y-axis change as follows:

### 4.10 Displaying Listings

If a widget includes the Listing button you select. In some cases, the listing button might appear as a button with text (such as Toggle Details).

, you can display a listing, which shows the lowest-level data for the context

To display a listing:

1. Select one or more items.

- For a table, select one or more cells.

To select multiple cells, hold down the Shift key while selecting the cells.

To select an entire row, select the row label on the left. To select an entire column, select the column header.

The listing option is not available for cells in a total row or a total column.

- For a chart, select a single chart item. For example, select a bar in a bar chart.

The selected item or items are highlighted.

2.

Select the Listing button

.

The widget then toggles to list the lowest level records for the selected cells. For example:

If there are more than 100 rows, the bottom area displays buttons that you can use to page through all the rows.

The check boxes enable you to select rows so that you can perform actions (particularly custom actions) that use those rows as input. Actions are usually shown as buttons at the top of the widget.

If your pivot table uses a subject area that includes an NLP (Natural Language Processing) measure, the NLP Measure

Value

button might be available; for details, see Displaying NLP Measure Values for Selected Facts.

3.

To toggle back to the original view, select the Table button

.

#### 4.10.1 Map Listing Variation

In some cases, the widget displays a Map Listing button:
locations. For example, from the HoleFoods sample:

. If you select this, the system displays a map that shows

Displaying Listings

In this case, the displayed locations are locations of the sales for the selected records.

Map listings are also known as geo listings.

#### 4.10.2 Displaying NLP Measure Values

When you display a listing for a pivot table that uses a subject area that includes an NLP measure, the listing might include

a column that displays the NLP Measure Value

button. For example:

If you select this button, the system then displays a page like the following:

This page displays (by default), the complete text of an NLP measure, for that record.

On this page, you can do the following:

- Select a tab to display the text for a different record.

- Select the most relevant sentences of this text. To do so, type an integer into Summary length and then select summarize.

- The system then displays that number of sentences, starting with the most relevant sentence, as determined by the
Analytics Engine.

Highlight specific kinds of elements, as determined by the Analytics Engine. By default, nothing is highlighted.

Note the following points:

- A dictionary term is a word or phrase found in a specific dictionary loaded into the system. In general, a dictionary defines a mapping that typically associates multiple synon yms with each other. You can select the dictionary or dictio-
naries to consider, among the available dictionaries in your system; these are specific to your implementation

- A dominant term is a unit of text that is dominant within this text, as determined by the Analytics Engine. To understand the choices, it is necessary to review some concepts related to text analysis.

In text analysis, a key concept is the entity. The Analytics Engine processes the given text and identifies the entities in it. An entity is a minimal logical unit of text. It is a word or a group of words. Example entities are clear skies and clear sky. The Analytics Engine language model identifies tw o kinds of entities: relations and concepts. A relation is a word or group of words that join two concepts by specifying a relationship between them. A relation is commonly but not always a verb. A concept is a word or group of words that is associated by a relation. A concept is commonly but not always a noun or noun phrase.

The page can also highlight dominant CRCs and paths. A CRC is a concept-relation-concept sequence, and a path is a longer sequence.

Drilling Down

### 4.11 Drilling Down

In some widgets, you may be able to drill down to lower levels. In the InterSystems IRIS Business Intelligence model, levels are contained within hierarchies, which are contained within dimensions. In some cases, there are multiple levels within a hierarchy. In these cases, a member of the higher level contains one or more members of the lower level, and you can drill down — navigate from the higher-level member to the lower-level members. You can do this via double-click or (if available) via the Drilldown button.

It is not possible to drill down from a total row. Also note that the drilldown action has no effect if the pivot table uses a manually entered MDX query (which is a rare scenario).

#### 4.11.1 Drilling Down with Double-Click

If a pivot table row represents a higher-level member, you can double-click the member name to view the lower level
members. For example, consider the following pivot table widget:

If you double-click the cell 1930s, the widget then displays the following:

If you select the << characters in any row, the system restores the previous state of the widget.

This kind of drilldown action is not available in charts.

#### 4.11.2 Using the Drilldown Button

A widget might include the Drilldown button
In this case, to drill down:

, which provides you with an alternative way to drill down in a hierarchy.

1. Select a row in the pivot table. Or select a chart item if the widget is in chart format.

For example:

2.

Select the Drilldown button

.

The widget then displays data for the lower-level members associated with the selected item. For example:

Using the Dimension List

### 4.12 Using the Dimension List

A widget might include the Dimension List button

, which provides you with additional drill options.

If you select this button, the widget then displays a list of dimensions, to the left of the pivot table. For example:

This list may or may not be the same as the dimensions defined in the cube, depending on ho w it was created.

To use this list:

1. Expand the folders as needed.

2. Drag and drop from the list onto the gray part of any row.

For example:

For another example:

To reverse the effect, select the Reset button

above the dimension list or select the << button in the pivot table.

### 4.13 Drilling to a Different Dashboard

In some pivot table widgets, you might be able to double-click a cell in order to display a different dashboard. The newly opened dashboard is filtered to the conte xt in which you double-clicked. For example, suppose that the first dashboard
includes the following widget:

Refreshing a Widget

Depending on how this pivot table widget is configured, if you double-click a data cell, the system might display a dif ferent
dashboard, as follows:

- If you double-click in the Female row, the newly opened dashboard is filtered to female patients.

- If you double-click in the Male row, the newly opened dashboard is filtered to male patients.

- If you double-click in the All Patients row, the newly opened dashboard is not filtered by gender .

### 4.14 Refreshing a Widget

To refresh the display in a widget, select the Refresh button

.

In some cases, this button might appear as a button with text. The text on the button might be Refresh, Redisplay, or any other suitable string.

In some cases, the widget might automatically refresh at a specified interv al. In this case, there might not be a refresh button.

### 4.15 Reloading a Dashboard

To reload the dashboard itself, select the Reload Dashboard button

.

In some cases, this button might appear as a button with text. The text on the button might be Reload or some other suitable string.

### 4.16 Exporting Data to Microsoft Excel

You can export data to Microsoft Excel from a pivot table widget, but not from other types of widgets. To do so, select the

Export to Excel button

in the widget.

The system generates an Excel file that contains all the data currently displayed in the widget. The file has the name %DeepSee.UI.MDXExcel.zen.xls, %DeepSee.UI.MDXExcel.zen-1.xls, or similar. Your browser then does one of the following,
depending on your operating system, the configured file types on your machine, your bro wser, and your browser settings:

- Opens the file with Excel (or other selected program).

You specify the program to use by setting a browser option. For example, on Firefox, you use Tools > Options > Applications. This option also enables you to specify whether the browser should open the file with this program or prompt you to save it to the hard drive.

- Prompts you to open the file with Excel (or other selected program, as described in the pre vious bullet).

- Opens this file within the current bro wser window.

This is the default behavior for Windows operating systems earlier than Windows Vista. You can change this behavior on the Edit File Type dialog box (which you access via My Computer > Tools > Folder Options or My Computer > View > Options, depending on the operating system version).

This option is not available on Windows Vista and later Windows operating systems.

- Prompts you to save the file to the hard dri ve.

- Automatically saves the file to the hard dri ve.

When you export to Excel, note that it is not possible to export more than 250000 rows. Also, if the subject area uses an external table, there is a limit of 1000 rows in the listing.

Note:

If no numeric formatting is specified, an y numbers are formatted as integers by default. (The actual values are available in Excel, and you can change the formatting as needed to display them appropriately). If numeric formatting is specified in the model or in the pi vot table definition, that formatting is used in Excel.

### 4.17 Printing Data

The dashboard might include one or more Print buttons . Depending on how it is configured, a Print b utton might print only a single widget or multiple widgets. In any case, when you use this button, the system generates a .pdf file and opens it in your default browser. (If the output represents multiple widgets, the file contains one page for each widget.) You can then use options in the browser to print the file or to do wnload it, for printing later.

Note that if you download the file, the bro wser saves the file to the def ault download directory for that browser; there is
no mechanism for the system to specify a different location.

If the pivot table is extremely wide, it is not possible to generate a .pdf file for it.

#### 4.17.1 Requirements for Printing

When a user invokes the Print option, InterSystems IRIS® data platform uses Java to call out to a third-party PDF rendering tool. This means that Java (or specifically JRE, Ja va Runtime Environment) is required on the user’s local machine. For information on the requirements, see Configuring InterSystems IRIS for PDF Output

.

### 4.18 Using a Map Widget

A map widget includes a different set of options that are not present in other widgets:

Other Tasks

In a map widget, you can do the following:

- Toggle the display between the map view and the satellite view. To do so, select the Map/Satellite button.

- Display a different area. To do so, drag the cursor while holding down the left-select button.

- Zoom in or out. To do so, drag the slider on the zoom bar.

- Display additional details about a data point. To do so, select the data point. The widget then displays a popup window,
if there is any additional data. For example:

To close this window, select the X in the upper right.

### 4.19 Other Tasks

In a dashboard, you may also be able to do the following:

- Reconfigure an y widget. To do so, select the < button (if available) on the left of the dashboard to open the Dashboard Editor. Then make changes as described in Creating Dashboards.

- Select items that redefine the widget in dif ferent ways. There are many options. For example, the widget could include
a drop-down list where you can choose a different pivot table to display:

For another example, it could include a drop-down list that controls what is shown for rows or columns:

- Display the Mini Analyzer and make local changes to the pivot table shown in a widget. Select the Mini Analyzer button , if included, and make changes as described in Using the Analyzer.

The changes do not affect other widgets, other dashboards, or other users.

Then to save your changes and exit the Mini Analyzer, select OK in the Mini Analyzer. Or, to discard your changes and restore the original pivot table, select Reset.

- Perform custom actions. The Filters box and the widgets might include additional buttons to perform custom actions.

In some cases, you might first need to select a ro w or rows in a widget. To do so:

–

–

In a standard pivot table widget, to select a row, select the row. To select multiple rows, hold down the SHIFT key while selecting those rows.

In a pivot table widget that displays a listing, select the check boxes at the left of the rows.

A custom action can do any of the following:

– Open a different dashboard in the same window.

– Open a URL in the same window or in a new window.

–

–

Execute server-side code.

Execute client-side commands such as refreshing the dashboard.

### 4.20 Saving Your Changes

To save the current state of the dashboard that you are viewing, select Menu > Save My Settings. This option performs a local save of the current dashboard. It saves the size and placement of each widget and the current state of all filters and other controls in the dashboard. These changes are saved only for you, and are not visible to other users.

If you select Menu > Clear My Settings, the system removes your settings for this dashboard. After using this option, use the browser’s refresh button to display the dashboard in its base state.

There are also options for saving the base dashboard design itself so that all users see the changes (see Creating Dashboards). You can use these only if you have the appropriate permissions.

For reference, the following table describes how the different dashboard changes can be saved.

Saving Your Changes

Can Be Saved As My
Setting?

Can Be Saved As
Dashboard Design?

Dashboard Change

Maximizing or minimizing a widget

Moving or resizing a widget

Changes made via the Dashboard Designer

Using the Mini Analyzer to make local changes to the pivot table used in a widget

Specifying values for filters or for other widget controls

Yes

Yes

No

Yes

Yes

Other changes (sorting, drilling down, and others)

No

Yes

Yes

Yes

No

No

No

When you save the dashboard design, your settings for that dashboard are cleared, except for any changes made via the
Mini Analyzer.

This page describes how to use the Pivot Analysis window, which you can access via the Analysis button table widgets.

on pivot

### 5.1 Using the Pivot Analysis Window

The system provides an analysis window that you can use for several specialized kinds of analysis. In each case, you first
select one or more cells, and the analysis considers the lowest-level data associated with those cells. To access this window:

1. Select the data cells in the row or rows.

To select multiple cells, hold the Shift key down while selecting the cells.

To select an entire row, select the row label on the left. To select an entire column, select the column header.

The analysis option is not available for cells in a total row or a total column.

2.

Select the Analysis button

.

Depending on how the widget is configured, the system either pro vides a choice of analysis options or displays one of them without any choice.

3.

(If applicable) For Analysis Option, select one of the following:

- Cluster — Performs a cluster analysis.

- Distribution — Performs a distribution analysis.

- Regression — Performs a regression analysis.

Or select iKnow Plug-ins and then select one of the following:

- Content Analysis — Performs a content analysis.

- Entity Analysis — Performs a entity analysis.

The iKnow Plug-ins options are applicable only if your cube includes NLP measures.

The following sections provide the details.

Note:

This window is also available in the Analyzer.

### 5.2 Cluster Analysis

For background on the Pivot Analysis window, see Using the Pivot Analysis Window.

Cluster analysis or clustering is the assignment of a set of observations into subsets (called clusters) so that observations in the same cluster are similar in some sense. Clustering is a method of unsupervised learning, and is a common technique for statistical data analysis used in many fields, including machine learning, data mining, pattern recognition, image analysis, information retrieval, and bioinformatics.

For a cluster analysis, the top area of the page looks something like the following:

To use this page:

1. Specify details of the analysis in the top area of the page.

Details are beyond the scope of this book; it is assumed that the reader is familiar with cluster analysis.

2. Select Run.

The bottom area of the page displays the results. For example:

Distribution Analysis

For general information on cluster analysis, see the Wikipedia page (https://en.wikipedia.org/wiki/Cluster_analysis). There are also many books available on this topic.

### 5.3 Distribution Analysis

For background on the Pivot Analysis window, see Using the Pivot Analysis Window.

A distribution analysis shows the number of occurrences of different values of specific measurement, across a set of records.

For a distribution analysis, the system displays something like the following:

To use this page, select a measure (such as Age in this example).

The horizontal axis then shows all the values of this measure for the selected cells. For each measure value, the vertical axis shows the number of source records (for the selected cells) that have that value.

The top of the page shows the following values:

- Items — Number of source records for the selected cells of the pivot table.

- Missing — Number of source records (for the selected cells) that do not have a value for this measure.

- Min value — Lowest value for this measure among these source records.

- Max value — Highest value for this measure among these source records.

- Avg — Average of these values.

### 5.4 Regression Analysis

For background on the Pivot Analysis window, see Using the Pivot Analysis Window.

A regression analysis attempts to determine the relationship between independent variables and a dependent variable. (The InterSystems IRIS Business Intelligence regression analysis considers only one independent variable.)

For a regression analysis, the system displays something like the following:

Regression Analysis

To use this page, specify the following details:

- Input (X) Measure — Select the measure that you want to treat as independent (such as Age in this example). These values are shown on the horizontal axis.

- Response (Y) Measure — Select the measure that you believe is dependent on the first measure (such as Encounter Count in this example). These values are shown on the vertical axis.

- When you do so, the page displays a data point for each lowest-level record associated with the selected cells.

- Fit — Select the type of fitting to perform:

–

–

–

–

line — Performs a linear regression.

exp — Performs an exponential regression.

log — Performs a logarithmic regression.

power — Performs a power regression.

Confidence Level — Optionally select the confidence le vel to use when calculating error bars for the values being determined.

In each case, the system determines the details of the equation that predicts Y as a function of X, and it plots the predicted
X-Y curve on the page. The area above the chart displays details of the fit. F or example, for a linear regression:

For another example, the page displays the following details for an exponential regression:

For general information on regression analysis, see the Wikipedia page (https://en.wikipedia.org/wiki/Regression_analysis). There are also many books available on this topic.

### 5.5 Text Analytics Content Analysis

For background on the Pivot Analysis window, see Using the Pivot Analysis Window.

The iKnow content analysis option displays information about the most typical and least typical unstructured text values. This analysis option is applicable only if your cube includes NLP measures.

For the content analysis, the system displays something like the following:

The Most typical facts section lists the records that have the most typical content, as determined by the Analytics Engine. The Most breaking facts section lists the records that have the breaking content. Breaking content is content in which the dominant entities in that source are least similar to the dominant elements of the group of sources. For more information, see Dominance and Proximity.

Each table lists the records and displays the fields listed in the selected detail listing.

On this page, you can do the following:

- See the entire unstructured text for a given record. To do so, select the magnifying glass icon shown by that record.

- Select a different NLP measure to analyze. To do so, select a choice for Measure.

An NLP measure is different from other kinds of measures and cannot be used in the same way as other measures. It is based on a source value that contains unstructured text such as a free-form text report. When you select an NLP measure to analyze here, you are examining results of the Analytics Engine for those source values.

- Select a different detail listing to use. To do so, select a choice for Display Listing.

The system initially displays the listing named ShortListing (if that is defined) or the def ault listing for the subject area.

This example uses the Aviation Events sample.

### 5.6 Text Analytics Entity Analysis

For background on the Pivot Analysis window, see Using the Pivot Analysis Window.

The iKnow entity analysis option displays information about the entities in your unstructured text values. This analysis option is applicable only if your cube includes NLP measures.

For the entity analysis, the system displays something like the following:

This page provides three tabs, which display information about the records associated with the pivot table cells that you

selected before you selected the Analysis button

. These tabs work together as follows:

- The Overview tab displays information for the 20 most common entities among those records. You use the Select by
option to control how the system selects these entities; see the first subsection .

- Select a rectangle in this chart to see further detail; see the next bullet item.

- For a selected rectangle in the Overview tab, the Cell breakdown tab shows how that entity is distributed among the original pivot table cells. See the second subsection.

Select a bar in this chart to see further detail; see the next bullet item.

For a selected bar in the Cell breakdown tab, the Entities tab displays related entities. See the third subsection.

This example uses the Aviation Events cube demo in the BI samples.

#### 5.6.1 Overview Tab

The Overview tab displays information about the top entities among the records associated with the pivot table cells that

you selected before you selected the Analysis button top 20 entities, according to your choice of metric.

. The chart on this tab displays one rectangle for each of the

##### 5.6.1.1 Selecting the Top Entities

To determine how the system selects the top entities, select a metric from the Select by drop-down list. The options are as
follows:

- spread, the default, lists the top entities by their spread (total number of facts in which the entity appears).

- BM25 lists the top entities using a frequency calculation algorithm in descending order by calculated BM25 score. It calculates this score using an algorithm based on the Okapi BM25 standard, which combines an entity's Term Frequency with its Inverse Document Frequency (IDF), taking into account document length.

- TFIDF lists the top entities using a frequency calculation algorithm in descending order by calculated TFIDF score. It calculates this score by combining an entity’s Term Frequency (TF) with its Inverse Document Frequency (IDF). The Term Frequency counts how often the entity appears in a single source. The Inverse Document Frequency counts the number of times the entity appears in the collection of sources, and uses this overall frequency to diminish the Term
Frequency. Thus an entity that appears multiple times in a small percentage of the sources is given a high TFIDF score;
an entity that appears multiple times in a large percentage of the sources is given a low TFIDF score.

Note:

The BM25 and TFIDF options are computation-intensive and can take some time to complete.

##### 5.6.1.2 Color Coding

The colors in this chart indicate how well each entity serves as an indicator for a given pivot table cell, based on the Naive
Bayes probability for that entity, as follows:

- If only one cell was originally selected in the pivot table, the colors indicate how well each entity serves as an indicator for that pivot table cell, compared to all other records.

- If multiple cells were originally selected in the pivot table, the chart displays the Color-code by drop-down list, which lists the pivot table cells by name and includes the all option.

In this case, the colors indicate how well each entity serves as an indicator for the pivot table cell that is currently shown in the Color-code by drop-down list, compared to the records for all the other originally selected cells.

To use a different pivot table cell as the basis of comparison, select an option from the Color-code by drop-down list.
For example:

The total option considers all the originally selected cells as a group.

Green generally denotes good indicators, and red denotes bad indicators. Solid green means that the term is a very good indicator, pale green means that the term is a good indicator, pale red means that it is a bad indicator, and solid red means that it is a very bad indicator. Note that in some cases, an entity is a bad indicator because it is common to all sources and thus does not enable you to discriminate categories of sources.

For example, suppose that we use a pivot table that displays aircraft type as rows. As the starting point for analysis, we
select the pivot table cells Airplane and Helicopter. If we use Airplane to color-code, this chart looks as follows:

Notice that the entities airplane and runway are good indicators for the pivot table cell Airplane. The other entities (especially ground) are bad indicators.

In contrast, if we use Helicopter to color-code, the chart would be colored as follows:

This shows that the entities airplane and runway are bad indicators for the pivot table cell Helicopter. The other entities (especially ground) are good indicators.

##### 5.6.1.3 Other Options

On the Overview tab, you can also do the following:

- Select a different NLP measure to analyze. To do so, select a choice for Measure.

An NLP measure is different from other kinds of measures and cannot be used in the same way as other measures. It is based on a source value that contains unstructured text such as a free-form text report. When you select an NLP measure to analyze here, you are examining results of the Analytics Engine for those source values.

Specify an additional string to analyze. To do so, type a string into Analyze string and then press analyze. The system then includes additional information for that string.

Select a rectangle in this chart to display a breakdown for the corresponding entity. See the next section.

- 5.6.2 Cell Breakdown Tab

- The Cell breakdown tab is useful only if you started by selecting multiple cells of a pivot table.

This tab shows how an entity is distributed among the pivot table cells from which you started. When you select a rectangle in the Overview tab, the system displays the Cell breakdown tab with information for that entity.

The Cell breakdown tab looks like this:

For the given entity, this tab shows how that entity is distributed among the pivot table cells that you selected before you
selected the Analysis button. For each cell, the chart shows fiv e color-coded bars, which display the following series:

- entities — indicates the count of distinct, similar entities in records associated with the given pivot table cell or cells. This count includes all entities that are similar to the given entity.

- entity freq — indicates the entity frequency; that is, the number of times the given entity occurred in records associated
with the given pivot table cell or cells.

- If you select Include similar entities, this calculation also includes similar entities.

- entity spread — indicates the entity spread; that is, the total number of records in which the given entity appears, for
the given pivot table cell or cells.

- If you select Include similar entities, this calculation also includes similar entities.

cell probability — indicates how well the given entity serves as an indicator for the selected pivot table cell or cells, based on the Naive Bayes probability for that entity.

dominance — indicates how dominant the given entity is, within these records. For information, see Semantic Dominance.

Important:

These series are scaled separately so the chart can show them all. The scale shown on the chart applies only to the entities series. To see the actual numeric value for any bar, hover the cursor over the bar. For
example:

On this tab, you can do the following:

- Select a different NLP measure to analyze. To do so, select a choice for Measure.

- Include similar entities in the calculations for entity freq and entity spread. To do so, select Include similar entities.

- Display entity spread % (the entity spread as a percentage of the total number of records) instead of entity spread. To do so, select Spread as %.

- Specify an different string to analyze. To do so, type a string into Analyze string and then press analyze.

- Select a bar in this chart to display related entities. See the next section.

#### 5.6.3 Entities Tab

The Entities tab displays related entities in the given pivot table cell or cells. When you select a bar in the Cell breakdown tab, the system displays the Entities tab with the associated details.

The Entities tab looks like this:

On this tab, you can do the following:

- Select a different NLP measure to analyze. To do so, select a choice for Measure.

- Specify a different string to analyze. To do so, type a string into Analyze string and then press analyze. The system then shows information for that string.

- Page through the results. To do so, use the << and >> buttons.
