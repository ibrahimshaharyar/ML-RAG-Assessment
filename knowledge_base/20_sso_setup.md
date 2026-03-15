# SSO Setup (Single Sign-On)

Single Sign-On (SSO) is available on the **Enterprise plan**. It allows your team to log in using your existing Identity Provider (IdP).

## Supported SSO Protocols

- **SAML 2.0** (Okta, Azure AD, Google Workspace, PingIdentity)
- **OIDC / OAuth 2.0** (Google, Microsoft, Auth0)

## Configuring SAML 2.0 SSO

### Step 1: Get Our Service Provider Details

In **Settings → Security → SSO**:
- **ACS URL (Assertion Consumer Service)**: `https://auth.example.com/saml/acs`
- **Entity ID**: `https://auth.example.com/saml/entity`
- **Metadata URL**: `https://auth.example.com/saml/metadata`

### Step 2: Configure Your Identity Provider

Add our app in your IdP (e.g., Okta) with the above ACS URL and Entity ID.

Map these attributes:
| IdP Attribute | Our Field |
|--------------|-----------|
| `email` | Email address |
| `firstName` | First name |
| `lastName` | Last name |
| `groups` | Team roles (optional) |

### Step 3: Enter IdP Details in Our Dashboard

1. Go to **Settings → Security → SSO**
2. Paste your IdP **Metadata XML** or enter the fields manually:
   - SSO URL
   - Certificate (X.509)
3. Click **"Test SSO"** to verify
4. Click **"Enable SSO"**

## JIT Provisioning

When SSO is enabled, users who authenticate via your IdP are **automatically created** in your team (Just-In-Time provisioning). No need to manually invite each user.

## Enforcing SSO

To require all team members to use SSO (disable email/password login):
1. Settings → Security → SSO → **"Enforce SSO"**
2. Confirm — users without SSO access will be locked out

> ⚠️ Always test SSO thoroughly before enforcing it to avoid lockout.

## SSO Troubleshooting

| Error | Likely Cause |
|-------|-------------|
| `Invalid signature` | Certificate mismatch |
| `ACS URL mismatch` | Wrong ACS configured in IdP |
| `User not provisioned` | Email domain not whitelisted |

Contact support@example.com for SSO setup assistance.
