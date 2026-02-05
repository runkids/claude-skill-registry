# InterSystems IRIS Release Notes

New in InterSystems IRIS 2025.3

This page describes the new features, enhancements, and other significant updates in the 2025.3 release of InterSystems IRIS® data platform, which is a continuous delivery (CD) release.

For other information you may wish to consider related to changes included in this release, see Known Issues and Notes. For a more exhaustive list of the changes included in this release, refer to the Upgrade Impact Checklist.

### 1.1 Release Information for 2025.3

The current release is 2025.3. The posting for 2025.3 is build 2025.3.0.226.0.

### 1.2 Enhancing Analytics and AI

Improved performance for vector search

The internal layout of the Approximate Nearest Neighbour (ANN) index used by vector search has been modified to improve duplicate entry management and reduce query-time overhead. Benchmarks show throughput and latency improvements of up to 10% depending on workload characteristics.

The updated format is applied automatically when the index is rebuilt. Rebuilding is not required for continued operation: the runtime is fully backwards compatible and can read and write indices in both the legacy and updated formats.

New version of Adaptive Analytics

Adaptive Analytics has published AtScale 2025.4.1. This release contains bug fix es and performance enhancements, and introduces support for inbound query CROSSJOIN operations that return inbound cells.

New in InterSystems IRIS 2025.3

### 1.3 Enhancing Developer Experience

Scale interoperability production hosts while maintaining FIFO

In past releases, it was necessary to configure pool sizes of one in order to force sequential message processing in order to maintain first-in-first-out (FIFO) queuing beha vior for messages in a message feed. This release introduces customer-calculated message group identifiers, which allo ws for pool sizes of greater than one while maintaining FIFO. These identifiers also enable parallel processing of messages that had no direct dependenc y, increasing throughput of a production.

There are two settings provided for Business Processes and Business Operations under the header “FIFO Message Grouping” - Group Calculation (FMGCalculation) and Group Completion Hosts (FMGCompletionHosts) - that ven group allow developers to configure the group identifier and the host that releases the group handle for a gi identifier , respectively. Group identifiers are configured by a Data Transformation (DTL) and is typically set to a value that identifies a FIFO dependenc y, such as a patient or device id.

### 1.4 Enhancing Database Operations

Journal archiving support for Azure Blob Storage

Journal Archiving allows InterSystems IRIS to push closed journal files—after compression—directly to a cloudbased archive location, reducing the use of high-IOPS local storage. In addition to Amazon S3, Azure Blob Storage is now supported as an archive target.

### 1.5 Enhancing Data Management and SQL

Enhancements to foreign tables

This release extends Foreign Table pushdown from the individual table level to the server level, enabling pushdown of entire JOIN operations across two or more tables originating from the same foreign server. Previously, such joins required pulling all qualifying rows from each table into InterSystems IRIS for local execution, which could be costly when querying large tables without direct filtering. This change represents the final major milestone in maximizing query computation pushed down to eligible foreign sources.

Guardrails against running out of process memory

When executing complex queries, InterSystems IRIS SQL may create temporary data structures (tempfiles) for operations such as sorting or aggregation. If table statistics indicate these structures will be small, the optimizer may use in-memory arrays, which are significantly f aster than process-private globals (PPGs). However, if the statistics are inaccurate, the optimizer may underestimate the size of a tempfile, potentially e xhausting process memory at runtime and resulting in a <STORE> error.

To address this, InterSystems IRIS SQL now monitors memory usage during query execution. If the system detects that memory is running low, it will automatically fall back to using PPGs in cases where inaccurate statistics led to an underestimation. While representative table statistics remain strongly recommended, this safeguard reduces the risk of runtime failures due to misestimates.

Other SQL enhancements

This release improves the storage of lightweight runtime statistics for each SQL statement in the Statement Index, enhancing the performance of common queries against INFORMATION_SCHEMA.STATEMENTS and related tables.

Additional enhancements have been made to SQL Query Plan output, including new information messages.

Performance has been improved for queries that aggregate data across low-cardinality field on columnar tables.

### 1.6 Enhancing Database Operations

Additional metrics for process information, ECP status, and the Write Daemon

The 2025.3 release includes substantial metrics additions to the metrics available through OpenTelemetry and the
metrics API. These additions include:

- An entry for each iris_process, listing its pid, state, internal wait state, job type, and client name.

- Counters by process for global references, ObjectScript commands, block allocations, physical reads, blocks queued for writing, and journal entries.

- A gauge for PPG block usage in megabytes by process.

- The iris_ecp_servers metric, which reports a series for each ECP connection, listing the server it is connected to and the connection state.

- The iris_ecp_clients metric, which is similar to iris_ecp_servers, but lists the information for clients.

- iris_wd_* metrics, which provide insights into the state of the Write Daemon.

Daily System Performance collection service

When enabled, your instance will collect daily system performance reports. This feature is configured through the SystemPerformanceDailyReportsOn CPF parameter.

Add metrics to %SYS.ProcessQuery

This release now exposes the parent process ID and start time in %SYS.ProcessQuery. Both metrics are exposed in the Management Portal (on the Processes and Process Details pages) and in ^JOBEXAM (under Examine details).

### 1.7 Enhancing Speed, Scale, and Security

Security Wallet

The new security wallet lets you securely store and access “secrets” in InterSystems IRIS without exposing those secrets to application code. In this context, a “secret” refers to any piece of sensitive information required by an application at runtime, including API keys, encryption keys, usernames, and passwords. Secrets are grouped together in collections for convenient access management and access to these secrets is audited.

Secrets are stored in the IRISSECURITY database, which must be encrypted to protect sensitive data.

New in InterSystems IRIS 2025.3

### 1.8 Modernizing Interoperability User Interface

The following enhancements are included in interoperability-enabled products in the new user interface (which remains an opt-in experience).

New Production Configuration user experience enhancements

- When editing host categories, viewing connections are permissible

- A view icon on all rule sets open the specific rule set in the Rule Editor split panel

- Updated icons to open and close a panel

- When selecting the test button, the button is highlighted to indicate that the test panel is open

- Added a legend for Host Statuses in the information icon on a host

- Added drop down icons for all drop-down enabled settings fields

- Host Properties are now searchable, with added “expand all” sections

- IP Address and Port Number are now searchable in the Production Configuration Filter Bar

- Host Connections appear as they are registered by the front end, rather than appearing all at once when connections are fetched New DTL Editor user experience enhancements

- DTL Segment Path copies with both field te xt and ordinal numbers

- The “hover over” segment icons for copying or adding a mapping are more accessible

- When adding a mapping, hovering over the particular segment now only shows the copy icon

- The DTL Editor split screen header and toolbar both remain in place when scrolling New in InterSystems IRIS 2025.2 This page describes the new features, enhancements, and other significant updates in the 2025.2 release of InterSystems IRIS® data platform, which is a continuous delivery (CD) release.

For other information you may wish to consider related to changes included in this release, see Known Issues and Notes. For a more exhaustive list of the changes included in this release, refer to the Upgrade Impact Checklist.

### 2.1 Release Information for 2025.2

The current release is 2025.2. The posting for 2025.2 is build 2025.2.0.227.0.

### 2.2 Enhancing Speed, Scale, and Security

New security database

Upgrading to InterSystems IRIS 2025.2 will move security data from the IRISSYS database into the IRISSECURITY database. New installations also store their security data in IRISSECURITY.

Among other things, this change removes direct access to security globals, updates privileges for security APIs (these now require %DB_IRISSYS:R and %Admin_Secure:U), and restricts SQL queries on security data. Customers should thoroughly test their applications prior to upgrade.

You can use the new %SecurityAdministrator role for general security administration tasks.

InterSystems recommends encrypting IRISSECURITY.

For a detailed overview of these changes, see https://community.intersystems.com/post/advisory-irissecurityintersystems-iris-20252 or IRISSECURITY Upgrade Impact.

Important:

This is a major incompatible change to a core component of InterSystems IRIS. If you are upgrading to version 2025.2, it is imperative that you thoroughly test your software after upgrading. If you encounter any problems, please contact InterSystems Support.

OAuth2 authentication

This release introduces several features to improve the user experience of configuring O Auth2.

- OAuth2 is now a native authentication type that can easily be enabled for web applications.

New in InterSystems IRIS 2025.2

- You can now create resource servers with the new OAuth2.ResourceServer class, which simplifies resource server configuration significantly . Previously, resource servers were configured as an instance of O Auth2.Client.

- The OAuth2.ResourceServer class provides a sample authenticator for determining user permissions which, for simple configurations, requires no custom code (this pre viously required a custom ZAUTHENTICATE implementation). This simple authenticator can be extended and customized to suit your environment.

- You can now use JDBC and ODBC to authenticate to InterSystems IRIS with access tokens.

Support for ECC

InterSystems IRIS now supports ECC (ECDSA) certificates for TLS configurations. ECC certificates are smaller and more computationally efficient than RSA and DSA certificates.

### 2.3 Enhancing Analytics and AI

Improvements to the Cube Manager

The Cube Manager was designed to assist customers with managing cube updates, synchronization, and build. In this release, InterSystems has made several improvements in functionality and in the user interface to more easily
manage cube updates. The improvements include:

- Reworking the cube build/sync functions so that they perform dependency analysis and automatically rebuild dependent cubes when called, providing guardrails and preventing situations where dependent cubes are not built.

- Updating the Cube Manager user interface to focus on a schedule group. The user identifies the frequenc y with which the cube is to be updated and the schedule is kicked off to sync (if possible) or build (is sync is not possible). Power users can continue to manage builds and syncs from the APIs, command line, or the Architect user interface.

- Logging cube update events in %DeepSee_CubeManager.CubeEvent.

- Including additional information to help customers identify what is happening with the cube updates in this user interface, such as previous update time, status, and next schedule time as shown below.

### 2.4 Enhancing SQL and Data Management

Smarter table statistics

This release introduces a significant change in ho w InterSystems IRIS manages table statistics, a key ingredient for getting high SQL query performance. InterSystems IRIS now distinguishes between fixed statistics , which are stored in the class definition and can be tuned by a de veloper (as in the pre-existing model), and collected statistics, which are stored with the data and are always based on actual data.

A new system maintenance task is available to automatically collect statistics for tables that do not have any or have stale statistics. This task is currently off by default to stay as close as possible to the pre-existing behavior, but InterSystems recommends switching it on and reviewing whether the additional IO load is reasonable. Fixed statistics always take precedence over collected statistics, so it is worth reviewing your current application to evaluate whether there are any fix ed statistics in the class definition that you may w ant to drop in favor of the collected ones.

Table partitioning

Table partitioning helps users manage large tables efficiently by enabling them to split data across multiple databases based on a logical scheme. With this architecture, you can, for example, move older data to a database mounted on a cheaper tier of storage, while keeping the current data that is accessed frequently on premium storage. The data structure for partitioned tables also brings several operational and performance benefits when tables get very large (greater than one billion rows).

As this is a broad new product capability, it will be made available in phases. This release includes the core partitioning and bucketing capabilities, as well as an API to may partitions to specific databases. F orthcoming releases will introduce additional functionality, such as converting existing tables from or to a partitioned structure, and adopt it for some built-in datasets. See the documentation for more details.

Note:

Table partitioning is currently an Experimental Feature. An Early Access Program is currently available for customers who are evaluating the feature and wish to share their feedback and use cases, as well receive software updates and examples. Register here if you wish to participate.

Expanded pushdown capabilities for foreign tables

This release significantly enhances the foreign table infrastructure, which no w also considers functions, aggregates, grouping, and ordering clauses in queries selecting from foreign tables, such that their evaluation can be pushed down to the remote servers. The new capabilities significantly e xpand upon the number of predicates that were previously eligible for pushdown and therefore can speed up many queries by minimizing the amount of data that needs to be passed back over the connection, a major factor in foreign table query performance.

To address the variance in different vendors’ support for SQL functions, a set of simple tiers is used to captured which set of functions it is safe to assume a foreign server supports. See the foreign tables documentation for more details.

Foreign tables now also use a simplified class structure, meaning it is safe to e xport and import them simply as a class definition.

Full support for mixing columnar and non-columnar indexes in query plans

Columnar storage for relational tables offers order-of-magnitude faster response times for analytical SQL queries. With this release, InterSystems introduces enhancements to the SQL optimizer’s costing algorithm to accurately estimate the cost of not just the query plans that entirely use columnar indexes, but also the mixed plans that combine columnar and non-columnar index structures. These changes increase the applicability and benefits of columnar stored in mixed transactional-analytical environments.

### 2.5 Enhancing Database Operations

Full support for truncations across database volumes

When using multivolume databases, you can now truncate up to any size small enough to hold the remaining data. Previously, you could only truncate the last volume for a database, but now truncation will delete empty volumes as needed.

Integrity check CHUI

This release introduces a new CHUI (character user interface) for the integrity check utility (^Integrity), significantly enhancing the usability of this important maintenance task. The new interface uses multiple background processes and offers better progress information, including tallies of globals checked and errors found while the process is running, and a number of minor quality-of-life enhancements.

New in InterSystems IRIS 2025.2

With this release, InterSystems also deprecates a number of legacy subroutines in favor of this new entry point.

### 2.6 Modernizing Interoperability User Interface

The following enhancements are included in interoperability-enabled products in the new user interface (which remains an opt-in experience).

New Production Configuration user experience enhancements

- Pool size quantities are now displayed on each production configuration host.

- You can now create a new category by directly entering the naming convention in the category field of the host.

- There is now support for browser-level control find in Production Configuration.

- Production Host items now feature the Test Host function.

- In the new Settings Panel the X cancel icon also appears on panels to cancel an action.

- Longer class tooltip descriptions are formatted per the class documentation.

- Display of configuration item descriptions is enhanced to honor markup for longer , structured descriptions.

- Action Items are grayed out when not in the context of a host item or production.

- Creating a host enabled the automatic creation of a router and role.

- You now have the option to Update and Recover a production, where supported.

- Productions may not be created through the UI.

New DTL Editor user experience enhancements

- The Data Transformation Function drop-down menu is now searchable and limited to functions defined in the subclass.

- The DTL Graphical Editor now includes a button to copy an HL7 field path when ho vering over a segment.

- Setting the Ordinal Number or Path Expressions or both will input the same expression setting when setting the DTL statement target and source fields.

New Rule Editor user experience enhancements

- It is no longer possible to rename rules. Previously, that behavior cause confusion about changes to active rules. To create a new rule, use Save As instead.

- There is now support for browser-level control find in Rule Editor .

### 2.7 Platform Updates

Remove Support for Red Hat 8

This release discontinues support for running InterSystems IRIS on Red Hat Enterprise Linux 8 for x86–64 or
ARM64.

New in InterSystems IRIS 2025.1

This page describes the new features, enhancements, and other significant updates in the 2025.1 release of InterSystems IRIS® data platform, which is an extended maintenance (EM) release.

For other information you may wish to consider related to changes included in this release, see Known Issues and Notes. For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 3.1 Release Information for 2025.1

The current release is 2025.1. The posting for 2025.1 is build 2025.1.3.477.0.

### 3.2 Enhancing Developer Experience

Python Support in DTL Editor

This release of InterSystems IRIS introduces the capability to leverage Python statements in your Data Transformation Language (DTL) classes. For each action, users can select the language (ObjectScript or Python) enabling developers who are skilled in Python to utilize larger parts of the platform with their existing skill set.

### 3.3 Enhancing Analytics and AI

Approximate Nearest Neighbor Index for Vector Search

InterSystems IRIS Vector Search now features a disk-based Approximate Nearest Neighbor (ANN) index for VECTOR—typed columns. The ANN index is based on the popular Hierarchical Navigable Small Worlds (HNSW) algorithm. It yields sub-second similarity query response times over millions of vectors, providing a 2,500 times speedup in performance compared to the "brute force" non-indexed vector search, when searching over 100 million vectors.

When creating the ANN index, the user must choose which similarity function will be used (either VEC- TOR_DOT_PRODUCT or VECTOR_COSINE) to query the data. The ANN also supports incremental updates, and can be used in combination with the %EMBEDDING index.

New in InterSystems IRIS 2025.1

Updates to Business Intelligence Cube Building and Synchronization

This release includes changes to the InterSystems IRIS Business Intelligence cube building process to provide safeguards for updating related cube dependency chains and other enhancements that address several customerreported issues in this area. To ensure that analysis of cube builds is always taken into consideration and that data remains consistent, the base functions for cube building and synchronization (%BuildCube and %SynchronizeCube) now perform cube dependency analysis automatically and execute a full model group update. This new procedure
includes:

- Analyzing the requested cube to see if there are any relationship dependencies and then internally establishing a full list of cubes that need to be updated, along with appropriate build orders for that cube list.

- Executing build and synchronization of individual cubes in succession for the list, as needed, using the new %BuildOneCube and %SynchronizeOneCube functions.

- Collating the singular statistics into a complete set to return to the caller.

These changes also include logging of all events recorded for all cubes built in the dependency chain, independent of the Cube Manager, making troubleshooting more accessible.

If you are upgrading to this release from a previous one, these changes may affect the behavior of your custom cube update tasks or methods. Refer to Special Considerations When Upgrading for more information.

### 3.4 Enhancing SQL and Data Management

New syntax for server-side pagination

InterSystems IRIS SQL has long supported the TOP keyword to limit query results only to the first n records of a sorted result set. With this release, InterSystems adds support for two alternative syntax fla vors: LIMIT ... OFFSET ..., which is commonly used in other database platforms, and OFFSET ... FETCH ..., which is the official ANSI standard. By offering all three methods of server-side pagination, InterSystems has made it easier for new customers and users migrating to InterSystems IRIS to write efficient queries.

Better bulk Import of DDL statements

Based on customer feedback on the LOAD DATA command, InterSystems IRIS SQL now supports a similar LOAD SQL command to load and execute any number of SQL DDL statements from a file or directory . This new command offers a simple entry point for developers accessing the system over SQL and writes detailed output, either to the SQL Diagnostics table or another log file.

The pre-existing ObjectScript entry points have also been enhanced to support the diagnostic output.

In-place conversion between row and columnar table layout

This release extends the ALTER TABLE ... CONVERT command to support conversion between row and columnar table layouts. Users can choose to convert the whole table or a subset of columns. Queries and DML (INSERT, UPDATE, and DELETE) commands can still be executed while the table conversion is taking place. Please see ALTER TABLE for more details on the conversion process.

Additional SQL functions

This release introduces two new convenience functions to the InterSystems SQL dialect:

- APPROX_COUNT_DISTINCT() is a new aggregate function that implements the HyperLogLog algorithm, which offers users an estimate of the number of distinct values for a particular column that is orders of magnitude faster than the exact result obtained from a COUNT(DISTINCT) command.

- HASHBYTES() offers a convenient SQL entry point for common hash functions, such as SHA256.

### 3.5 Enhancing Speed, Scale, and Security

Smaller journal records

The 2025.1 release improves the scalability of $INCREMENT and introduces a new, more compact journal file
format. The new format uses less I/O bandwidth (due to the smaller journal record size) on average and includes
changes to the way that $INCREMENT is recorded in the journal.

Important:

Journal files created on a 2025.1 instance cannot be opened on an instance running a prior release, so be sure to keep track of which mirror members are upgraded. Applications that have implemented custom logic to read and interpret journal files should be re viewed to determine whether
this logic is impacted by the new $INCREMENT handling discussed in Special Considerations
When Upgrading; most such custom logic is not impacted.

Faster database compaction

This release includes a number of enhancements to increate the efficienc y of database compaction and defragmentation. Especially for large databases with lots of big strings, the compaction process now runs significantly f aster and is better aligned with any concurrent block allocation for application workloads.

Download mirror database

Previously, adding a database to a mirror required following a manual process copying the database file to the other mirror members, coordinated with API calls to register the database. Starting with this release, the new database can be created automatically on all mirror members and global data is downloaded automatically, without requiring file copies. These improvements significantly simplify the setup of comple x mirrored environments, although attention should be paid to the size of the database being added to the mirror, as file copies may still be a practical solution when the database being added already contains a large amount of data. Please refer to the API reference for more details on the new option.

Command-line ECP management utility

This release introduces a new ^ECP command line utility to perform common ECP management tasks, similar to existing ^SECURITY and ^DATABASE utilities. This means administrators of ECP environments no longer need to rely on the Management Portal for most configuration tasks.

FIPS 140–3

InterSystems can now interact with the cryptographic libraries of FIPS 140–3. Previous versions supported FIPS 140–2, so this is an important upgrade for users that require the latest FIPS-compliant libraries.

### 3.6 Other Enhancements and Efficiency Improvements

#### 3.6.1 Observability with OpenTelemetry

The 2024.3 release included a built-in exporter for OpenTelemetry that collected both metrics published in the Open Metrics API and structured logs. Your applications can add to these metrics and logs with other existing APIs.

New in InterSystems IRIS 2025.1

The 2025.1 release further adds the ability to publish traces. Each trace describes the steps and timing used to handle requests. Typically, these start with a web request and can be used to show how long each part of your request takes to process. Basic tracing can be turned on simply. If you want more than the basic information, you can further augment your application.

The following image shows what trace information looks like.

#### 3.6.2 Updated Interfaces for Production Configuration and DTL Editor Applications

The user interfaces for the Production Configuration and DTL Editor applications ha ve been updated to provide modern user experiences. Changes are limited to these two applications, not broader functionality, and are further explained below. All other screens remain in the Standard user interface. You can fle xibly switch between the modernized and standard views.

Production Configuration

See Introduction to Configuration Tasks for more information.

- Production Configur ation: Supported in this version of production configuration: Creating/Editing/Copying/Deleting Hosts / Stop/Start Hosts / Editing Production Settings / Stop/Start Productions.

- Source Control Integration: Support for source control integration for the above configuration functionality is available.

- Split Panel View: Users can open the Rule Editor and DTL Editor directly from the Production Configuration screen to edit and view rules and transformations included in the production in a split-panel view.

- Enhanced Filtering: A search box at the top enables you to search and filter across all b usiness components, including multiple categories, DTLs, and sub-tranforms. Use the left sidebar to search independently of the main panel to view search results across hosts and categories.

- Bulk-Editing Host Categories: You can add a new category or edit an existing category for a production by adding hosts from the production configuration.

- Expandable Routers: Routers can be expanded to view all rules, transformations, and connections inline.

- Reworked Host Connection: Direct and indirect connections are now rendered when a business host is selected, allowing you to see the full path a message can take. Hover over any outbound or inbound host for further differentiating connections. The Show Connected Hosts Only toggle filters on the selected hosts and its connections.

DTL Editor

See Introduction to DTL Tools for more information.

- Source Control Integration: Support for source control integration is available.

- VS Code Integration: Users can view this version of the DTL Editor in their VS Code IDE.

- Embedded Python Support: Embedded Python support extends to this version of the DTL Editor.

- DTL Testing: DTL Test utility is available in this version of the DTL Editor.

- Switch Panel Layout: The DTL editor supports a side-to-side and top-to-bottom layout.

- Undo/Redo: Users and undo and redo all actions that have not yet been saved with the undo and redo buttons.

- Generate Empty Segments Parameter: The new GENERATEEMPTYSTATEMENTS parameter generates empty segments for missing fields.

- Sub-transforms Viewing: Users can view sub-transforms by clicking the eye-shaped icon to open the subtransform DTL in a new tab.

- Scrolling: The DTL Editor now offers independent scrolling and joint scrolling. With independent scrolling, the left (source) and right (target) sections of the DTL editor can be scrolled independently by positioning the cursor above once of the sections and using the scroll wheel or trackpad to move through each section separately. With joint scrolling, you can scroll through both the source and target sections by placing the cursor in the middle of the diagram.

- Field Autocomplete: Autocomplete is available for source, target, and condition fields, as well as for the Source Class, Source Doc Type, Target Class, and Target Doc Type.

- Ordinal Numbering: The visual editor allows you to toggle on and off the view of the ordinal numbers and full path expression for each segment.

- East References: When a field in the Action Editor is focused, double clicking a segment in the Graphical Editor inserts the corresponding segment reference at the current cursor position in the Action Editor.

- Synchronization: Click an element in the visual editor to highlight the corresponding row in the action editor.

#### 3.6.3 Support rsa-sha2-256 and rsa-sha2-512 host key algorithms

InterSystems IRIS now supports rsa-sha2-256 and rsa-sha2-512 HOSTKEY algorithms for SSH and SFTP connections.

New in InterSystems IRIS 2024.3

This page describes the new features, enhancements, and other significant updates in the 2024.3 release of InterSystems IRIS® data platform, which is an continuous delivery (CD) release.

For other information you may wish to consider related to changes included in this release, see Known Issues and Notes. For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 4.1 Release Information for 2024.3

The current release is 2024.3. The posting for 2024.3 is build 2024.3.1.228.0.

### 4.2 Enhancing Developer Experience

Ability to Resend Messages from Visual Trace

This feature introduces a simple “Resend” button in Visual Trace, making it easier for users to resend messages directly from the trace without performing complex message searches. This significantly reduces the time required to correct message flo ws in integration scenarios.

Enhanced Rule Editor Capabilities

Several enhancements have been introduced to the rule editor, improving its usability and scalability:

- Add Filter by Rules: Adds a toolbar filter to simplify rule vie wing and editing.

- Auto Scroll to Specific Rule: Automatically scrolls to a specific rule within the editor .

- Support for Large Rule Sets: Enhances the ability to handle and manage large rule sets.

### 4.3 Enhancing Analytics and AI

Vector Search Enhancements

Vector Search, introduced with InterSystems IRIS 2024.1 as an experimental feature, is now fully supported for production use.

New in InterSystems IRIS 2024.3

This release significantly e xtends the Vector Search capability introduced with InterSystems IRIS 2024.1.0. Optimization of the low-level vector similarity operations and a more tailored storage model for vector data has yielded a 3-4x speedup of raw vector search speed.

This release also introduces a new EMBEDDING datatype that automates the creation of vector embeddings for text or other content captured in another column. This removes the need for user code to invoke an embeddings model and pass those vector embeddings in manually when ingesting new rows. An EMBEDDING column simply refers to a source column in the same table, and a named configuration that defines the specific embeddings model or service to use.

For more about these new capabilities, see Using Vector Search.

Adaptive Analytics Updates

InterSystems IRIS Adaptive Analytics version 2024.1.3 includes AtScale version 2024.1.3 and an updated User
Defined Aggregate Function (UDAF) file. This release includes the following new modeling and BI capabilities:

- Formatting of calculation output based on the field input rather than just the format defined on the calculation. This is particularly useful for calculations that cannot have a standard output format, such as year-over-year growth in dollars, euros, or time.

- Support for the following MDX functions: DatesPeriodsToDate, DatesMTD, DatesQTD, DatesWTD,
DatesYTD.

- Support for Microsoft Excel’s custom pivot table dimension grouping functionality. This enables you to create custom groups within Excel, without having to make changes to your models. This change also includes support for session sub-cubes, naming, totaling, filtering, and ungrouping.

For more detail on AtScale 2024.1.3, see the AtScale release notes.

For more information about Adaptive Analytics, refer to the InterSystems documentation and online learning content.

### 4.4 Enhancing SQL and Data Management

Enhanced SQL Query Plans

SQL query plans now may include informational and warning messages to inform users about possible opportunities to improve the query structure, schema, or system settings. Messages may include warnings about tables lacking statistics, indices that are marked as non-selectable, collation mismatches, and more. Future releases will expand the types of messages users may see, and include mechanisms to easily aggregate and consume this information for at the namespace level.

Common Table Expressions for DML Statements

The WITH clause, used to define Common Table Expressions (CTEs) at the beginning of a statement, can now also be used in DML statements. This means complex INSERT ... SELECT statements, or UPDATE and DELETE statements with a complex FROM clause, can now be simplified with upfront CTE definitions, increasing the overall readability of the statement.

### 4.5 Enhancing Speed, Scale, and Security

Selective SQL Auditing

Administrators can now define more fine-grained auditing policies for SQL statements, refining them based on statement type in addition to the access mechanism (database driver, Dynamic SQL, or Embedded SQL) as was available before. For example, a policy may audit all statements that modify data (DML statements), but ignore queries that only read data.

Faster Expansion of Database and WIJ Files

On Linux and Unix platforms, InterSystems IRIS will now use fast storage allocation functionality when available in the underlying filesystem to e xpand databases and WIJ files. Pre viously, database expansion happened through writing empty blocks, whereas the new approach involves a metadata operation only, improving the speed of database and WIJ file e xpansion as much as 50 to 100-fold. The filesystems for which this ne w approach is supported are XFS, ext4, Btrfs on Linux, and JSF2 on AIX. Other platforms and filesystems may see limited impro vements thanks to other optimizations to the expansion code introduced in this release.

Convert Non-sharded Tables to Sharded

Starting with this release, users can convert a non-sharded table to a sharded table and vice versa, even when data is present in the table. Using a new ALTER TABLE ... CONVERT command, you can change not only the table’s storage definition, b ut also distribute data from the shard master database across shards (or vice versa). This is an online operations, and applications and queries can continue to read from and write to the table while conversion is running. API methods are available to check progress for this potentially long-running operation.

Support for Larger String Fields in Columnar Storage

When using Columnar Storage to achieve top analytical query response times, data is organized in $vector chunks
holding up to 64000 values at a time. For string fields with high cardinality (man y distinct values), these data structures risked hitting lower level limitations on what can be stored in a single unit, and we automatically reverted the storage mode of such columns to row layout based on the column's defined string length. With this release, we're introducing a mechanism to automatically adjust the chunk size based on the column's defined length, such that longer string sizes can still be treated using columnar storage and benefit from f ast response times when used in analytical queries.

### 4.6 Other Enhancements and Efficiency Improvements

New IRISMETRICS Database

A new system database IRISMETRICS has been introduced for storing interoperability usage metrics. No customer application should directly interact with the IRISMETRICS database, which exists purely for internal use by
InterSystems IRIS.

New in InterSystems IRIS 2024.3

### 4.7 Platform Updates

Remove Support for OpenSSL 1.x on AIX

InterSystems has provided two fla vors of kits for AIX users this year: one that supports OpenSSL 1.x and one that supports OpenSSL 3.x. Starting with the current 2024.3 release, InterSystems will only provide kits that support OpenSSL 3.x.

New in InterSystems IRIS 2024.2

This page describes the new features, enhancements, and other significant updates in the 2024.2 release of InterSystems IRIS® data platform, which is an continuous delivery (CD) release.

For other information you may wish to consider related to changes included in this release, see Known Issues and Notes. For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 5.1 Release Information for 2024.2

The current release is 2024.2. The posting for 2024.2 is build 2024.2.0.247.0.

If you are running AIX OpenSSL 1.x, the posting is build 2024.2.0.247.1.

### 5.2 Enhancing Developer Experience

#### 5.2.1 Removal of Studio

Windows installations of this 2024.2 release do not include the Studio IDE and upgrading an existing instance to this version removes Studio from the instance’s bin directory. Developers who wish to continue using Studio should download the
### 2024.1 version of the Studio component independently from the WRC component distribution page.

Note:

Re-installing Studio as a component does not destroy or modify your existing registry settings, ensuring continuity between your Studio configuration data. The 2024.1 version of the Studio component is forward compatible, so it can connect with 2024.1+ versions.

The 2024.1 version of the Studio component will be available on the WRC distribution page will be available for a minimum of 24 months following the release of 2024.2.

#### 5.2.2 Full Support for Foreign Tables

In the 2023.1 release, InterSystems introduced foreign tables as an experimental feature and worked closely with early adopters through the Early Access Program to solicit feedback on critical features for the full version. With the 2024.2 release, InterSystems has addressed a majority of the feedback, including better metadata management, improved predicate pushdown, and further alignment with the LOAD DATA command that ingests, rather than projects, external data into

New in InterSystems IRIS 2024.2

SQL tables. As part of the promotion out of the experimental status, this release also finalizes the pri vilege model for managing foreign tables and servers, and running statements against them.

Note:

If you are currently using foreign tables with regularly-privileged users (specifically , users that do not have the %All privileges), you may have to grant the USE object privilege on existing foreign servers to query foreign tables. To manage foreign servers, you may also need to grant the new %Manage_Foreign_Server administrative privilege to the appropriate users or roles.

Another new capability introduced in this release is a new THROUGH command to send a SQL statement directly to a foreign server. This new command can be used in exploration scenarios, ahead of a creating a new foreign table after asserting the returned results match expectations.

Foreign tables are now fully supported for production use and all documented APIs can be considered final. InterSystems will continue to enhance the capability, but preserve compatibility with the interfaces available in this 2024.2 release.

#### 5.2.3 Flexible Python Runtime for Microsoft Windows

Customers running on Windows are now able to select the Python runtime used for Embedded Python. You can choose Python 3.9 or higher, including Anaconda, to meet your organization’s needs. Linux users have been able to select their Python runtime since the 2024.1 release.

### 5.3 Enhancing Analytics and AI

#### 5.3.1 Business Intelligence

The 2024.2 release includes some enhancements to business intelligence. In particular:

- Standard KPI plugins have been added to calculate the standard deviation and variance based on measures from fact tables.

- Changes that provide better integration with the PowerBI connector privileges so that the PowerBI user has access to all cubes that are not restricted by a resource or are public cubes.

#### 5.3.2 Reports

The 2024.2 release includes a new version of Logi Report 2024.1 SP2, including enhancements to PDF exports. For additional details, see the Logi Report release notes.

#### 5.3.3 InterSystems Connector for Power BI

Beginning with the Microsoft Power BI July 2024 release, the connector which InterSystems provides for Power BI has been renamed from the InterSystems IRIS (Beta) Connector to the InterSystems Health Insight Connector. For clients who have built reports or dashboards using the InterSystems IRIS (Beta) Connector, please follow the instructions provided in Cannot Connect to Data Source for Existing Report or Dashboard to update your connections.

Enhancing Cloud and Operations

### 5.4 Enhancing Cloud and Operations

Containers for the 2024.2. release of InterSystems IRIS are based on Ubuntu 24.04.

### 5.5 Enhancing Speed, Scale, and Security

#### 5.5.1 SQL Performance

The 2024.2 release includes a number of enhancements that benefit SQL query performance:

- When ingesting large volumes of data into tables using columnar storage, a new JDBC driver optimization will speed up ingestion as much as an order of magnitude.

- Use of the YEAR, ISNULL, NVL, and COALESCE functions in SQL queries now trigger additional optimizations that should lead to more efficient query e xecution strategies.

- Query processing now makes broader use of global temporary tables (shared by multiple worker processes) and adaptive parallel execution (such as when using the %FIND operator), enhancing overall performance.

#### 5.5.2 JobServers

The behavior of the JobServers parameter has been updated. Previously, new jobs servers were not created to replace ones that were utilized, and the parameter set both the total number and the number created upon start up.

With the update, the JobServers parameter still sets the number of job servers created at start up, but it also determines the target number of available job servers the system will maintain. As job servers are utilized, more are created so there are always available job servers.

### 5.6 Platform Updates

#### 5.6.1 Ubuntu Version Support

The 2024.2 release adds platform support for Ubuntu 24.04.

Ubuntu 20.04, which was supported in earlier versions, is no longer a supported platform.

New in InterSystems IRIS 2024.1

This page describes the new and enhanced features in the 2024.1 release of InterSystems IRIS® data platform, which is an extended maintenance (EM) release. Some of these features were also available in the continuous delivery (CD) releases since 2023.1, the previous EM release.

For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 6.1 Release Information for 2024.1

The current release is 2024.1.5. The posting for this release is build 2024.1.5.649.0.

### 6.2 Enhancing Developer Experience

#### 6.2.1 Using vectors in ObjectScript

As part of the new Vector Search capability (see related note in the Enhancing Analytics and AI section), InterSystems is
making the $vector ObjectScript language feature available to all developers. InterSystems introduced $vector as an internal-
only feature in 2022.2 to address the need for a new datatype and corresponding set of operators to work with large arrays of elements of a single datatype, and its highly efficient encoding format and use of SIMD functions for b ulk operations contributed to the order-of-magnitude performance improvements brought by Columnar Storage. The Vector Search capability introduced with this release offers another use case for working with this kind of datatype, notably to capture embeddings and to perform fast bulk operations on the entire vector at once. Given the feature addresses two distinct use cases in modern computing challenges well, InterSystems has decided to make the feature available to all ObjectScript developers.

You can find full documentation of the ne w syntax and the current set of operators in the ObjectScript reference.

At first sight, you may think $v ector has a lot of overlap with $list and wonder which one to use. They are, however, distinct
features that server different use cases. In general, if you are dealing with a single datatype and always access and operate
on data elements in bulk, you may fit the $v ector use case.

New in InterSystems IRIS 2024.1

#### 6.2.2 Support for JSON_TABLE

InterSystems IRIS 2024.1 introduces support for the JSON_TABLE function according to the SQL standard. This function, intended for use in the FROM clause of a query, maps JSON values to columns in a relational table, enabling you to query JSON data in the context of SQL and providing very powerful capabilities in combination with lateral joins.

#### 6.2.3 SQL Development

The SQL standard includes a WITH clause that helps in breaking complex nested queries down into small blocks, similar to how you’d use SQL views, but restricted to a single statement. In 2024.1, you can now use such Common Table Expressions (CTEs) in SELECT statements to add more structure and transparency to your queries. Many tools that generate SQL statement can also use CTEs.

As with each release, InterSystems IRIS SQL 2024.1 includes a number of enhancements that improve query performance:

- When executing queries, any intermediate results that can be shared between different worker threads are now cached.

This saves significantly on I/O when running comple x queries on large datasets.

- Space efficienc y for tables that use columnar storage where all table columns meet the requirements for pure columnar storage has been optimized.

- The Adaptive Parallel Execution mechanism introduced in prior releases now applies to a broader set of queries, including those that employ complex conditions, and virtually eliminates the cases in which traditional parallel subqueries would be used in the background.

- The set of cases where filter and other query predicates for statements in volving foreign tables can be pushed down to a remote database has been expanded. This makes foreign tables more performant by limiting the amount of data that gets passed back to your instance of InterSystems IRIS.

#### 6.2.4 Flexible Embedded Python Runtime

Flexible Python Runtime allows an administrator to choose the Python runtime that Embedded Python uses. This is perfect for upgrading to a specific v ersion of Python or using a distribution like Anaconda. The Python runtime library can be configured through the Configuration P arameter File. This feature is available only for Linux-based builds of InterSystems IRIS in 2024.1

#### 6.2.5 Embedded Python for AIX

Embedded Python is now available on AIX systems.

#### 6.2.6 Python BPL Editor

The Business Process Language editor now gives developers the option to write their business processes using Python. While most BPL scripts require no coding, there are a few blocks that enable the developer to implement their own logic in ObjectScript, JavaScript, or (new in the 2024.1 release) Python.

#### 6.2.7 WSGI Web Apps

InterSystems IRIS 2024.1 includes, on an experimental basis, the ability to create, secure, and host Web Applications that conform to the Python WSGI standard. With this enabled, you can run WSGI-compliant frameworks, such as flask or Django, inside your instance and take advantage of all the power of Embedded Python for moden Python web development. Even better, authentication is handled by the Web Gateway just like with all web applications. This feature is experimental in the 2024.1 release.

InterSystems welcomes feedback on how well this feature meets your needs.

### 6.3 Enhancing Analytics and AI

#### 6.3.1 Vector Search

Vector Search is a new experimental feature in InterSystems IRIS 2024.1 that provides the core functionality for semantic and vector-powered search of structured data, the cornerstone of generative AI applications, such as those implementing the Retrieval Augmented Generation (RAG) pattern. Vector search in 2024.1 comprises a new VECTOR SQL datatype and a set of related functions, including TO_VECTOR (which converts strings to vectors) and both VECTOR_DOT_PROD- UCT and VECTOR_COSINE (which compute similarity between vectors).

In a typical application, specialized statistical language models called “embedding models” (smaller versions of LLMs like ChatGPT) convert sequences of text (or images, if the embedding model has been trained to process images) into embedding vectors, dense numeric arrays that specify a point in high-dimensional “latent embedding” space. Vectors are then stored in a SQL table column and the similarity functions are used to compare them to an input or query vector, the result of applying the same embedding model to the query string. The results of that search are the most similar vectors, and this can be a higher quality search capability than traditional “keyword” search because the embedding models have been trained to capture the “semantics” of the text. Future releases of InterSystems IRIS will increase the speed of search and introduce SQL syntax that abstracts the process of converting stored text as well as queries into vectors thereby providing a convenient way to implement powerful “semantic search” over data in InterSystems IRIS without having to deal with the underlying vectors directly.

#### 6.3.2 Business Intelligence Improvements

InterSystems continues to improve the performance of InterSystems IRIS BI. In this release, the Analyzer user interface’s
filter list management has been enhanced. In addition, this release includes:

- Handling of deeply nested AND/OR conditions in the Advanced filters in Analyzer. This change introduces a means for computing structures consisting of deeply nested CROSSJOIN and %OR functions in MDX slicer clauses.

- Enhanced APIs to allow accessing pivot table and dashboard metadata to allow for other visualization user interfaces to access that stored data.

### 6.4 Enhancing Speed, Scale, and Security

#### 6.4.1 Multi-Volume Databases

As customer databases grow, so do database files. To avoid those files becoming unmanageably lar ge, or hit hard filesystem limits, InterSystems IRIS now supports splitting your database across multiple physical “volumes” transparently. This new capability is easily configured: for an y database, you can now configure a threshold size. When your initial IRIS.DAT file is about to hit this size and ne w global data needs to be written, InterSystems IRIS will transparently create a new “database volume” file and start writing ne w data to that file. When that volume hits the threshold, another file is created, and so on.

There is no impact on applications and code accessing the data, as they continue to see the full database's content, no matter how many volumes it might be spread across. Furthermore, you can configure which directory the ne xt volume should be

New in InterSystems IRIS 2024.1

created in, and when needed, you can rearrange database volumes across directories as a maintenance operation. Combined with planned work to increase the overall maximum database size, this will ensure your data remains easy to manage, well into the petabyte range.

#### 6.4.2 Fast Online Backup

InterSystems for a long time has offered two main backup options: External Backup and Online Backup. With External Backup, users can freeze the write daemon for a brief period of time such that external solutions can create a consistent snapshot of all database, journal and other files. Those external solutions may track what changed versus the previous snapshot to produce an incremental snapshot that is much smaller than a full copy. In Online Backup, InterSystems IRIS tracks which blocks changed, and can produce incremental backups while the system remains fully online (with only a very brief pause in writing).

This release introduces a new mechanism for incremental and full backups to the Online Backup feature, writing separate backup files per database using parallel processes. F or large systems with many databases, this provides very significant improvements in the overall time it takes to perform a backup. The new Backup.Online class is the entry point for the new capability.

Important:

This change is the first part of a broader major project impro ving the performance and interface of the Online Backup feature, and covers the parallelism described above. As we intend to make further changes to the API and output format, the new API is currently labeled as experimental.

InterSystems welcomes feedback from customers through the Early Access Program and look forward to incorporating such feedback in an upcoming release.

During this phase, the pre-existing API in Backup.General and other utilities continue to invoke Online Backup’s pre-existing implementation and can continue to be used without any changes.

### 6.5 Platform Updates

#### 6.5.1 Minimum Supported CPU Models

InterSystems IRIS 2024.1 now has set a minimum CPU instruction set policy for Intel and AMD (amd64/x86_64) processors. InterSystems now requires all CPUs to have the AVX and BMI instructions, which are generally available on the following
CPU architectures:

- For Intel processors: Haswell and up

- For AMD processors: Steamroller and up InterSystems is taking advantage of newer instructions to improve product performance. InterSystems IRIS 2024.1 takes advantage of the AVX instruction to reliably speed up vector operations.

#### 6.5.2 Operating System Updates

InterSystems IRIS 2024.1 will support Ubuntu 24.04 shortly after the OS is generally available.

MacOS Sonoma is added as a supported version of MacOS.

New in InterSystems IRIS 2023.1

This page describes the new and enhanced features in the 2023.1 release of InterSystems IRIS®, which is an extended maintenance (EM) release. Some of these features were also available in the continuous delivery (CD) releases since 2022.1, the previous EM release.

For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 7.1 Release Information for 2023.1

The current maintenance release is 2023.1.6. The posting for 2023.1.6 is build 2023.1.6.810.1.

### 7.2 Enhancing Analytics and AI

#### 7.2.1 Columnar Storage

Columnar Storage is a new storage option for InterSystems IRIS SQL tables. Columnar Storage offers analytical queries which are an order of magnitude faster than traditional row queries on InterSystems IRIS. Such queries typically aggregate data over very large tables and typically involve filters and groupings on one or more columns. By laying out the table data by column rather than by row (which works best for transactions on a handful of rows at a time), we can dramatically reduce the amount of I/O required to run such queries and exploit modern chipset-level optimizations called SIMD (Single Instruction Multiple Data) to further improve performance as part of vectorized query processing.

Note:

This capability first became a vailable in InterSystems IRIS 2022.2 as an experimental feature. It is now fully supported for production use in 2023.1, with the exception of using columnar storage for sharded tables. Support for this combination will be delivered in a future release. Customers who used the experimental version of this capability should reload all columnar table data after upgrading to 2023.1.

For more details, see Choose an SQL Table Storage Layout.

New in InterSystems IRIS 2023.1

### 7.3 Enhancing Speed, Scale, and Security

#### 7.3.1 Foreign Tables

This release introduces a new capability for leveraging external data in InterSystems IRIS. To any SQL queries you write in InterSystems IRIS, Foreign Tables present themselves as regular InterSystems IRIS tables. However, their data is not physically stored within the InterSystems IRIS server. They may be in remote files, third-party databases (on-prem or DBaaS), or a separate InterSystems IRIS server to which an ECP connection would not be practical. In other words, the data in these tables is not managed by the InterSystems IRIS instance, but it is projected to the InterSystems IRIS instance.

InterSystems IRIS 2023.1 includes support for projecting data from CSV files and JDBC data sources. The JDBC option leverages existing SQL Gateway infrastructure for managing connection details and credentials, and the syntax and capabilities for using file sources is fully aligned with the e xisting LOAD DATA command.

Important:

Foreign Tables are available in InterSystems IRIS 2023.1 as an Experimental Feature. This means they are not supported for production environments. However, the feature is well-tested and InterSystems believes it can add significant v alue to customers.

InterSystems is looking for feedback on this new capability based on customers’ use in real-world environments. Please reach out on the Developer Community or contact the Worldwide Response Center (WRC) if you would like to share your experiences or you have questions.

For more details, see Foreign Tables.

#### 7.3.2 Memory Settings

New installations of InterSystems IRIS now use smarter defaults for shared memory and lock table size settings. The new uffer size (which, in turn, considers available defaults apply best practice configurations based on the configured global b system memory if not set by the user) and work well for most workloads. As before, users may still override these defaults with specific v alues. Existing settings are not affected.

#### 7.3.3 Platform Scalability

This release includes a number of scalability enhancements that enable large production deployments to meet highly demanding workloads. These enhancements include the asynchronous reading of journal files during de-journaling and changes to the infrastructure of the Enterprise Cache Protocol (ECP) which optimize resource usage and limit contention under very high load.

### 7.4 Platform Updates

This release adds support for the following new server platforms:

- macOS 13 (Ventura) New in InterSystems IRIS 2022.1 This page describes the new and enhanced features in the 2022.1 release of InterSystems IRIS®, which is an Extended Maintenance (EM) release. Some of these features were also available in the continuous delivery (CD) releases since 2021.1, the previous EM release.

For a more exhaustive list of the changes included in this release, refer to the Upgrade Checklist.

### 8.1 Release Information for 2022.1

The current maintenance release is 2022.1.7. The posting for 2022.1.7 is build 2022.1.7.1116.1.

This release is the final maintenance release of v ersion 2022.1.

### 8.2 Enhancing Developer Experience

#### 8.2.1 Kafka Messaging Support

This release supports Apache Kafka https://kafka.apache.org/, an open-source distributed event streaming platform used for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications. You can use Kafka in interoperability productions (see Using Kafka Messaging) or use the Common Messaging APIs outside of productions.

#### 8.2.2 Embedded Python

InterSystems IRIS 2022.1 introduces Python fully integrated into the kernel, making Python a full peer to ObjectScript. Almost anything that you can do in ObjectScript, you can now also do in Python, including defining class methods. You can also interleave Python and ObjectScript, including directly calling Python libraries from ObjectScript without writing any Python code. Python provides access to many thousands of high-quality pre-built libraries, which can speed development and lower your maintenance cost. Python developers who are not familiar with ObjectScript can start developing without learning a new language.

Any InterSystems IRIS object can be created and accessed with Embedded Python:

- Objects implemented in embedded Python are treated the same as objects implemented in ObjectScript.

New in InterSystems IRIS 2022.1

- In Embedded Python, you have full and direct access from Python objects to ObjectScript objects and from ObjectScript objects to Python objects.

- Embedded Python has full access to globals, which are accessed as normal Python objects. You can use InterSystems IRIS persistence to store objects in the database, making them available in future sessions until the objects are explicitly deleted.

Embedded Python augments the InterSystems IRIS Python SDK, which includes client libraries and the external Python gateway.

For an introduction to embedded Python, see the Embedded Python Overview.

Note:

Embedded Python is designed to run with whatever version of Python you have installed on your machine.

If you are running Microsoft Windows and do not have Python already installed, the InterSystems IRIS installation kit installs it for you.

Many fla vors of UNIX or Linux come with Python installed. If you need to install it, use the version recommended
for your operating system by your package manager, for example:

- macOS: Install Python 3.9 using Homebrew (https://formulae.brew.sh/formula/python@3.9)

- Ubuntu: apt-get install python3

- Red Hat Enterprise Linux or Oracle Linux: yum install python3

- SUSE: zypper install python3 If you get an error that says “Failed to load python,” it means that you either don’t have Python installed or an unexpected version of Python is installed on your system. Install it or reinstall it using one of the above methods.

On a UNIX-based system, you may want to install Python packages with the pip3 command. If you do not have pip3 installed already, install the package python3-pip with your system’s package manager.

#### 8.2.3 Interoperability Productions in Python

In this release, you can develop interoperability productions in Python using the Production EXtension (PEX) framework. This gives you the choice of developing productions in Python, Java, .NET, or ObjectScript. You can easily combine production components developed in different languages. You can develop in the language you are familiar with even if the other production components were developed in a different language. You can use Python with PEX to create new protocol adapter, perform complex analysis or calculations, and to create persistent messaging and long-running business processes. For more information, see Developing Production Components with External Languages. (first in 2021.2)

#### 8.2.4 Visual Studio Code ObjectScript Extension Pack Updates

The Visual Studio Code ObjectScript Extension Pack is available from the Visual Studio Code download page and has the
following enhancements that make developing code faster and easier:

- Integrated documentation — hover-over in-line documentation, browse class hierarchies, and preview custom class documentation.

- Server-side source improvements — search and support for many client-side web application workflo ws.

- Debugging — inspect properties of objects and improved reliability.

The extension pack includes the ObjectScript extension and the Language Server extension. For more information, see the VSCode ObjectScript Extension documentation. (first in 2021.2)

#### 8.2.5 Make SQL Queries With Minimal Code in Interoperability Productions

In this release, new SQL business services and operations make it easy to perform SQL queries in a production. See Using SQL Business Services and Operations for details. (first in 2021.2)

### 8.3 Enhancing Analytics and AI

#### 8.3.1 SQL Loader

The SQL LOAD DATA command loads data from a CSV file or JDBC source into an SQL table efficiently you to easily populate a table with well-validated data. You can refine the command with COLUMNS and VALUES clauses similar to an INSERT statement and override default behavior with the USING clause, similar to how it’s used in IntegratedML. For details, see LOAD DATA in the SQL Reference. (first in 2021.2)

. This allows

#### 8.3.2 Adaptive Analytics Enhancements

In this release, Adaptive Analytics added two additional features:

- Validation of InterSystems Reports as a client of Adaptive Analytics — now our customers can provide reports using InterSystems Reports with the same data model that is shared with PowerBI, Tableau, and other business intelligence tools. (first in 2021.2)

- Import of InterSystems IRIS Business Intelligence (BI) cubes — we have the ability to export an InterSystems IRIS BI cube definition and import it as a virtual cube in Adaptive Analytics. Please note that there are caveats with this – some things cannot be exported from a cube such as Cube Relationships and cubes based on data connectors – see the Adaptive Analytics documentation for more information. (first in 2021.2)

### 8.4 Enhancing Cloud and Operations

#### 8.4.1 Cloud Connectors

This release contains cloud connectors that make it easier for you to manage InterSystems IRIS applications in Amazon
Web Services and use connectors to access services. This release has the following adapters:

- Inbound and outbound adapters for S3 (Amazon Simple Storage Service) (first in 2021.2)

- Outbound adapter for Cloudwatch (Amazon monitoring service) (first in 2021.2)

- Outbound adapter for SNS (Amazon Simple Notification Service) for messaging (first in 2021.2)

#### 8.4.2 IKO Enhancements

This release makes it easier to deploy and manage InterSystems IRIS in Kubernetes with the following new InterSystem
Kubernetes Operator (IKO) features:

- IKO can deploy and manage InterSystems System Alert and Monitoring (SAM) and the InterSystems API Manager (IAM) with your InterSystems IRIS cluster. This makes it easier to administer and scale your system. (first in 2021.2) New in InterSystems IRIS 2022.1

- IKO can deploy locked down InterSystems IRIS and InterSystems Web Gateway containers. (first in 2021.2)

- IKO can deploy InterSystems Web Gateway containers with Nginx as well as Apache web servers. (first in 2021.2)

- IKO can include ephemeral as well as persistent volumes in deployments. (first in 2021.2)

### 8.5 Enhancing Speed, Scale, and Security

#### 8.5.1 Online Shard Rebalancing

InterSystems IRIS Sharding distributes data and its associated workload across multiple nodes. Even data distributions offer near linear scalability for analytical query workloads. Therefore, if the data volume or workload increases, you may add additional data nodes to meet your performance goals. After adding a data node, a rebalancing operation can be used to redistribute the older data across all available nodes, which enhances the elasticity of sharded clusters. Starting in this release, this rebalancing happens online: users can continue to query and update the data while rebalancing is running. (first in 2021.2)

#### 8.5.2 Adaptive SQL Optimizer

The InterSystems IRIS SQL Optimizer leverages table statistics to derive the best query plan for each user-submitted statement and uses an efficient query cache to reuse the generated code. When those statements include parameters, the values submitted at runtime may provide opportunities for faster execution using an alternative query plan. The new Run- Time Plan Choice (RTPC) infrastructure introduced with this release ensures InterSystems IRIS SQL takes advantage of such opportunities efficiently . RTPC scans for the use of outlier values and efficiently estimates the selecti vity of range conditions based on more detailed table statistics. This leads to more adaptive query planning and significant sa vings in execution time and I/O for many real-world datasets. (first in 2021.2)

In addition, InterSystems IRIS now uses block-level sampling rather than full or row-based scanning to gather the table statistics used by the optimizer. This efficient algorithm enables g athering statistics (such as by using the TUNE TABLE command) for even the largest tables with billions of rows within seconds. Also, InterSystems IRIS SQL will now gather table statistics on-the-fly when a table has none to ensure appropriate query plans. (first in 2021.2)

#### 8.5.3 Saving on Storage

In this release, stream and journal compression can significantly reduce storage needed for your InterSystems IRIS
deployment:

- Stream compression – is now on by default for all globals-based stream classes, with no application change required. Existing data remains readable and will be compressed upon the next write. Experiments with real-world data have indicated compression ratios ranging from 30% for short texts to 80% and more for XML and other document types. (first in 2021.2)

- Journal compression — compresses inactive journal files immediately after journal switch. Rollback and roll forw ard are executed directly from the compressed format. This significantly reduces the storage requirements for this vital part of InterSystems IRIS data integrity strategy. See Journaling Best Practices for more information. (first in 2021.2)

#### 8.5.4 TLS 1.3 Support (OpenSSL 1.1.1)

With this version, InterSystems IRIS includes support for OpenSSL 1.1.1 and fully supports TLS 1.3. With TLS 1.3, users will see faster performance among other improvements, such as cutting the encryption latency in half. This is accomplished by eliminating an entire round trip from the handshake process. (first in 2021.2)

Beginning with InterSystems IRIS 2021.2, we will no longer ship OpenSSL libraries on UNIX but depend on the operating system to provide those. One benefit of this change is that updates to the OpenSSL library no longer requires a ne w installation of InterSystems IRIS but can be performed with the usual operating system updates. For more information on this new approach, see Relationship of TLS Version to Operating System and Its Version. Because InterSystems products require access to the operating-system-provided OpenSSL library, the product will now perform a check during the installation and the startup of an instance. The call can also be manually invoked. See Installing the Required Dependencies for details.

The change to not ship OpenSSL libraries also triggered an adjustment we needed to make for kits. Every kit is specific to a major version of OpenSSL (OpenSSL 1.1.1 is the major version, minor versions are indicated by a letter following the major version, such as OpenSSL 1.1.1f).

On Windows, the kit does install the OpenSSL library.

Note:

If the correct version of OpenSSL is not installed on your UNIX system, the installation will not succeed. You must install OpenSSL and then reinstall InterSystems IRIS. For example, on MacOS, you can install OpenSSL using Homebrew, see https://formulae.brew.sh/formula/openssl@1.1.

#### 8.5.5 New ^TRACE Utility

This release introduces a new tool for tracing raw events from one or more processes. Existing utilities such as %SYS.MONLBL and PERFMON track mostly the same event types but immediately generate a report formatted for a specific type of analysis. The new ^TRACE tool captures these events in a more generic file format and allo ws interactive navigation and summarization of the captured information through a command-line interface or API. Supported event types include, but are not limited to global sets and kills, physical writes, network requests, cache hits and reads, and various journal events. Information captured for these events includes the routine line and call stack, as well as the full global reference where applicable. This offers a single interface for a broader set of performance analysis tasks. (first in 2021.2)

### 8.6 Other Enhancements and Efficiency Improvements

In each release, InterSystems makes many efficienc y improvements and minor enhancements. This release includes:

- DataMove is enhanced for general robustness and for recoverability around mirror failover.

- Separate kits are provided for installing InterSystems IRIS with IntegratedML or without, making the installation process more efficient.

- Compact double support for external clients, including JDBC, .NET clients, Python, and IRISNative. (first in 2021.2)

- In this release, the security tables now have an embedded version number, which allows finer access o ver allowable imports. You can export security tables from version 2021.1 and then import them to this version. For details, see ^SECURITY. (first in 2021.2)

- This release updates the Log4j library to version 2.17.0. (first in 2021.2)

- This release updates the node.js library to version 14. (first in 2021.2) New in InterSystems IRIS 2021.1 This page describes the new and enhanced features in the 2021.1 release of InterSystems IRIS®, which is an extended maintenance (EM) release. Some of these features were also available in the continuous delivery (CD) releases since 2020.1, the previous EM release.

### 9.1 Release Information for 2021.1

The current maintenance release is 2021.1.3. The posting for 2021.1.3 is build 2021.1.3.389.0.

### 9.2 Enhancing Analytics

With InterSystems IRIS 2021.1, customers can deploy InterSystems IRIS Adaptive Analytics, an add-on product that extends InterSystems IRIS to deliver greater ease of use, fle xibility, scalability, and efficienc y to analytics end users regardless of their business intelligence (BI) tools of choice. It enables defining an analytics-friendly b usiness model and transparently accelerates analytic query workloads that run against this model by autonomously building and maintaining interim data structures in the background.

Other enhancements for Analytics use cases include:

- SQL users querying InterSystems IRIS directly now have access to SQL standard Window Functions for easily expressing complex aggregations in a single query. This enables pushing data-intensive calculations typical for reporting and BI use cases closer to the data and improves both net performance and simplicity.

- InterSystems IRIS embedded BI capability will experience measurable performance improvements thanks to enhancements to its native MDX query engine.

### 9.3 Enhancing Developer Experience

InterSystems IRIS 2021.1 introduces a new Python and R Gateway to run code in those languages out-of-process or on a different server as needed. The Python Gateway supports virtual environments, meaning that each Gateway can use its own version of Python to maximize developer fle xibility. All gateways now support starting automatically on first use, as well as simple and secure re-entrant connections. This means, for example, that external code can transparently reach back into

New in InterSystems IRIS 2021.1

InterSystems IRIS for data access without having to explicitly open a new connection and provide user credentials. The .NET Gateway now supports .NET Core 2.1 (first in 2020.3).

New in InterSystems IRIS 2021.1 is the ability to define e xternal stored procedures in SQL. This enables developers to leverage code written in Java, Python or .NET from SQL, using simple SQL syntax. The external code is invoked transparently through the corresponding Gateways. This release also adds SQL user-defined aggre gate functions with CREATE AGGREGATE and DROP AGGREGATE.

This release also adds a number of significant enhancements and e xtensions to the client APIs, including a fully native
Python client SDK that runs on all platforms supporting Python, and support for $list and $order operations in all four
Native SDK languages (Python, Java, C# and Node.JS). The ODBC driver has been enhanced with additional T-SQL support. XEP adds support for deferred indexing and indexes can be built as a background process (first in 2020.3).

Java developers can now take advantage of Java SE 11 LTS. InterSystems tests and supports both the Oracle OpenJDK and AdoptOpenJDK implementations of the standard for all of its Java-based components. See the corresponding section in the Supported Technologies list for more detail (first in 2020.4).

The InterSystems IRIS JDBC driver now fully supports Connection Pooling for efficient managing of database connections from your Java applications. See the Connection Pooling section in the JDBC documentation for more detail (first in 2020.4).

For ObjectScript developers, the VSCode-ObjectScript Version 1.0 is available. VSCode-ObjectScript is an open source extension for the VSCode IDE to enable practical development of ObjectScript applications for InterSystems IRIS. For details, see the VS Code InterSystems ObjectScript documentation.

This release has support for Spark 2.4.4 (first in 2020.3).

### 9.4 IntegratedML Machine Learning

This release includes IntegratedML, a new feature that brings best of breed machine learning to analysts and developers via simple and intuitive SQL syntax (first in 2020.3). De velopers can now easily train and deploy powerful predictive models from within InterSystems IRIS, right where their data lives. For details, see Using IntegratedML and Learn IntegratedML in InterSystems IRIS.

For this release:

- Standard and Community Edition containers are available from the InterSystems Container Registry (ICR). See Using the InterSystems Container Registry for information on the container registry.

- Community Edition containers are also available from Docker Hub.

- Kits (and container tarballs) are available from the WRC Software Distribution site.

Note:

Full installation kits are provided for a subset of server platforms on the WRC. When using the installer, you must specify a custom install and select the IntegratedML option to install it on your system.

### 9.5 Enhancing Operations

This release provides the following enhancements to the deployment and operations experience, both in the cloud and on-
premises:

- The InterSystems Kubernetes Operator (IKO) packages InterSystems IRIS-specific kno wledge and best practices into an easy-to-use, automated tool for provisioning and operating dynamic clusters. Starting with 2021.1, IKO also supports deploying InterSystems System Alerting & Monitoring (SAM).

Enhancing Interoperability

- The InterSystems Cloud Manager (ICM) adds support for InterSystems API Manager (first in 2020.3) and SAM (first in 2020.4) deployments.

- This release include asynchronous mirroring support for sharded clusters (first in 2020.3). Users can no w configure mirroring (synchronous or asynchronous) on an existing cluster, or fail over the entire cluster to the set of asynchronous mirror members in another data center in Disaster Recovery scenarios. See the corresponding section in the Scalability Guide for more details (first in 2020.4).

- The InterSystems SQL syntax has been extended with a set of new commands for managing and configuring your database from a SQL prompt. This enables users with just JDBC or ODBC access to perform most administrative tasks without requiring access to the System Management Portal or an ObjectScript terminal prompt. It includes common tasks such as building indexes and managing frozen plans. For details, see BUILD INDEX, FREEZE PLANS, PURGE CACHED QUERIES, CREATE INDEX, and new options in SET OPTION (first in 2020.4).

- You can now manage Work Queues from the System Management Portal (first in 2020.3).

- The newly available iris-lockeddown container is a security-hardened container image that implements many security best practices, offering peace of mind for customers deploying sensitive applications in complex environments. Users of the Web Gateway container will be pleased to see improvements to its default configuration.

- Starting with 2021.1, InterSystems IRIS is now available for ARM platforms, both as full kits and pre-packaged containers. This enables customers to deploy their applications to cost-efficient hardw are platforms, both physical and in the cloud. For more information, refer to the Supported Platforms guide.

- This release simplifies the deplo yment of InterSystems Reports, the new reporting capability for InterSystems IRIS (first in 2020.4). As part of a closer integration, InterSystems Reports now uses the same user accounts as InterSystems IRIS for managing, building and executing reports. In addition, all configuration and management data for InterSystems Reports uses InterSystems IRIS if the setup scripting is used. A script to complete the initial configuration of InterSystems IRIS Report Server for on-prem deployments and a docker-compose file for Dock er deployments of the Reports Server are both available as part of this release.

### 9.6 Enhancing Interoperability

With InterSystems IRIS 2021.1, customers can deploy InterSystems API Manager (IAM) 2.3, which includes many enhancements broadening the reach of this crucial component in a modern API-centric environments.

There are the following other interoperability enhancements:

- New SOAP Business Service and Business Operation, EnsLib.EDI.X12.Service and EnsLib.EDI.X12.Operation that allow you to use SOAP to receive and send X12 messages (First in 2020.2).

- Improved X12 error handling (First in 2020.2).

- This release adds support for a new "foreach" action, which can be used within Routing Rules used for segmented virtual documents (ASTM, EDIFACT and X12). The foreach action is supported in the Rule Type "Segmented Virtual Document Message Routing Rule". The foreach action can loop over repeating segments in the virtual document and nested loops are supported. This enables developers to build rules that match certain conditions regardless of the position of a segment within a repeating group. For details, see About Actions (first in 2020.4).

New in InterSystems IRIS 2021.1

### 9.7 Block-level Compression Reduces the Overall Storage Footprint (Experimental Feature)

Block-level compression reduces the overall storage footprint (amount of disk required). Depending on the data cardinality (extent of repetition in data values), compression can reduce storage consumption significantly . Sparsely populated data (lots of zeros and spaces in the data) compress much better.

Block-level compression is an experimental feature in InterSystems IRIS 2020.2. This means that it is not supported for
production. The feature is well tested, and compression can provide substantial space savings; however there may be an
impact on performance. In some cases, performance may increase as less data needs to be moved from disk to memory; in
others it could decrease because of the computation to do compression and decompression. Space savings and performance impact will depend on the application and platform.

InterSystems is looking for feedback around the space saving and performance overhead seen on customers' real systems — in test environments. Please contact the Worldwide Response Center (WRC) if you are measuring this in your environment.

Currently, the three compression types provided are zlib, zstd, and lz4. Only data and big string blocks are compressed, although this could be extended to other block types in the future. A given database block is compressed only if the compression will allow freeing at least one 4KB chunk of space on disk. Block compression is only supported on Linux systems that support sparse files.

### 9.8 Other Enhancements and Efficiency Improvements

In each release, InterSystems makes many efficienc y improvements and minor enhancements. This release includes these
improvements:

- You can now use Proof Key for Code Exchange (PKCE) with OAuth authentication. PKCE enables you to securely perform the OAuth exchange from public clients and mitigates the threat of having the authorization code intercepted. PKCE is supported in both the OAuth clients and servers.

- The configuration and utility functions in $SYSTEM.SQL ha ve now been organized thematically in subclasses such
as %SYSTEM.SQL.Functions, %SYSTEM.SQL.Schema and %SYSTEM.SQL.Stats.Runtime, making their signature and behavior more consistent across the board. The old entry points in %SYSTEM.SQL have been deprecated but are still available for backwards compatibility (first in 2020.3).

- You can now use Transact-SQL through JDBC. Please see the Transact-SQL Migration Guide for more on hosting Transact-SQL applications on InterSystems IRIS (first in 2020.3).

- Node.js Native SDK now includes the List class. See Native SDK Quick Reference for Node.js (first in 2020.3).

- Java Messaging Service (JMS) adapter is able to connect to a broader range of servers. (first in 2020.3)

- InterSystems IRIS on Linux has been enhanced to use Asynchronous I/O for writes to database files, as it al ways has on all UNIX® and Windows platforms (first in 2020.3). This is coupled with automatic use of direct I/O instead of
buffered I/O. This change optimizes the disk I/O characteristics for database files in the follo wing ways:

–

–

–

Improves application responsiveness at higher scaling levels by more fairly sharing I/O bandwidth with database reads and journal writes.

Improves integrity check performance by allowing integrity check to read multiple blocks asynchronously.

Improves effectiveness of asynchronous reads performed by $prefetchon.

- InterSystems SQL saw a number of performance enhancements that will speed up many different types of queries when upgrading to this release. A complex customer benchmark composed of millions of queries ran 6% faster on
### 2020.4 and 2021.1 compared to earlier releases.

- This release introduces a new algorithm for estimating field selecti vity when gathering table statistics. This improves the ability of the SQL optimizer to choose the fastest query plan for any given SQL statement (first in 2020.4).

- For a number of applicable scenarios, the SQL engine will now use a kernel-level iterator to read through temporary results. This simplifies generated code and can speed up certain steps in a query plan, such as sorting, by up to 40% (first in 2020.4).

- Recent updates to browser security have changed handling of third-party cookies. These updates use the SameSite attribute to reduce the risk of cross-site request forgery (CSRF) attacks, unauthorized access to data, and other possible security issues. Chrome (starting with v.84) enforces stricter rules for SameSite behavior, and these rules can cause issues with existing websites and web applications. These issues may include login problems, the login page being displayed repeatedly, and page elements not displaying properly. In previous versions, you could not modify the
SameSite attribute; hence web applications running on these versions may have such issues.

- This release (first in 2020.4) solv es these problems by setting the SameSite attribute for cookies and by allowing you
to set change the default setting; however, you may need to modify your code to customize values setting the session
cookie scope and the user cookie scope. Additionally, if you are using “SameSite=None”, you must ensure that your web application can support secure HTTPS connections. For details, see About the SameSite Attribute.

- This release improves performance on newly installed systems where the database cache size has not been configured. ge Pages for optimal Under most circumstances, you should carefully configure cache sizes and Configure Huge and Lar system performance. Configuring cache sizes is especially important for li ve production systems, systems with heavy loads, and systems with multiple instances. (first in 2020.3) This release improves security of the command-line history by not recording it if the user is ‘root’ or has administrative
privileges. Usually command line history is written to ~/.iris_history, where ~ expands to the value of $HOME (the
user's home directory). If you scroll before the first command in the current session, the command history from the log is used. When the user is 'root' command history is not written to the log or read from previous sessions so as not to expose any commands executed as superuser.

New in InterSystems IRIS 2020.1

This document describes the new and enhanced features in the 2020.1 release of InterSystems IRIS®. It addresses the new features in 2020.1 that were not present in the 2019.1.0 version (see New and Enhanced Features for InterSystems IRIS 2019.1). Some of these features were first introduced in a 2019.1 maintenance release or in a 2019.2, 2019.3, or 2019.4 continuous delivery release. These features are identified in the descriptions. The following sections describes the 2020.1
release and its new capabilities and enhancements:

- Continuous Delivery releases of InterSystems IRIS

- –

- – Open API/Swagger Specification-First REST De velopment

- InterSystems Reports

- Client Language Enhancements

- –

- –

- InterSystems IRIS Native API for Python InterSystems IRIS Native API for Node.js – Relational access for Node.js

–

Java and .NET Gateway Reentrancy

– Native API for Java and .NET Enhancements

–

Execute TSQL Code via JDBC

New look in the Management Portal

SQL Enhancements

– Universal Query Cache

– New PEX Framework for Coding Production Components in Java and .NET

–

Port Authority for Monitoring Port Usage in Interoperability Productions

– X12 Validation Enhancements

–

Enhanced DTL Support for X12

New in InterSystems IRIS 2020.1

–

Import X12 Schemas from XSD Files

– MQTT Adapters

- Sharding Enhancements – –

Simplified Architecture

Flexible Sharded Schema Design and Objects Support

– Unified Shard Queue Manager

New Automatic Configuration Customization

Analytics Enhancements

–

–

–

Natural Language Processing Enhancements

Other Enhancements and Efficienc y Improvements

- 10.1 Continuous Delivery Releases of InterSystems IRIS

- InterSystems IRIS 2020.1 is both an extended maintenance release and a continuous delivery release of InterSystems IRIS.
There are now two streams of InterSystems IRIS releases:

- Continuous delivery releases — These releases provide access to new features and are ideal for developing and deploying applications in the cloud or in local Docker containers.

- Extended maintenance releases — These releases are less frequent than the continuous delivery releases but provide the increased stability of maintenance releases. These releases are ideal for large enterprise applications where the ease of getting fix es in maintenance releases is more important than getting early access to new features.

- Continuous delivery releases are provided in container format and are available on Amazon Web Services (AWS), Google Cloud Platform (GCP), Microsoft Azure, Docker Hub, and the InterSystems WRC download site. You can run a continuous delivery release on any of these cloud platforms or a local system using Docker container. InterSystems does not provide maintenance releases for continuous delivery releases, but instead fix es issues in subsequent continuous delivery releases.

- The initial major extended maintenance release is provided on all InterSystems IRIS Supported Platforms, including UNIX, Windows, the cloud platforms, and the Docker container. Following maintenance releases are provided on all server and cloud platforms in the InterSystems IRIS Supported Platforms, but are not provided on the Docker container. If you are on a Docker container, you can upgrade to a continuous delivery release.

- If your application runs on a non-container platform, you can only use an extended maintenance release for that application
but can consider using the continuous delivery releases for:

- Evaluating new features and testing your custom code — this will reduce your upgrade costs when you upgrade to the next extended maintenance major release.

- Using it for new projects that can be deployed in the cloud or in local containers.

- In addition to providing fully suppported releases, InterSystems provides access to prerelease software for developers who want to get an early look at new features.

### 10.2 API Management

This release includes two new API Management features:

- Open API/Swagger Specification-First REST De velopment

- 10.2.1 InterSystems API Manager This release includes the InterSystems API Manager (IAM) enabling you to monitor and control traffic to and from your web-based APIs. The API Manager was released with the maintenance release 2019.1.1 and the continuous delivery release
### 2019.2 (an early version of 2019.2 did not include the API Manager).

If you are building service-oriented application layers, you are very likely to find the number of APIs you are using quickly rise. The more distributed your environment the more critical it becomes to properly govern and monitor your API traffic. The API Manager enables you easily route all your traffic through a centralized g ateway and forward API request to
appropriate target nodes. This enables you to:

- Monitor all your API traffic in a central spot.

- Plan, document, and update the list of APIs you are using and the servers that provide them.

- Identify issues before they become critical.

- Control API traffic by throttling throughput, configuring allo wed payload sizes, whitelist and blacklist IP addresses and domains, and quickly taking an endpoint into maintenance mode.

- Onboard internal and external developers by providing interactive API documentation through a dedicated and customizable developer portal.

- Secure your API's in a central place.

The API Manager is interoperable, reliant, intuitive, and scalable. You can perform all configuration using a simple webbased user interface, but can also configure the API Manager using API calls, which makes it easy to perform remote deployments,

The API Manager is released in its own container. You can configure the API Manager as a cluster of multiple nodes, but even a single node can handle the load of multiple tens of thousands of requests per second.

For more information, see InterSystems API Manager.

#### 10.2.2 Open API/Swagger Specification-First REST Development

This release enhances the API Management service so that it can generate the ObjectScript code for REST services from OpenAPI 2.0 specifications. This generated code handles the incoming REST call and you only have to write custom code to perform the specific function performed by the service. If you are implementing a service that is already defined in an OpenAPI 2.0 specification, your w ork is significantly reduced. Ev en if there is no existing OpenAPI 2.0 specification, it is much easier to create a new specification than to write the custom code required to define the REST API and the specification also provides documentation and aids anyone developing client code for the service. For details see Creating REST Services. (first released in 2019.2)

New in InterSystems IRIS 2020.1

### 10.3 In-Place Conversion from Caché and Ensemble

This release of InterSystems IRIS allows you to convert an existing instance of Caché or Ensemble to InterSystems IRIS. The conversion process may require some changes to application code, configuration scripts, and other procedures, b ut will be relatively easy for the majority of cases. As with any major upgrade, you should thoroughly test your custom code, including any production business services, processes, and operations, in a test environment before deploying to a live production environment.

Before performing an in-place conversion, it is important that you read the IRIS In-Place Conversion Guide and the Inter- Systems IRIS Adoption Guide for background information on the differences between Caché or Ensemble and InterSystems IRIS. You can download these documents from the InterSystems Worldwide Response Center documents distribution page.

Important:

Only the HealthShare Health Connect and InterSystems IRIS for Health products support the HL7 and DICOM features that are available in Ensemble. The InterSystems IRIS product does not support these features. Consequently, if your Ensemble productions use the Ensemble health care features, you should not perform an in-place conversion to InterSystems IRIS, but should rather convert to InterSystems IRIS for Health or HealthShare Health Connect.

- If you are using Ensemble as a general-purpose data platform for health care development or plan to develop health care applications in the future, you should convert to InterSystems IRIS for Health
### 2020.1 or later.

- If you are using Ensemble as an integration engine, you should convert to HealthShare Health Connect
### 2020.1 or later.

For details, see the InterSystems IRIS for Health Release Notes or the HealthShare Health Connect Release Notes and the IRIS In-Place Conversion Guide and the InterSystems IRIS Adoption Guide.

### 10.4 InterSystems Reports

InterSystems Reports can be used with InterSystems IRIS and InterSystems IRIS for Health. InterSystems Reports is a repackaging of Logi Report (formerly named JReport®), a product of Logi Analytics®. We plan to provide documentation on how to use InterSystems Reports with our database products, but for customers who want to start using InterSystems Reports now, you can start with the Logi Analytics documentation. If you have questions about using InterSystems Reports, contact the Worldwide Response Center (WRC).

### 10.5 Client Language Enhancements

#### 10.5.1 InterSystems IRIS Native API for Python

This release introduces the Native API for Python, which is a lightweight Python interface to the native multidimensional storage data structures that underlie the InterSystems IRIS object and SQL interfaces. The Native API allows you to implement your own data structures by providing direct access to global arrays, the tree-based sparse arrays that form the basis of the multidimensional storage model. By providing direct access to global arrays, the Native API for Python allows you to define v ery efficient storage structures in Python and, consequently , very efficient applications. F or details see Using the Native API for Python. (first released in 2019.2)

New Look in the Management Portal

#### 10.5.2 InterSystems IRIS Native API for Node.js

This release introduces the Native API for Node.js, which is a lightweight Node.js interface to the native multidimensional storage data structures that underlie the InterSystems IRIS® object and SQL interfaces. The Native API allows you to implement your own data structures by providing direct access to global arrays, the tree-based sparse arrays that form the basis of the multidimensional storage model. By providing direct access to global arrays, the Native API for Node.js allows you to define v ery efficient storage structures in Node.js and, consequently , very efficient applications. F or details see Using the Native API for Node.js. (first released in 2019.2)

#### 10.5.3 Relational access for Node.js

This release provides ODBC access to InterSystems IRIS databases to Node.js developers. (first released in 2019.2)

#### 10.5.4 Java and .NET Gateway Reentrancy

This release allows you to use reentry on the Java and .NET Gateway with forward and reverse proxy. Forward and reverse proxy allow freer use of objects. Proxy objects, or object originally created in InterSystems IRIS to represent objects in Java and .NET, will be created in more situations involving method invocation. You can create objects without concern for the proxy objects. (first released in 2019.3)

#### 10.5.5 Native API for Java and .NET Enhancements

The IRIS Native API, which allows you to access InterSystems IRIS data using globals, has been extended to include $LIST
and pass by reference:

- $LIST allows you to easily iterate through data structures without needing to parse them in detail. This supports sce-
narios such as developing Java and .NET applications that access existing global structures from existing applications, as well as simplifying development and speeding performance. (first released in 2019.4)

- Passing parameters by reference allows you to create applications that use less memory, using cleaner code, and have improved performance. Passing by reference provides an effective mechanism for two-way communication between the referencing routine and the function. Any change the function makes to a variable in its formal list is also made to the corresponding by-reference variable in the actual list.

#### 10.5.6 Execute TSQL Code via JDBC

This release provides the ability to execute Transact-SQL (TSQL) code directly from JDBC.

### 10.6 New Look in the Management Portal

This release represents the beginning of a new, more modern look for the Management Portal. In this first phase, the menus and buttons have a new look but the functionality is unchanged. This new implementation provides the basis for future streamlining and improvements to the user interface. (first released in 2019.2)

New in InterSystems IRIS 2020.1

### 10.7 SQL Enhancements

As with every release, InterSystems IRIS includes a number of enhancements to its SQL engine, based on advancements in the underlying software and continuous benchmarking against industry-standard and customer workloads. Customers are likely to observe measurable increases in query throughput for high-load scenarios compared to the 2019.1 release and are encouraged to share their experiences with InterSystems in case there is an opportunity for extending our benchmarking to include specific ne w use cases.

Note that when you upgrade to a new major version, existing Query Plans are automatically frozen. This ensures that a major software upgrade will never degrade the performance of an existing query. For performance-critical queries, you should test if you can achieve improved performance.

This release includes the following enhancements:

- Universal Query Cache

- Improvements to our parallelization engine that enable more types of queries and DML to be parallelized (automatically) and make more efficient use of CPU capacity . (first released 2019.4)

- Sharded queries can now use implicit joins using -> syntax. (first released 2019.4)

- Queries issued from the SQL explorer page in the System Management Portal are executed in the background. While this enables query cancellation and avoids web request timeouts, it also means certain legacy stored procedures that depend on foreground execution and write to the current device may no longer display this logging information properly. (first released 2019.3)

#### 10.7.1 Universal Query Cache

This release introduces a Universal Query Cache, which enables every query (including embedded and class queries) to be saved as a cached query. Previously, the use of embedded SQL meant application code needed to be recompiled in order to pick up current table statistics or newly available indexes. Now, all query plans are managed in a single cache and can be purged (per query, table or namespace) when appropriate. This significantly impro ves the ability for applications to adapt to actual data characteristics when deployed to multiple sites.

Also, all query types can now equally take advantage of more efficient data access implemented in generated query code.

### 10.8 Interoperability Production Enhancements

#### 10.8.1 New PEX Framework for Coding Production Components in Java and .NET

This release includes the Production EXtension (PEX) framework that provides you with a choice of implementation languages when you are developing interoperability productions. In this release you can use Java and .NET to develop business services, processes, and operations and, also, inbound and outbound adapters. In previous releases, you could only code business services and operations, could only code in Java, and had to use a special code generator wizards in the Management Portal. The PEX framework provides the fle xible plumbing that connects your Java and .NET code to the interoperability production components. You can connect your Java and .NET code using PEX with minimal or no ObjectScript coding.
The PEX package includes the following classes:

- EnsLib.PEX.BusinessService

- EnsLib.PEX.BusinessProcess

- EnsLib.PEX.BusinessOperation

- EnsLib.PEX.InboundAdapter

- EnsLib.PEX.OutboundAdapter

- EnsLib.PEX.Message For details, see PEX: Developing Productions with Java and .NET.

#### 10.8.2 Port Authority for Monitoring Port Usage in Interoperability Productions

The Port Authority utility allows you to monitor how ports are used in your interchange systems. The Port Authority examines the business services and business operations in multiple productions and instances to determine which ports are being used on each system. You can determine which ports are free for new services and operations and reserve ports for specific uses. F or details, see Managing Port Usage.(first released in 2019.3)

#### 10.8.3 X12 Validation Enhancements

This release provides two kinds of enhanced X12 validation:

- SNIP levels 1 and 2 validation — validates the X12 message according to the standards developed by the Workgroup for Electronic Data Exchange (WEDI) Strategic National Implementation Process (SNIP).

- X12 element validation — (first released in 2019.1.1 and 2019.2) In previous releases, you could not use SNIP validation and could only validate the overall segment structure. There was no mechanism to validate the contents of the segment.

SNIP allow you to validate that:

- SNIP level 1 — segments are valid , segment order is valid, element attributes are valid, numeric data elements have numeric values, and message conforms to X12 rules.

- SNIP level 2 — meets HIPAA requirements, such as presence of required elements, non-use of elements marked as not used, and values conforming to the code tables.

X12 element validation enables you to validate that:

- Required fields are present and that all fields are allo wed by the schema.

- Number of fields within a se gment and whether they are repeated as allowed by the schema.

- Data types for fields and components are correct.

- Field values conform to the code tables specified.

- Field and components conform to length restrictions.

For details, see X12 Validation.

In this release you can define data transformations for an entire X12 batch including schemas for the interchange en velope, functional groups, and transaction sets. This allows you to process X12 batch messages using a single data transformation without having to use subtransformations. This release also improves the user interfaces and also provides convenience functions that make it easier to handle repeating elements. For details, see Creating an X12 Data Transformation.

New in InterSystems IRIS 2020.1

#### 10.8.5 Import X12 Schemas from XSD Files

In previous versions, you could only import X12 schemas from SEF files or InterSystems proprietary XML format. In this release, you can also import X12 schemas from the newer XSD schema files. F or details, see Loading X12 Schemas.

#### 10.8.6 MQTT Adapters

This release includes MQTT adapters that support Message Queuing Telemetry Transport (MQTT) protocol, which is often used in Internet of Things (IoT) applications. For details, see Using MQTT Adapters in Productions.

### 10.9 Sharding Enhancements

#### 10.9.1 Simplified Architecture

This release introduces a simple and straightforward blueprint for sharded clusters, the node-level architecture, which can be configured through the ne w %SYSTEM.Cluster API. In this cluster architecture, we’ve implemented some best practices on laying out the different foundational elements introduced with sharding in the initial InterSystems IRIS 2018.1 release that will make it significantly easier to deplo y and expand your cluster. As the node-level architecture is essentially a smart way of leveraging the existing infrastructure, it is fully transparent to application code and does not require any changes to existing deployments. For details, see Elements of Sharding and Sharding APIs in the Scalability Guide and see the %SYSTEM.Cluster class documentation in the InterSystems Class Reference. (first released in 2019.2)

#### 10.9.2 Flexible Sharded Schema Design and Objects Support

This release introduces further improvements to how sharding supports designing your application’s schema in the following
ways:

- You can now coshard any two sharded tables. Before, only tables with a common user-defined shard k ey could be cosharded (that is, explicitly defining the shard k ey for an Order and OrderLine table to be OrderID, the field on which they are joined). With this release, you can use COSHARD WITH syntax in DDL or the CoShardWith index keyword to coshard a new table with an existing table that has a system-assigned shard key. This significantly increases the fle xibility for designing your application’s schema, preserving the operational benefits of using system-assigned shard keys. For details, see Create the Tables in the Scalability Guide and Defining a Sharded Table.

- Where previously sharded schema design could only happen through DDL, you can now mark a persistent class (table) as sharded through its class definition, using the ne w “Sharded” class keyword. The class compiler has been extended to warn against using class definition features incompatible with sharding, such as customized storage definitions, at compile time. For details, see Defining a Sharded Table by Creating a Persistent Class.

- You can use the object paradigm to interact with sharded classes. This means you can create new or open existing sharded class instances with %New() or %OpenId() methods and save them with %Save(). The sharding infrastructure will make sure new instances are appropriately distributed across the cluster, fully transparent to the application. Note that this object code will still be executed on the machine your client is connected to.

These sharding enhancements were first released in 2019.2.

#### 10.9.3 Unified Shard Queue Manager

In this release, the Unified Shard Queue Manager impro ves sharding efficienc y when a sharded cluster is being queried by large numbers of clients by queuing up sharded query work rather than spawn individual processes for each shard-local query and potentially flood the system. An efficient algorithm then ensures an appropriate number of w orker processes is used to process work from the queue, based on available hardware and system load.

### 10.10 Infrastructure and Cloud Deployment Improvements

This release contains improvements to the infrastructure and cloud deployment, including the following:

- Tencent Cloud Support — InterSystems Cloud Manager (ICM) now provides end-to-end cloud provisioning and deployment for applications based on InterSystems IRIS and running on Tencent Cloud. (first released in 2019.4)

- Support for Docker named volumes in addition to bind mounts. (first released in 2019.4)

- InterSystems Cloud Manager (ICM) support for elastic scaling — Existing configurations can no w be scaled, that is,
reprovisioned and redeployed with more or fewer nodes. (first released in 2019.2; scale out D ATA nodes and scale
in/out COMPUTE nodes in node-level architecture first released in 2019.4)

- Improved user experience when packaging your own container. (first released in 2019.3)

- InterSystems Cloud Manager (ICM) support for node-level sharding. (first released in 2019.3)

- Containers use non-root default user, which is a container best practice and improves security. (first released in 2019.3)

- ICM support for creating and deploying on a private network, in which bastion servers connect your private network to the public network and provide improved security protection from denial of service attacks. (first released in 2019.3)

- Support for service discovery with secure RPC communication. (first released in 2019.3)

- ICM support for multi-region deployments, which can provide high availability even if an entire region stops functioning. (first released in 2019.3)

- Ability to upgrade ICM and retain knowledge of deployed systems. (first released in 2019.3)

- Containerless Mode — The following were previously restricted but can now be performed: deploying sharded configurations on Google Cloud Platform using containerless mode and deploying the Web Gateway on Ubuntu or SUSE nodes using containerless mode. (first released in 2019.2)

### 10.11 New Automatic Configuration Customization

A new InterSystems IRIS configuration feature enables customization of the configuration parameter file (CPF) of an InterSystems IRIS instance prior to startup, upon which the custom configuration is automatically implemented. This feature greatly simplifies automation and supports the use of configuration management tools such as K ubernetes with InterSystems IRIS, and is also included in ICM in this version. Automatic configuration customization is an important ne w capability that will be expanded in future versions. (first released in 2019.4)

New in InterSystems IRIS 2020.1

### 10.12 Analytics Enhancements

This release contains the following analytics enhancements:

- 10.12.1 Selective Cube Build

- This release provides Selective Cube Build, a feature of InterSystems IRIS Business Intelligence, that allows you to select the measures and dimensions to be built individually. You can make changes and selectively rebuild without taking the full cube out of service. The user interface also automatically flags the dimensions or measures that ha ve been added or changed so that you know what to rebuild.

- 10.12.2 PowerBI Connector InterSystems customers can now use Microsoft Power BI to access tabular and cube data stored on InterSystems IRIS. This allows combining the data visualization capabilities offered by Power BI with the high-performance data management and querying capabilities offered by InterSystems IRIS. While the connector leverages ODBC, it will also allow customers to access InterSystems IRIS BI cubes directly from Power BI when connecting to InterSystems 2019.2 or above. The connector ships as part of Power BI starting with its April 2019 release. For details, see InterSystems IRIS Connector for Power BI .

#### 10.12.3 Pivot Table Preview

This release contains the Analytics Pivot Table Preview, a new mode for the Analyzer that presents a representative pivot table based on a truncated data set. This will allow previewing a pivot table much more quickly than analyzing the complete result set. A Show All button is also presented when in Preview mode to indicate that the result set is not complete. Selecting the Show All button automatically turns off Preview mode. (first released in 2019.2)

### 10.13 Natural Language Processing Enhancements

This release contains the following natural language processing enhancements.

- InterSystems IRIS Natural Language Processing (NLP) will now extract value and unit information for measurement attributes in the English language model. This information can be visualized through highlighting or retrieved through the query and REST APIs. (first released in 2019.3)

- This release introduces support for the Czech language with InterSystems IRIS Natural Language Processing. The embedded NLP engine will now also identify concepts and their context for natural language text written in Czech as it does for the 10 other languages supported previously. (first released in 2019.2)

### 10.14 Improved Performance and Scalability of the Database

This release has significant optimizations in the database engine. This is especially important for very large systems and significantly increases the ability to scale systems to handle v ery heavy loads.

One of the efficienc y changes in this release improves efficienc y when traversing globals. For a database block in memory that is accessed frequently but not modified often, the system may automatically b uild an optimization structure, called a node table, to speed up searches for nodes within the block. This speeds up global accesses, particularly when access to nodes are sparsely or randomly distributed, or for patterns that access the nodes in reverse collation order (including reverse
$order / $query). The memory for this comes from the database cache itself, a small fraction typically less than one percent.

### 10.15 Other Enhancements and Efficiency Improvements

In each release, InterSystems makes many efficienc y improvements and minor enhancements. In this release these
improvements include:

- Journal performance enhancements.

- Easier configuration for mirrored en vironments.

- Support for new versions of Apache Spark version 2.3 and 2.4.

- Support for WebSocket client in addition to the existing WebSocket server support in the Web Gateway.

- Source Control for Productions — source control hooks have been added to allow check-in and check-out of a production as an entity, simplifying change tracking and configuration management. (first released in 2019.4)

- Whitelists to Support Penetration Testing — customers performing their own security penetration testing can reduce or eliminate false positives related to CSP, Zen, and REST. (first released in 2019.4)

- Upgrades .NET support to .NET Core 2.1. (first released in 2019.3)

- Improved efficienc y for ODBC database access. (first released in 2019.3)

- Structured logging to improve access to log messages. (first released in 2019.3)

- Improved API to fetch alerts. (first released in 2019.3)

- Compiler now tests for global names that are too long and reports an error. Previously, these global names were silently truncated. (first released in 2019.3) Maintenance release 2019.1.1, continuous delivery release 2019.3, and subsequent releases include the set of changes identified as JournalingGroup2019, which corrects issues associated with journaling and mirroring. The changes associated with these issues are SML2776, SML2781, SML2782, SML2783, SML2785, JO2990, JO3117, JO3137, JO3140, JO3141, RJF391, RJF392, HYY2362, HYY2364, and HYY2373.

New in InterSystems IRIS 2019.1

This page describes the 2019.1 release of InterSystems IRIS®.

This release includes new capabilities and enhancements in the following areas:

- Extended Maintenance and Continuous Delivery Releases of InterSystems IRIS

- InterSystems Cloud Manager

- Client languages

- Improved scalability and operations for sharded clusters

- SQL performance

- Analytics

- Interoperability

- New Features in 2019.1.1 Release:

- – – – X12 Element Validation in Interoperability Productions

### 11.1 Extended Maintenance and Continuous Delivery Releases of InterSystems IRIS

InterSystems IRIS 2019.1 is an extended maintenance delivery release of InterSystems IRIS in contrast with InterSystems
IRIS 2019.2, which is a continuous delivery release. There are now two streams of InterSystems IRIS releases:

- Continuous delivery releases — These releases provide access to new features and are ideal for developing and deploying applications in the cloud or in local Docker containers.

- Extended maintenance releases — These releases are less frequent than the continuous delivery releases but provide the increased stability of maintenance releases. These releases are ideal for large enterprise applications where the ease of getting fix es in maintenance releases is more important than getting early access to new features.

New in InterSystems IRIS 2019.1

Continuous delivery releases are provided in container format and are available on Amazon Web Services (AWS), Google Cloud Platform (GCP), Microsoft Azure, Docker Hub, and the InterSystems WRC download site. You can run a continuous delivery release on any of these cloud platforms or a local system using Docker container. InterSystems does not provide maintenance releases for continuous delivery releases, but instead fix es issues in subsequent continuous delivery releases.

The initial major extended maintenance release is provided on all InterSystems IRIS Supported Platforms, including UNIX, Windows, the cloud platforms, and the Docker container. Following maintenance releases are provided on all server and cloud platforms in the InterSystems IRIS Supported Platforms, but are not provided on the Docker container. If you are on a Docker container, you can upgrade to a continuous delivery release.

If your application runs on a non-container platform, you can only use an extended maintenance release for that application
but can consider using the continuous delivery releases for:

- Evaluating new features and testing your custom code — this will reduce your upgrade costs when you upgrade to the next major release.

- Using it for new projects that can be deployed in the cloud or in local containers.

In addition to providing fully-suppported releases, InterSystems provides access to preview software for developers who want to get an early look at new features.

### 11.2 InterSystems Cloud Manager Enhancements

InterSystems Cloud Manager (ICM) provides you with a simple, intuitive way to provision cloud infrastructure and deploy
services on it. In this release ICM has the following enhancements:

- Availability Zone Support — This enhancement allows you to span multiple zones within a given region with cloud providers that provide this facility.

- Asynch Mirror Support — This enhancements lets you configure async mirror members.

- Containerless Support — This enhancement allows you to use ICM to deploy noncontainerized InterSystems IRIS instances from installation kits.

- Service Discovery — Service Discovery mode gives multiple users in any networked locations management access to a single ICM deployment.

### 11.3 Client Languages Enhancements

This release contains the following enhancements and performance boosts to access InterSystems IRIS using client languages:

- IRIS Native API for .NET — Provides low-level access to the underlying global storage from .NET applications.

- Relational access for Python.

- Dynamic Java Gateway.

- Shared memory support for Java Gateway — Support for shared memory connections has been extended to Java Gateway. For more information, see Using Shared Memory Connections in Using Java with the InterSystems JDBC
Driver.

- Hibernate — This release is compatible with Hibernate 5.2 or 5.3. For more information, see Hibernate Support in the InterSystems Implementation Reference for Java Third Party APIs.

- Bulk loader in Java — The bulk loader is a new utility that can be used for massive data transfer from one data source to another.

Improved Scalability and Operations for Sharded Clusters

### 11.4 Improved Scalability and Operations for Sharded Clusters

An InterSystems IRIS® sharded cluster partitions both data storage and caching across a number of servers, providing fle xible, inexpensive performance scaling for queries and data ingestion while maximizing infrastructure value through highly efficient resource utilization. This release provides improved scalability and operations for sharded clusters including
the following:

- Scalability Enhancements — Support a broader set of scalability scenarios for SQL. Data nodes can be now be added to a sharded cluster at all times, irrespective of the database schema and shard keys used. Furthermore, after nodes are added, data can be rebalanced across the available nodes to ensure an even distribution of data and, subsequently, work to improve overall cluster performance. For more information, see Rebalance Sharded Data Across Additional Shard Data Servers in the Scalability Guide.

- Management Portal Enhancements — New page to review and configure the sharded cluster’ s layout.

- API for Backups — A new API for coordinating the creation of backups of a sharded cluster’s data. For details, see Coordinated Backup and Restore of Sharded Clusters in the Scalability Guide.

- Bulk Loader Support — New Bulk Loader client utility also optimizes ingestion of large datasets into a sharded cluster.

### 11.5 SQL Enhancements

This release contains significant enhancements to SQL usability and performance including the follo wing:

- Auto-parallel queries — This release provides improved efficienc y by automatically using parallel queries where appropriate, significantly impro ving throughput for machines with many CPU cores. For more information, see System- Wide Parallel Query Processing in the InterSystems SQL Optimization Guide.

- SQL Usability Enhancements — The new TUNE TABLE command tunes a table based on the data currently in the table and is available from the SQL shell. For more information, see TUNE TABLE in the InterSystems SQL Reference.

- In addition, this release includes several other SQL shell enhancements, such as the ability to browse the schemas, tables, and views defined in or accessible from the current namespace. F or more information, see Using the SQL Shell Interface in Using InterSystems SQL.

- ShowPlan function and EXPLAIN command — Now display sub-plans for composite plans such as parallel and/or sharded queries. For details, see Show Plan.

Comment Options — This release supports Comment Options specified in the SQL code that cause the Optimizer to override a system-wide compile option for that query. For more information, see Comment Options in the InterSystems SQL Optimization Guide.

General performance enhancements — With each release, InterSystems includes various enhancements to its SQL engine that are 100% transparent from the application’s perspective. For 2019.1, an especially broad array of improvements went into the query optimizer and subsequent code generation that define your SQL query performance. Combined with the now automated parallel query execution, InterSystems IRIS SQL users should see a noticeable to significant impro vement in throughput, depending on their query set.

New in InterSystems IRIS 2019.1

### 11.6 Analytics Enhancements

This release contains the following analytics enhancements:

- Partial Date type in Business Intelligence — Partial dates allow you to specify incomplete dates, such as just a year or a year and a month. For more information, see Partial Dates in Defining Models for InterSystems IRIS Business
Intelligence.

- %SQLRESTRICT dimension for cubes — This new cube dimension allows run-time restrictions on an MDX query via a SQL SELECT statement or WHERE clause. For more information, see %FILTER Clause in the InterSystems MDX
Reference.

- Pivot Table Headers — When a large pivot table requires scrolling to see all columns and/or rows, the header columns and rows remain in place so that the labels continue to be visible as you scroll.

- Work Queue Manager replaces Agents — The Work Queue Manager is used in InterSystems IRIS Business Intelligence to distribute work to multiple concurrent processes in order to manage performance. The Work Queue Manager is a standard component of InterSystems IRIS. For more information on the Work Queue Manager, see Using the Work
Queue Manager.

### 11.7 Interoperability Enhancements

This release contains new interoperability capabilities that speed configuring and troubleshooting of productions. These
include the following:

- Interface Maps — Users can search for and view all the routes that a message can take within a production.

- Search for Interface References — Users can search to find where production components are referenced by other production components.

- Data Transformation Testing Enhancements — When testing data transformations, users can unit test record maps in the Data Transformation Editor by allowing raw text input in the Test Transform dialog and can enter values for aux, context, and process system objects as if the data transformation was invoked with these objects instantiated.

- DTL Editor Enhancements — The usability of the Data Transformation Editor has been enhanced with the addition of switch/case actions, the ability to group actions together, the ability to collapse/expand groups, and the ability to add comments to the data transformation.

- Unit Testing of Routing Rules — This enhancement introduces a unit testing capability to the Rule Editor, whereby a user can feed a message through a business rule and view rule execution results without having to run the message through the entire production.

- Download Multiple Messages to Local Computer — Users can select multiple messages in the Message Viewer and download them to their local computer.

- Download Event Logs to Local Computer — Users can download event logs to their local computer. Previously event logs could only be downloaded to the server.

- Rule Editor Enhancements — The usability of the Rule Editor has been enhanced with the ability to add comments to a business rule and the ability to view and edit a Data Transformation (DTL) directly from the Rule Editor when the given DTL is used in a business rule.

- Queue Wait Alert Modification — The Queue Wait Alert setting now specifies the length of time that a message can wait in the business host’s queue or be the active message before an alert is triggered. Previously, the setting only applied to messages in the queue, not the active message.

- Restrict Access to System Default Settings — Administrators can control whether users can create, edit, or delete system default settings.

- Export Productions to Local Computer — Users can export productions to their local computer. Previously productions could only be exported to the server.

- Deploy Productions from Local Computer — Users can deploy productions from their local computer. Previously productions could only be deployed from the server.

- Enhanced Navigation from Production Configur ation Page — Links have been added to the tabs of the Production Configuration windo w to quickly open related items in a separate window. On the Queue tab, clicking the message ID opens a window to display the visual trace for the message. On the Messages tab, clicking the Session ID opens a window to display the visual trace of the message. On the Jobs tab, clicking the message ID opens a window to display the visual trace for the message, and clicking the Job ID opens a window to display the Process Details for the job.

- Business Host Wizard Enhancements — To enhance user productivity, additional options have been added to the wizards used to create business hosts. Users can use the business host wizards to automatically assign system default values when fields are left blank and to define a package prefix for auto-generated routing rules.

### 11.8 System Performance and Capabilities

This release contains the following system security, performance, and efficienc y enhancements:

- Substantial scalability and performance improvements, particularly for large-scale Non-Uniform Memory Access (NUMA) systems. This includes changes to improve scalability in statistics tracking and global buffer management, performance improvements in use of subscript level mapping, and more effective optimizations to avoid traversing global pointer blocks. To enable these improvements there are minor changes to memory utilization and system statistics described in the Incompatibility History document.

- These enhancements increase the amount of memory allocated for global buffer metadata by 64 bytes per buffer on Intel systems and by 128 bytes per buffer on IBM Power systems. For example, with 8K buffer sizes, the shared memory allocated for a global buffer increases by 0.75% on Intel systems and by 1.5% on IBM Power systems. These enhancements also cause minor changes is in statistics displayed by utilities and the Management Portal.

- Key Management Interoperability Protocol (KMIP) — In this release, InterSystems IRIS® can be a client to an enterprise key management server and use the Key Management Interoperability Protocol (KMIP) to store and retrieve keys on the server. KMIP, an OASIS standard, gives you the power of centralized key management. You can use keys from a KMIP server to encrypt data at rest — for both database encryption and data-element encryption. They are available for all the same activities as keys from key files, such as journal file encryption. InterSystems IRIS also allows you to copy keys from the KMIP server to local files, so that there can be local backup copies. F or more information, see Managing Keys with the Key Management Interoperability Protocol (KMIP) in the Encryption Guide.

- Note:

- InterSystems IRIS does not support KMIP on the macOS platform.

DataMove — Enables you to move data from one database to another, revise the mappings to access the data, and delete the data from its old location.

Support for large JSON strings.

IRIS Studio support for other InterSystems products.

New in InterSystems IRIS 2019.1

- Support for Microsoft Integrated Windows Authentication for HTTP Connections (SPNEGO) — This new enhancement allows %Net.HttpRequest to use windows based authentication over HTTP 1.1 to establish a connection to a secure server. Users can provide credentials or, if no credentials are provided, the system will try to authenticate using the current logged in context. Client may initiate a connection to the server with an "Authorization" header or try to establish a connection without that header and process the 401 status code with its associated with WWW-Authenticate header and then respond with the appropriate authentication mechanism. The supported authentication schemes are Negotiate (Kerberos & NTLM), NTLM, and Basic. For more information see Providing Authentication in Using
Internet Utilities.

- Journaling efficiency impr ovements.

- Async I/O efficiency impr ovements.

### 11.9 New Features in 2019.1.1 Release

This section describes new features that are only available in the InterSystems IRIS 2019.1.1 maintenance release and later maintenance releases. If you are running release 2019.1.0, you do not have these features.

#### 11.9.1 In-Place Conversion from Caché and Ensemble

This release of InterSystems IRIS allows you to convert an existing instance of Caché or Ensemble to InterSystems IRIS. The conversion process may require some changes to application code, configuration scripts, and other procedures, b ut will be relatively easy for the majority of cases. As with any major upgrade, you should thoroughly test your custom code, including any production business services, processes, and operations, in a test environment before deploying to a live production environment.

Before performing an in-place conversion, it is important that you read the IRIS In-Place Conversion Guide and the Inter- Systems IRIS Adoption Guide for background information on the differences between Caché or Ensemble and InterSystems IRIS. You can download these documents from the InterSystems Worldwide Response Center documents distribution page.

Important:

InterSystems IRIS does not support the HL7 and DICOM features and the X12 health schemas that are available in Ensemble. This support is included in the HealthShare Health Connect and InterSystems IRIS for Health products. Consequently, if your Ensemble productions use HL7, DICOM, or the X12 health schemas, you should not perform an in-place conversion to InterSystems IRIS. If you are using Ensemble as an integration engine, you should first upgrade to HealthShare Health Connect 15.03x b uilt on the Caché/Ensemble platform and then perform an in-place conversion to Health Connect 2019.1 on the InterSystems IRIS platform. If you are using Ensemble as a general-purpose data platform for health care, you should wait for the release of InterSystems IRIS for Health that supports in-place conversion. In order to ensure that the in-place conversion is relatively easy, InterSystems performs significant testing, including test conversions at customer sites. We are deferring support of in-place conversion to InterSystems IRIS for Health until after we have completed this testing.

#### 11.9.2 InterSystems API Manager

This release includes the InterSystems API Manager (IAM) enabling you to monitor and control traffic to and from your web-based APIs.

If you are building service-oriented application layers, you are very likely to find the number of APIs you are using quickly rise. The more distributed your environment the more critical it becomes to properly govern and monitor your API traffic. The API Manager enables you easily route all your traffic through a centralized g ateway and forward API request to
appropriate target nodes. This enables you to:

New Features in 2019.1.1 Release

- Monitor all your API traffic in a central spot.

- Plan, document, and update the list of APIs you are using and the servers that provide them.

- Identify issues before they become critical.

- Control API traffic by throttling throughput, configuring allo wed payload sizes, whitelist and blacklist IP addresses and domains, and quickly taking an endpoint into maintenance mode.

- Onboard internal and external developers by providing interactive API documentation through a dedicated and customizable developer portal.

- Secure your API's in a central place.

The API Manager is interoperable, reliant, intuitive, and scalable. You can perform all configuration using a simple webbased user interface, but can also configure the API Manager using API calls, which makes it easy to perform remote deployments,

The API Manager is released in its own container. You can configure the API Manager as a cluster of multiple nodes, but even a single node can handle the load of multiple tens of thousands of requests per second.

For more information, see InterSystems API Manager.

Note:

The API Manager is only available in a Docker container distribution. You can use it with an InterSystems IRIS system that is installed on any of the InterSystems IRIS Supported Platforms, including UNIX, Windows, the cloud platforms, and the Docker container.

#### 11.9.3 X12 Element Validation in Interoperability Productions

This release provides enhanced X12 validation. In previous releases, you could only validate that the required segments are in the correct order and that there are no segments present that are prohibited, but there was no mechanism to validate
the contents of the segment. This enhancements enables you to validate that:

- Required fields are present and that all fields are allo wed by the schema.

- Number of fields within a se gment and how they are repeated are allowed by the schema.

- Datatypes for fields and components are correct.

- Field values conform to the code tables specified.

- Field and components conform to length restrictions.

For details, see Validation in Routing X12 Documents in Productions.

Known Issues and Notes

This topic describes known issues in InterSystems IRIS® 2024.3.

This topic lists features deprecated features in InterSystems IRIS®; it also lists any features that are discontinued or removed.

### 13.1 About Deprecated and Discontinued Technologies and Features

From time to time, InterSystems stops further development of a technology when newer and better options are available. However, product support for these capabilities continues in the same way that it does for products beyond our Minimum
Supported Version.

Deprecated designates a feature or technology that InterSystems no longer actively develops and for which better options exist. Deprecated items should not be used for new development. The deprecated designation indicates that customers should plan to eliminate use of the feature or technology. InterSystems maintains the staff expertise to support deprecated product capabilities.

Discontinued designates a feature or technology that is no longer viable for use, even in existing applications. InterSystems
feels that continued use of such technology is a risk for our customers. The reasons for this include but are not limited to:

- Usage has declined to a small number of customers.

- The feature has become incompatible with current technologies or security practice.

- Incompatibilities between the feature or technology and our current product implementation make application maintenance prohibitive.

- The feature or technology depends on discontinued content from a third party.

### 13.2 InterSystems Cloud Manager

As of version 2025.3, InterSystems Cloud Manager (ICM) has been removed and will not be supported in subsequent releases.

Customers in the cloud who are interested in deploying and managing an InterSystems IRIS deployment with many systems should use Kubernetes and the InterSystems Kubernetes Operator, which has similar functionality to ICM.

### 13.3 MultiValue

As of version 2025.1, MultiValue is deprecated. InterSystems will continue to support existing customers using the technology, but it is not recommended for new applications. Support will continue to be available from the Worldwide Response Center on the same “best effort” basis as is provided for releases older than Minimum Supported Versions.

While there are no immediate plans to remove MultiValue from our products, InterSystems reserves the right to remove the feature at a future date. If you have questions about your current or planned use of MultiValue, please reach out to your account team.

### 13.4 System Alerting and Monitoring

System Alerting and Monitoring (SAM) is discontinued. As of December 4, 2024, it is no longer available for download.

### 13.5 Studio

Important:

Starting with this 2024.2 release, Windows kits no longer contain Studio. This means that new installations of this kit will not install Studio, and upgrading an existing instance to the version of this kit will remove Studio from the instance’s bin directory.

Developers who wish to keep using Studio will need to download the 2024.1 Studio component from the WRC component download page independently. Studio version 2024.1 is forward compatible, so it can connect to future versions, including this release.

InterSystems recommends Visual Studio (VS) Code with the InterSystems ObjectScript Extension Pack, which provides a fully-featured integrated development environment for InterSystems applications. The InterSystems ObjectScript Expansion Pack includes the following extensions: InterSystems ObjectScript, InterSystems Language Server, and Server Manager extensions. See the documentation for the InterSystems VS Code extensions for information on migrating from IRIS Studio to VS Code.

### 13.6 Public Key Infrastructure

As of version 2024.1, InterSystems Public Key Infrastructure (PKI) is deprecated. It may be removed from future versions of InterSystems products. InterSystems urges users to discontinue use of the PKI features.

### 13.7 InterSystems IRIS Natural Language Processing

As of version 2023.3, InterSystems IRIS NLP, also known as iKnow, has been deprecated. All existing functionality continues to be available as part of InterSystems IRIS and InterSystems will continue to support existing customer deployments. However, InterSystems is no longer actively developing the capability and does not recommend starting new development projects with the technology. The open-source version of the core engine, packages as a Python module, can be used inde-

Private Web Server (PWS)

pendently of InterSystems IRIS and will continue to be available. Customers looking for guidance on their current use of the technology are invited to reach out to their account teams.

InterSystems IRIS SQL Search, also known as iFind, is only partly affected. Only the Semantic and Analytic index types make use of the iKnow engine and therefore are deprecated. All other functionality and index types are not affected by this and continue to be the recommended choice for applications requiring a fle xible and high-performance full text search capability.

### 13.8 Private Web Server (PWS)

As of version 2023.2, local installations of InterSystems IRIS will no longer install the private web server and InterSystems IRIS containers will no longer provide the private web server.

InterSystems strongly recommends that you install an external web server and configure it according to your needs, instead of using the private web server. Note that this is not a change in existing InterSystems recommendations and there is no change in the list of supported web servers.

Effective with the first EM release in 2026, the pri vate web server will be discontinued; at that point, upgrades of existing
InterSystems IRIS instances will remove the private web server.

For more details on this change, see the Private Web Server (PWS) topic in the 2023.2 new features listing.

### 13.9 Unstructured Information Management Architecture (UIMA) Integration

As of version 2023.1, the capability to implement the Unstructured Information Management Architecture (UIMA) has been deprecated. UIMA integration capability is still included in this release, but it will be removed in a future release.

As of version 2023.1, JAR files required to implement UIMA ha ve been removed from releases. To obtain these files, see Build Updated Apache UIMA JAR files .

### 13.10 Spark Connector

As of version 2022.1, the Spark connector has been deprecated. As of version 2022.3, it has been discontinued. As of version 2023.1, it has been removed from releases.

Spark now has a built-in JDBC connector. If you use the Spark connector, you should modify your code to use the Spark JDBC connector.

### 13.11 Atelier

As of version 2021.1, Atelier has been deprecated.

InterSystems recommends Visual Studio (VS) Code with the InterSystems ObjectScript Extension Pack, which provides a fully-featured integrated development environment for InterSystems applications. The InterSystems ObjectScript Extension

Pack includes the following extensions: InterSystems ObjectScript, InterSystems Language Server, and Server Manager extensions. See the documentation for the InterSystems VS Code extensions for information on migrating from IRIS Studio to VS Code.

### 13.12 Shadowing

As of version 2019.1, shadowing has been discontinued. Applications using shadowing should migrate to the corresponding capabilities available with mirroring, as described in the High Availability Guide.

### 13.13 Zen

As of version 2019.1, Zen has been deprecated. It is still included with this release, but it will be removed from a future release.

### 13.14 Zen Reports

As of version 2019.1, Zen Reports has been deprecated. It is still included with this release, but it will be removed from a future release.
