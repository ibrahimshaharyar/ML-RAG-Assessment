# SDK Quickstart

Get up and running with our official Python SDK in under 5 minutes.

## Installation

```bash
pip install example-sdk
```

## Authentication

```python
from example_sdk import Client

client = Client(api_key="YOUR_API_KEY")
# Or use environment variable: EXAMPLE_API_KEY
client = Client()  # auto-reads from env
```

## Submitting a Query

```python
response = client.query("How do I reset my password?")
print(response.answer)
print(f"Sources: {response.sources}")
print(f"Latency: {response.latency_ms}ms")
```

## Batch Queries

```python
questions = [
    "What payment methods do you accept?",
    "How do I cancel my subscription?",
    "What are the rate limits?"
]

results = client.batch_query(questions)
for q, r in zip(questions, results):
    print(f"Q: {q}\nA: {r.answer}\n")
```

## Async Support

```python
import asyncio
from example_sdk import AsyncClient

async def main():
    client = AsyncClient(api_key="YOUR_API_KEY")
    response = await client.query("How do I export my data?")
    print(response.answer)

asyncio.run(main())
```

## Configuration Options

```python
client = Client(
    api_key="YOUR_KEY",
    timeout=30,           # seconds
    max_retries=3,
    base_url="https://api.example.com/v1"
)
```

## Error Handling

```python
from example_sdk import Client, RateLimitError, AuthError

try:
    response = client.query("...")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthError:
    print("Invalid API key")
```

## SDK Reference Docs

Full documentation available at: `https://docs.example.com/sdk`
