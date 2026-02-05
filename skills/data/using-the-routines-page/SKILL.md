# Using the Routines Page

The Management Portal provides tools for managing routines. This page describes how to use these tools. See Routine Syntax for more information about routines.

## 1 Introduction to the Routines Page

The Management Portal includes the Routines page (System Explorer > Routines), which allows you to manage routines.
On this page, you can:

- Select Code in the row for a routine to display code for that routine in the right pane.

- Select Compile to compile routines.

- Select Export to export routines.

- Select Import to import routines.

- Select Find to find substrings in routines.

- Select Replace to replace a substring in routines.

- Select Delete to delete routines.

- Select Compare to compare two routines.

- Select Classes to view classes.

- Select Globals to view globals.

To find specific routines:

1. Select the namespace or database of interest:

- In the left pane, select either Namespaces or Databases from the Look in list.

- Select the desired namespace or database from the second drop-down list.

Selecting a namespace or database updates the page to display its routines.

2.

If you are looking for a particular routine and do not initially see its name, try specifying the following options:

- System items, Generated items, or Mapped items to include routines of the selected type in the search.

- Begin date and End date to specify the range of dates to search on. The Date column specifies when the routine was last modified.

- Routine and Include files to specify a search mask. If you end the string with an asterisk “*”, the asterisk is treated as a wildcard, and the page displays each routine whose name begins with the string before the asterisk. After entering a value, press Enter.

- You can also use the default masks, listed below the Routines and Include files field, by clicking on them.

- Maximum Rows, which determines the maximum number of rows to return.

Page size, located on the center pane of the page, which controls the number of routines to list on any page.

Compiling Routines

## 2 Compiling Routines

The Compile Routines wizard provides several options for compiling routines. To use this wizard on the Routines page:

1. Specify the routines to compile by selecting their check boxes. Introduction to the Routines Page describes the available

search tools.

2. Click the Compile button, which displays the Compile Routines wizard.

3. Select the Run compile in the background check box if you are compiling many or large files.

4. Click the Compile button. The Compile Routines wizard will display information regarding the status of the compilation.

5. To dismiss the wizard, click Done.

## 3 Exporting Routines

The Export Routines wizard enables you to export routines. To use this wizard on the Routines page:

1. Specify the routines to work with by selecting their check boxes. Introduction to the Routines Page describes the

available search tools.

2. Click the Export button to display the Export Routines wizard.

3.

In the Export Routines wizard, choose to export to a file on the serv er or the default browser by selecting the corresponding radio button under the Export the file to the label.

4. Specify the file into which you wish to e xport the routines. To do this, either enter a file name (including its absolute

or relative pathname, if exporting to the server) in the Enter the path and name of the export file field, or click Browse and navigate to the file.

5. Select the export file’ s character set with the Character set list.

6. Select Check here for exporting OBJ code in XML format to export the routines in XML format.

7. Select the Run export in the background check box if you are exporting many or large files to the serv er.

8. Click Export.

9.

If the file already e xists, select OK to overwrite it with a new version.

10. To dismiss the wizard, click Done.

## 4 Importing Routines

The Import Routines wizard enables you to import routines. To use this wizard on the Routines page:

1. Click the Import button to display the Import Routines wizard.

2. Specify the import file. To do this, either enter a file (including its absolute or relati ve pathname) in the Enter the path

and name of the import file field or click Browse and navigate to the file or directory .

3. Select or clear Compile imported items, and enter any Compile Flags.

4. Select Run import in the background if importing large files.

5. Click Import. The Import Routines wizard will display information regarding the status of the import.

6. To dismiss the wizard, click Done.

Note:

This page enables you to import routines that have been exported in XML format. It does not support older formats.

Finding Substrings in Routines

## 5 Finding Substrings in Routines

The Find Routine String page enables you to find a gi ven string in selected routines. To use this page:

1. Specify the routines to work with on the Routines page by selecting their check boxes. Introduction to the Routines

Page describes the available search tools.

2. Click the Find button.

3. For Find What, enter the string to search for.

4. Optionally clear Match Case. By default, the search is case-sensitive.

5. Click either Find First or Find All. The page then displays either the first line or all lines that contain the gi ven string,
within the selected routines. The table shows the line number on the left and the contents of the line on the right.

6.

If you used Find First, click Find Next to see the next line, as needed.

7. When you are done, click Close Window.

### 5.1 Performing Wholesale Replacements

CAUTION:

Before making any edits, be sure that you know which routines InterSystems IRIS uses and which routines your application uses. This option changes the data permanently. It is not recommended for use in production systems.

For development purposes, the Find Routine String page also provides an option to make wholesale changes to routines.
To use this option on the Routines page:

1. Specify the routines to work with by selecting their check boxes. Introduction to the Routines Page describes the

available search tools.

2. Click the Replace button.

3. Use this page to find v alues, as described in Finding Substrings in Routines.

4. Specify a value for Replace With.

5. Click Replace All.

6. Click OK to confirm this action. The page then displays a preview of the change.

7. Review the results. If they are acceptable, click Save; otherwise, click Undo Replace All.

8. Click OK to confirm this action.

Deleting Routines

## 6 Deleting Routines

CAUTION: A deleted Routine cannot be restored. There is no undo option.

The Routines page enables you to delete routines. To delete a routine:

1. Specify the routines to work with by selecting their check boxes. The Introduction to the Routines Page section describes

the available search tools.

2. Click the Delete button.

3. Click OK to confirm this action.

## 7 Comparing Routines

The Routine Compare page enables you to compare two selected routines. To use this utility on the Routines page:

1. Specify the routines to work with by selecting their check boxes. Introduction to the Routines Page describes the

available search tools.

2. Click the Compare button to display the Routine Compare page.

3. On the Routine Compare page, you can specify routines to compare. If you did not select two routines in step 2, you

can specify routines in the Routine 1 and Routine 2 fields.

4. Click Compare. The Differences between these two routines table appears, which displays the line-by-line differences

between the two selected routines.
