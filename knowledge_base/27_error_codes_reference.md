# Error Codes Reference

This reference lists all API error codes, their meanings, and how to resolve them.

## Error Response Format

All errors follow this JSON format:

```json
{
  "error": "error_code",
  "message": "Human-readable explanation",
  "request_id": "req_abc123",
  "docs_url": "https://docs.example.com/errors/error_code"
}
```

## Authentication Errors (4xx)

| Code | HTTP Status | Meaning | Resolution |
|------|------------|---------|-----------|
| `auth_required` | 401 | No API key provided | Add `Authorization: Bearer KEY` header |
| `auth_invalid` | 401 | API key is invalid or revoked | Check/regenerate your API key |
| `auth_expired` | 401 | OAuth token expired | Refresh your access token |
| `forbidden` | 403 | Key lacks required scope | Use a key with the correct permissions |

## Rate Limit Errors

| Code | HTTP Status | Meaning | Resolution |
|------|------------|---------|-----------|
| `rate_limit_exceeded` | 429 | Too many requests | Wait and retry after `Retry-After` header value |
| `daily_limit_reached` | 429 | Daily quota exhausted | Wait until midnight UTC or upgrade plan |

## Request Errors

| Code | HTTP Status | Meaning | Resolution |
|------|------------|---------|-----------|
| `invalid_request` | 400 | Malformed JSON or missing fields | Check your request body |
| `question_required` | 400 | `question` field is empty | Provide a non-empty question |
| `question_too_long` | 400 | Question > 1000 characters | Shorten your question |
| `not_found` | 404 | Resource doesn't exist | Check the endpoint URL |
| `method_not_allowed` | 405 | Wrong HTTP method | Use POST for `/ask`, GET for status |

## Server Errors

| Code | HTTP Status | Meaning | Resolution |
|------|------------|---------|-----------|
| `internal_error` | 500 | Unexpected server error | Retry with exponential backoff |
| `service_unavailable` | 503 | Service is down | Check `https://status.example.com` |
| `llm_error` | 502 | Upstream LLM provider error | Retry after 30 seconds |
| `retrieval_error` | 502 | Vector DB retrieval failed | Retry or contact support |

## Retry Strategy

For 5xx errors, use exponential backoff:

```python
import time

def retry_request(func, max_retries=3):
    for attempt in range(max_retries):
        response = func()
        if response.status_code < 500:
            return response
        wait = 2 ** attempt  # 1s, 2s, 4s
        time.sleep(wait)
    raise Exception("Service unavailable after retries")
```
