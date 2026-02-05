# Installing Code from the WRC

Execution of certain InterSystems upgrade tools requires that the most recent code be installed. Although the most recent version of the code is generally included in the latest installation kit, if you are upgrading from or to an older version, the code included in your installation may not be the most recent code available.

1. Go to the WRC Distribution page under Components and search for the name of the tool you wish to use.

2. Determine whether the code included in your installation is up to date, as follows:

a. The upgrade tool code version will match the version of your InterSystems IRIS, IRIS for Health, or HealthConnect

installation. You can find this v ersion number by clicking About in the management portal. Look in the Version row of the System Overview table. The version number has three segments. For example, 2025.1.2. The first two segments are the main release number, and the third section is the maintenance release number.

b. Compare the main release number (the first tw o segments) to the value in the Version column of the InterSystems

Components table in the WRC.

c.

If the two version numbers are the same, compare the third segment (the maintenance release number) of the value from the management portal to the value in the Maint column in the WRC table.

d. The higher number is the more recent version. For example, if the version in the management portal is 2025.1.1

and the WRC values are Version: 2025.1 and Maint: 3, the WRC code is more recent.

Note:

If the version in the management portal matches or is higher than the version in the WRC, you already have the most recent code, and you can skip the download and installation procedures described in this article. Otherwise, proceed with downloading and installation.

3. Download and unzip the ZIP file. Mak e a note of the name of the extracted file and the path to where you sa ve it.

Execute the remaining steps for all relevant systems. For example, for the Production Validator, execute the steps for the source system and the target system.

4. Log in to the IRIS terminal associated with the relevant system, and set the namespace to HSLIB.

Set $namespace="HSLIB"

5. Write enable the HSLIB database to prepare for loading the code.

write ##class(%ZHSLIB.HealthShareMgr).UpdateReadWrite("HSLIB",0)

6. Set a string variable to identify the filename and path to the code.

set file="<filepath>\<extracted_upgrade_tool_file>"

7. Load Production Validator code.

do $system.OBJ.Load(file,"ck")

8. Reset read/write permissions for the HSLIB database.

write ##class(%ZHSLIB.HealthShareMgr).UpdateReadWrite("HSLIB",1)
