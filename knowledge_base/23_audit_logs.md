# Audit Logs

Audit logs provide a complete record of activity within your account for security and compliance purposes.

## What Is Logged

| Event Category | Examples |
|---------------|---------|
| Authentication | Logins, logouts, failed attempts, 2FA changes |
| API Keys | Created, deleted, rotated |
| Team | Member invited, removed, role changed |
| Settings | SSO configured, webhooks added, billing updated |
| Queries | Who submitted what query and when |
| Data | Exports requested and downloaded |

## Accessing Audit Logs

**Available to: Owners and Admins only**

1. Go to **Settings → Audit Logs**
2. Use filters to narrow results:
   - **Date range**
   - **Event type**
   - **User** (filter by specific team member)
3. Each log entry shows:
   - Timestamp (UTC)
   - Actor (who performed the action)
   - Event type
   - Details (IP address, affected resource)
   - Status (success / failure)

## Exporting Audit Logs

1. Settings → Audit Logs → **"Export"**
2. Select date range and format (JSON or CSV)
3. Download the file

## Log Retention

| Plan | Retention Period |
|------|-----------------|
| Free | 7 days |
| Starter | 30 days |
| Pro | 1 year |
| Enterprise | Custom (up to 7 years) |

## Compliance Use Cases

- **SOC 2 audits**: Export logs for the audit period
- **GDPR**: Demonstrate data access controls
- **Internal security reviews**: Investigate suspicious activity
- **Employee offboarding**: Verify access was revoked properly

## Alerting on Suspicious Activity

Enterprise plan users can configure alerts for specific events:
- Multiple failed login attempts
- API key deletion
- Admin role assignment
- Unusual query volume

Go to **Settings → Audit Logs → Alert Rules** to configure.
