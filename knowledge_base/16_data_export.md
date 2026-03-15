# Data Export

Export your data at any time. We support multiple formats for portability.

## What Can Be Exported

| Data Type | Formats Available |
|-----------|------------------|
| Query history | JSON, CSV |
| Team members | CSV |
| API usage logs | JSON, CSV |
| Billing history | PDF (invoices), CSV |
| Account settings | JSON |

## How to Export Data

### From the Dashboard

1. Go to **Settings → Data & Privacy → Export Data**
2. Select the data type(s) to export
3. Select the date range (or "All time")
4. Choose the format (JSON or CSV)
5. Click **"Request Export"**
6. You receive a download link via email within **30 minutes**

### Via API

```bash
curl -X POST https://api.example.com/v1/export \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query_history",
    "format": "json",
    "from": "2024-01-01",
    "to": "2024-12-31"
  }'
```

Response:
```json
{
  "export_id": "exp_abc123",
  "status": "processing",
  "estimated_ready_in": 300
}
```

## Downloading Your Export

Export files are available for **72 hours** after generation. Download them from:
- The emailed download link
- **Settings → Data & Privacy → Export History**

## GDPR Data Request

If you are requesting your data under **GDPR Article 15** (right of access):
1. Email privacy@example.com with subject "GDPR Data Access Request"
2. Include your account email and ID
3. We respond within **30 days** as required by law

## Large Exports

For accounts with large data volumes (>1M records), exports may take up to **2 hours**. You will be notified by email when ready.
