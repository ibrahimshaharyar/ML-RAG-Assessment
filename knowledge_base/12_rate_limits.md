# Rate Limits

Rate limits protect the platform's stability and ensure fair usage for all users.

## Default Rate Limits by Plan

| Plan | Requests/day | Requests/minute | Concurrent Requests |
|------|-------------|-----------------|---------------------|
| Free | 100 | 5 | 1 |
| Starter | 10,000 | 60 | 5 |
| Pro | Unlimited | 300 | 20 |
| Enterprise | Unlimited | Custom | Custom |

## Rate Limit Response

When you exceed your limit, you receive a `429 Too Many Requests` response:

```json
{
  "error": "rate_limit_exceeded",
  "message": "You have exceeded your request limit. Retry after 60 seconds.",
  "retry_after": 60
}
```

## Rate Limit Headers

Every API response includes headers to help you track usage:

```http
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 247
X-RateLimit-Reset: 1710000000
```

- `X-RateLimit-Limit`: Your total limit for this window
- `X-RateLimit-Remaining`: Requests remaining in the current window
- `X-RateLimit-Reset`: Unix timestamp when the window resets

## Handling Rate Limits in Code

```python
import time
import requests

def make_request_with_retry(url, headers, payload, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            time.sleep(retry_after)
        else:
            return response
    raise Exception("Max retries exceeded")
```

## Increasing Your Limits

- **Upgrade your plan** to get higher limits automatically
- **Enterprise customers** can request custom limits via sales@example.com

## Daily Limit Reset

Daily limits reset at **midnight UTC**. Minute-level limits reset every 60 seconds.
