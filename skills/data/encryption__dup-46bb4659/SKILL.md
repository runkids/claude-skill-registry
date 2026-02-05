# Encryption

InterSystems IRIS includes a suite of encryption technologies that prevent unauthorized access to data at rest, which is data stored on disk or in the cloud. This suite of tools implements encryption using the AES (Advanced Encryption Standard)
algorithm. Its technologies include:

- Block-level database encryption — InterSystems IRIS performs database encryption and decryption when writing to and reading from disk. The encrypted content includes the data itself, indexes, bitmaps, pointers, allocation maps, and incremental backup maps.

- Data-element encryption for use in applications — Data-element encryption uses a simple and comprehensive set of methods that allow an application to encrypt and decrypt content as needed.

- Encryption key management — To support encryption operations, InterSystems IRIS provides tools for creating and managing data encryption keys. These keys can be stored either in key files or on k ey servers that use the key management interoperability protocol (KMIP).

As with every aspect of InterSystems IRIS, encryption and decryption are optimized for performance. Encryption has minimal impact on writes and a small, deterministic impact on reads.
