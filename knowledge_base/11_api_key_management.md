# API Key Management

API keys authenticate your application's requests to our platform. Treat them like passwords.

## Generating an API Key

1. Log in and go to **Settings → API Keys**
2. Click **"Generate New Key"**
3. Give the key a descriptive name (e.g., `production-app`, `dev-testing`)
4. Optionally restrict the key to specific IP addresses
5. Click **"Create"** — **copy the key now**, it is shown only once

## Using Your API Key

Include your key in every API request via the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
```

Example with curl:
```bash
curl -X POST https://api.example.com/v1/ask \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

## Key Permissions (Scopes)

When creating a key, you can limit it to specific scopes:

| Scope | Access |
|-------|--------|
| `read:all` | Read-only access to all resources |
| `write:queries` | Submit queries only |
| `admin:keys` | Manage API keys (use sparingly) |

## Rotating API Keys

We recommend rotating keys every **90 days**:
1. Generate a new key
2. Update your application to use the new key
3. Test the new key works
4. Delete the old key

## Revoking a Key

1. Settings → API Keys
2. Click the trash icon next to the key
3. Confirm deletion — this is **immediate and irreversible**

> ⚠️ Any application using the deleted key will stop working immediately.

## Security Best Practices

- **Never commit API keys to Git** — use `.env` files
- **Never share keys** in chat, email, or Slack
- Set IP restrictions where possible
- Use different keys for different environments (dev, staging, prod)
