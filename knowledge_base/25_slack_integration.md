# Slack Integration

Connect our platform to Slack so your team can ask questions and receive answers without leaving Slack.

## Setting Up the Slack Integration

1. Go to **Settings → Integrations → Slack**
2. Click **"Connect to Slack"**
3. Select the Slack workspace to connect
4. Authorise the required permissions
5. Choose the default Slack channel for notifications

## Using the Slack Bot

Once connected, invite the bot to any channel:

```
/invite @ExampleBot
```

Then ask questions directly:

```
@ExampleBot How do I reset my password?
```

The bot will reply in the thread with the answer and source documents.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/ask [question]` | Submit a query to the knowledge base |
| `/ask-status` | Check the bot's connection status |
| `/ask-help` | Show available commands |

## Notification Alerts via Slack

You can route webhook events to Slack channels:
1. Settings → Integrations → Slack → **Alert Rules**
2. Map event types (e.g., `billing.payment_failed`) to specific channels

Example: Route payment failures to `#billing-alerts`, API errors to `#dev-alerts`.

## Disconnecting Slack

1. Settings → Integrations → Slack → **Disconnect**
2. The bot is removed from all channels automatically

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Bot not responding | Re-invite with `/invite @ExampleBot` |
| Wrong channel responses | Check default channel in Settings |
| Auth error | Disconnect and reconnect the integration |
