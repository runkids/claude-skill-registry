---
name: contacts
description: Get contact information from macOS.  Use when texting, calling, emailing or social networking with people and companies.
compatibility: Designed for macOS.  Requires osascript.
---

# Contacts

## Find by Name

```bash
./scripts/find.sh Alice
./scripts/find.sh "John Smith"
```

Find contact by name.

## Find by Email Address

```bash
./scripts/find.sh -e alice@example.com
./scripts/find.sh -e "john@"
```

Find contact by email address.

## Find by Phone Number

```bash
./scripts/find.sh -p 555-1234
./scripts/find.sh -p "(555) 123"
```

Find contact by phone number.
