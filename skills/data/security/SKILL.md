---
name: security
description: Apply security practices for the .NET 8 WPF widget host app: authN/authZ, secrets, encryption at rest, and secure local storage. Use when handling credentials, tokens, user data, or integrating identity providers.
---

# Security

## Overview

Protect user data and credentials across local storage, network calls, and widget interactions.

## Core areas

- Authentication and authorization
- Secrets management
- Encryption at rest
- Secure local storage

## Definition of done (DoD)

- No secrets in source code or config files
- Sensitive data uses Windows DPAPI or equivalent
- Authorization checks happen at service boundaries, not UI
- Logs and telemetry are reviewed for PII before merging
- Password/token inputs are masked in UI

## Guidance

- Do not store secrets in plain text or config files.
- Use OS-provided secure storage for tokens.
- Encrypt sensitive local data with per-user keys.
- Validate authorization in application services, not UI.

## Workflow

1. Identify data classified as sensitive.
2. Select storage location and encryption strategy.
3. Implement token handling and refresh flow.
4. Validate authorization checks at service boundaries.
5. Review logs and telemetry for PII leakage.

## References

- `references/auth.md` for authN/authZ patterns.
- `references/secrets.md` for secret storage rules.
- `references/encryption.md` for encryption at rest.
- `references/secure-storage.md` for Windows storage options.
