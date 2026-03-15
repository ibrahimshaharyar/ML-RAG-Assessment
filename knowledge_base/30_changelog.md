# Changelog

All notable changes to the platform are documented here.

---

## v2.4.0 — March 2025

### New Features
- **Batch Query API**: Submit up to 50 questions in a single API call (`POST /v1/batch-ask`)
- **Streaming Responses**: Long answers can now be streamed via Server-Sent Events
- **Custom Role Permissions** (Enterprise): Create fine-grained custom roles

### Improvements
- Reduced median query latency by 35% through embedding cache optimisation
- ChromaDB persistence now auto-compacts nightly for faster retrieval
- Dashboard query history now includes cost estimates per query

### Bug Fixes
- Fixed: Rate limit headers were missing on 429 responses
- Fixed: Webhook retries were not triggering for `query.failed` events
- Fixed: 2FA backup codes were not invalidated after account password reset

---

## v2.3.0 — January 2025

### New Features
- **Zapier Integration**: Connect to 5,000+ apps via Zapier
- **Audit Log Alerts** (Enterprise): Set up alerts for suspicious activity
- **Annual Billing**: Save 20% with annual subscription plans

### Improvements
- SSO setup flow redesigned — now takes under 5 minutes
- Invoice PDFs now include itemised tax breakdown
- API keys can now be scoped to specific IP addresses

### Bug Fixes
- Fixed: Team invites were not expiring after 48 hours
- Fixed: Data export emails sometimes arrived in spam

---

## v2.2.0 — November 2024

### New Features
- **Slack Integration**: Ask questions and receive alerts in Slack
- **Evaluation API**: Programmatically measure retrieval recall and answer quality
- **OpenTelemetry Support**: Export traces to any OTLP-compatible backend

### Improvements
- Chunk overlap now configurable via `config.yaml`
- Improved retrieval accuracy by 12% using re-ranking (cohere rerank)

### Bug Fixes
- Fixed: Queries with special characters were sometimes failing
- Fixed: ChromaDB collection was not properly isolated between team workspaces

---

## v2.1.0 — September 2024

### New Features
- **FastAPI Endpoint**: `POST /ask` for programmatic access
- **Docker support**: Official Dockerfile and docker-compose configuration
- **GDPR Data Export**: Full self-serve data export

---

## v2.0.0 — July 2024

Initial public release of v2 platform.
- LangChain-based RAG pipeline
- ChromaDB vector store
- OpenAI GPT-4o-mini generation
- Starter, Pro and Enterprise plans launched
