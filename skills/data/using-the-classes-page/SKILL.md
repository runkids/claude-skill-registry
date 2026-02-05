# Using the Classes Page

This page describes how to use the Management Portal tools for viewing and managing classes.

## 1 Introduction to the Classes Page

The Management Portal includes the Classes page, which allows you to manage classes. On this page, you can:

- Select Documentation in the row for a class to display documentation for that class in the right pane.

- Select Compile to compile classes.

- Select Export to export classes.

- Select Import to import classes.

- Select Delete to delete classes.

- Select Routines to view routines.

- Select Globals to view globals.

To access this page from the Management Portal home page:

1. Select System Explorer > Classes.

2. Select the namespace or database of interest:

- In the left pane, select either Namespaces or Databases from the Lookin list.

- Select the desired namespace or database from the second drop-down list.

Selecting a namespace or database updates the page to display its classes.

3.

If you are looking for a particular class and do not initially see its name:

- Optionally select System items, Generated items, or Mapped items to include classes of the selected type in the search.

- Optionally specify a search mask. To do so, enter a value into the Class name field. If you end the string with an asterisk “*”, the asterisk is treated as a wildcard, and the page displays each class whose name begins with the string before the asterisk.

- After entering a value, press Enter.

- Optionally specify a Begin date and an End date to specify the range of dates to search on. The Date column specifies when the class w as last modified.

- Optionally enter a value for Maximum Rows, which determines the maximum number of rows to return.

In the center pane, optionally enter a value for Page size, which controls the number of classes to list on any page.

To display SQL table names, select the SQL table name check box. This includes the link View SQL related globals in the rows for any classes that have projections to SQL tables.

Compiling Classes

## 2 Compiling Classes

The Compile Classes wizard provides several options for compiling classes.

To access and use this wizard:

1. Display the Classes page.

2. Specify the classes to compile. To do so, see steps 2 and 3 in Introduction to the Classes Page. Select their check boxes.

3. Click the Compile button, which displays the Compile Classes wizard.

4.

In the Compile Classes wizard, specify the Compiler Flags that you would like to use by selecting the corresponding check box, or by entering them manually under Flags. By default, Flags is set to cuk.

5. Select the Run compile in the background check box if you are compiling many or large files.

6. Click the Compile button. The Compile Classes wizard will display information regarding the status of the compilation.

7. To dismiss the wizard, click Done.

## 3 Exporting Classes

The Export Classes wizard enables you to export classes.

To access and use this wizard:

1. Display the Classes page.

2. Specify the classes to work with. To do so, see steps 2 and 3 in Introduction to the Classes Page. Select their check

boxes.

3. Click the Export button to display the Export Classes wizard.

4.

In the Export Classes wizard, specify the file into which you wish to e xport the classes. To do this, either enter a file name (including its absolute or relative pathname) in the Enter the path and name of the export file field or click Browse and navigate to the file.

5. Select the export file’ s character set with the Character set list.

6. Select the Run export in the background... check box if you are exporting many or large files.

7. Click Export.

8.

If the file already e xists, select OK to overwrite it with a new version.

9. To dismiss the wizard, click Done.

## 4 Importing Classes

The Import Classes wizard enables you to import classes.

To access and use this page:

1. Display the Classes page.

Deleting Classes

2. Click the Import button to display the Import Classes wizard.

3.

In the Import Classes wizard, choose to import from a file or a directory by selecting the corresponding radio b utton under Import from a File or a Directory.

4. Specify the import file or directory . To do this, either enter a file or directory (including its absolute or relati ve pathname)

in the Enter the path and name of the import file field or click Browse and navigate to the file or directory .

5.

If importing from a directory, select or clear Include subdirectories.

6. Select or clear Compile imported items, and enter any Compile Flags.

7. Select Run import in the background if importing large files.

8. Click Import. The Import Classes wizard will display information regarding the status of the import.

9. To dismiss the wizard, click Done.

Note:

This page enables you to import classes that have been exported in XML format. It does not support older formats.

## 5 Deleting Classes

CAUTION: A deleted class cannot be restored. There is no undo option.

The Classes page enables you to delete classes. To access and use this page:

1. Display the Classes page.

2. Select the classes to work with. To do so, see steps 2 and 3 in Introduction to the Classes Page. Select their check

boxes.

3. Click the Delete button.

4. Click OK to confirm this action.
