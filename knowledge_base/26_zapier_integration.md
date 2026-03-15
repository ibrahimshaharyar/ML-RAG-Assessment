# Zapier Integration

Connect our platform to 5,000+ apps using Zapier — no code required.

## Setting Up Zapier

1. Go to [zapier.com](https://zapier.com) and create an account
2. Search for **"Example App"** in the Zapier app directory
3. Connect your account using your API key
4. Build Zaps (automated workflows) using our triggers and actions

## Available Triggers (Events That Start a Zap)

| Trigger | Description |
|---------|------------|
| New Query Completed | Fires when a query is answered |
| Payment Received | Fires on successful billing |
| New Team Member | Fires when a user joins |

## Available Actions (Things Zapier Can Do)

| Action | Description |
|--------|------------|
| Submit Query | Send a question to the knowledge base |
| Create Team Invite | Invite a new user to your team |

## Example Zaps

### Example 1: Log All Queries to Google Sheets
- **Trigger**: New Query Completed
- **Action**: Create Row in Google Sheets
- Columns: Question, Answer, Timestamp, Latency

### Example 2: Send Slack Message on Failed Payment
- **Trigger**: Payment Failed
- **Action**: Send Slack Message to `#billing-alerts`

### Example 3: Query Knowledge Base from Typeform
- **Trigger**: New Typeform Submission (question field)
- **Action**: Submit Query → get answer
- **Action**: Send Email reply to submitter with the answer

## Authentication

In Zapier, when connecting Example App:
1. Select **"API Key"** authentication
2. Paste your API key from **Settings → API Keys**
3. Zapier will verify the connection

## Rate Limits in Zapier

Zapier Zaps respect your plan's API rate limits. If you hit limits, Zapier will queue and retry actions.
