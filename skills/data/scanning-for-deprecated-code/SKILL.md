# Scanning for Deprecated Code

The class %SYSTEM.CodeScanner enables you to quickly find code that refers to deprecated classes and deprecated class members. This class provides two class queries, described here.

## 1 ScanDocuments Query

The ScanDocuments class query returns a result set that contains the following fields:

- Document identifies the class or routine that contains the reference. F or example:

- ResearchXForms.BasicDemo.cls

Location identifies the location of the reference, within the gi ven class or routine. For example:

ClassMethod CreateOne Implementation+4

- Message explains what is deprecated. For example:

Class '%Library.FileBinaryStream' is deprecated.

By default, the query scans only classes and routines in the default routine database for the current namespace, although you can pass a parameter to include mapped code. Also, the query ignores classes and routines that have names starting with %, as well as any classes that are marked as deprecated.

The query is projected to SQL as the %SYSTEM.ScanDocuments stored procedure.

## 2 ScanDocument Query

The ScanDocument class query takes one argument document, which is the name of a class, MAC routine, or INT routine. This argument includes the file e xtension, for example: MyPkg.MyClass.cls

This query returns a result set that contains the following fields:

- Location indicates the line number or class keyword describing where the deprecated reference is, within the given code item.

- Message string describing the deprecated reference.

## 3 Example

For example, you could write code as follows:

Scanning Mapped Code

Class Member

ClassMethod Check()
{
set stmt = ##class(%SQL.Statement).%New()
set status = stmt.%PrepareClassQuery("%SYSTEM.CodeScanner","ScanDocuments")
if $$$ISERR(status) {quit}
set rset = stmt.%Execute()
if rset.%SQLCODE<0 {quit}

while rset.%Next() {
set Document=rset.%Get("Document")
set Location=rset.%Get("Location")
set Message=rset.%Get("Message")
write !, Document_" "_Location_" "_Message
}
}

The following shows example output:

ResearchXForms.BasicDemo.cls Property BinStream Type Class '%Library.GlobalBinaryStream' is deprecated. ResearchXForms.BasicDemo.cls Property CharStream1 Type Class '%Library.GlobalCharacterStream' is deprecated. ResearchXForms.BasicDemo.cls Property CharStream2 Type Class '%Library.GlobalCharacterStream' is deprecated. ResearchXForms.BasicDemo.cls Property CharStream3 Type Class '%Library.GlobalCharacterStream' is deprecated. ResearchXForms.BasicDemo.cls ClassMethod CreateOne Implementation+4 Class '%Library.FileBinaryStream' is deprecated. ResearchXForms.BasicDemo.cls ClassMethod RoundTripBin Implementation+1 Class '%Library.FileBinaryStream' is deprecated.

## 4 Scanning Mapped Code

By default, the query scans only classes and routines in the default routine database for the current namespace. To include classes and routines from mapped databases, specify the query argument as 1, by passing that argument when executing
the class query. For example:

Class Member

ClassMethod Check()
{
set stmt = ##class(%SQL.Statement).%New()
set status = stmt.%PrepareClassQuery("%SYSTEM.CodeScanner","ScanDocuments")
if $$$ISERR(status) {quit}
set rset = stmt.%Execute(1)
if rset.%SQLCODE<0 {quit}

while rset.%Next() {
set Document=rset.%Get("Document")
set Location=rset.%Get("Location")
set Message=rset.%Get("Message")
write !, Document_" "_Location_" "_Message
}
}

## 5 See Also

- %SYSTEM.CodeScanner
