# Webhook Setup

Webhooks allow our platform to send real-time notifications to your server when events occur.

## Supported Events

| Event | Description |
|-------|-------------|
| `query.completed` | A query was processed successfully |
| `query.failed` | A query failed or timed out |
| `billing.payment_success` | A payment was processed |
| `billing.payment_failed` | A payment failed |
| `user.created` | A new team member joined |
| `user.deleted` | A team member was removed |

## Creating a Webhook

1. Go to **Settings → Webhooks**
2. Click **"Add Webhook"**
3. Enter your endpoint URL (must be publicly accessible HTTPS)
4. Select the events you want to subscribe to
5. Click **"Save"** — a secret key is generated

## Webhook Payload

All webhook payloads follow this format:

```json
{
  "event": "query.completed",
  "timestamp": "2024-10-01T12:00:00Z",
  "data": {
    "query_id": "abc123",
    "question": "How do I reset my password?",
    "answer": "To reset your password...",
    "latency_ms": 840
  }
}
```

## Verifying Webhook Signatures

We sign every request with an HMAC-SHA256 signature. Verify it to ensure the request is from us:

```python
import hmac
import hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

The signature is sent in the `X-Webhook-Signature` header.

## Retry Policy

If your endpoint returns a non-2xx response, we retry:
- After 5 minutes
- After 30 minutes
- After 2 hours
- After 24 hours

After 4 failed attempts, the webhook delivery is marked as failed.

## Testing Webhooks

Use **"Send Test Event"** in the Webhooks settings page to send a sample payload to your endpoint.
