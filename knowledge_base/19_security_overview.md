# Security Overview

We take security seriously and implement multiple layers of protection for your data and access.

## Infrastructure Security

- All data is hosted on **AWS** in `us-east-1` and `eu-west-1` regions
- Data is encrypted at rest using **AES-256**
- All data in transit is encrypted with **TLS 1.3**
- Regular third-party penetration tests (annual)

## Application Security

- Passwords are hashed with **bcrypt** (cost factor 12) — never stored in plaintext
- API keys are stored as **SHA-256 hashes** — we cannot recover your key if lost
- All inputs are sanitised to prevent SQL injection and XSS attacks
- Rate limiting applied to all endpoints to prevent abuse

## Access Control

- **Role-Based Access Control (RBAC)** — users only access what they're allowed
- Admin actions require **re-authentication** every session
- All admin actions are logged to the audit log

## Incident Response

In the event of a security incident:
1. We contain and investigate immediately
2. Affected users are notified within **72 hours** (GDPR requirement)
3. A full post-incident report is published within 30 days

## Responsible Disclosure

Found a security vulnerability? We operate a responsible disclosure program:
- Email: security@example.com
- PGP key available at `https://example.com/.well-known/security.txt`
- We respond within **48 hours** and do not pursue legal action for good-faith reports

## Certifications & Compliance

| Standard | Status |
|---------|--------|
| SOC 2 Type II | ✅ Certified |
| ISO 27001 | ✅ Certified |
| GDPR | ✅ Compliant |
| PCI DSS Level 1 | ✅ Compliant |
| HIPAA | ❌ Not applicable |

## Security Checklist for Users

- Enable 2FA on your account
- Use unique, strong passwords
- Rotate API keys every 90 days
- Restrict API keys to specific IP addresses
- Review your audit log monthly
