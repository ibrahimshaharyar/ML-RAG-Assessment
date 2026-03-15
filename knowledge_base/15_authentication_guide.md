# Authentication Guide

This guide covers all authentication mechanisms supported by our API.

## API Key Authentication (Recommended)

The simplest method. Pass your API key in the `Authorization` header:

```http
POST /v1/ask HTTP/1.1
Host: api.example.com
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## OAuth 2.0

For user-level access or third-party integrations, use OAuth 2.0.

### Step 1: Redirect User to Authorization

```
GET https://auth.example.com/oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=read:queries write:queries
  &response_type=code
```

### Step 2: Exchange Code for Token

```bash
curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=https://yourapp.com/callback"
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def..."
}
```

### Step 3: Use the Access Token

```http
Authorization: Bearer ACCESS_TOKEN
```

## Token Expiry & Refresh

Access tokens expire after **1 hour**. Use the refresh token to get a new one:

```bash
curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=refresh_token" \
  -d "refresh_token=REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

## Session Authentication (Web UI Only)

The web dashboard uses session-based cookies. Sessions expire after **24 hours of inactivity**.

## Token Scopes

| Scope | Access Level |
|-------|-------------|
| `read:queries` | Submit and read queries |
| `write:queries` | Submit queries (no read history) |
| `read:billing` | View billing information |
| `admin:all` | Full admin access |
