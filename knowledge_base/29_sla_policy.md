# Service Level Agreement (SLA)

Our SLA defines the uptime and support commitments we make to customers on paid plans.

## Uptime Commitments

| Plan | Monthly Uptime SLA | Credits if Missed |
|------|-------------------|-------------------|
| Free | No SLA | None |
| Starter | No SLA | None |
| Pro | **99.9%** (~43 min/month downtime) | Service credits |
| Enterprise | **99.99%** (~4 min/month downtime) | Credits + penalty |

## Downtime Definition

Downtime is defined as the API returning errors for **>50% of requests** for **>5 consecutive minutes**. Planned maintenance windows (with 48 hours notice) are excluded.

## Service Credits

If we miss SLA targets, you receive credits on your next invoice:

| Uptime Achieved | Credit |
|----------------|--------|
| 99.0% – 99.9% | 10% of monthly fee |
| 95.0% – 99.0% | 25% of monthly fee |
| < 95.0% | 50% of monthly fee |

### Requesting Credits
1. Email billing@example.com within **30 days** of the incident
2. Reference the incident ID from our status page
3. Credits are applied within 2 billing cycles

## Support Response Times

| Priority | Pro SLA | Enterprise SLA |
|----------|---------|----------------|
| P1 – Service down | 2 hours | 30 minutes |
| P2 – Major feature broken | 4 hours | 1 hour |
| P3 – Minor bug | 1 business day | 4 hours |
| P4 – Question / feature request | 3 business days | 1 business day |

## Planned Maintenance

We schedule maintenance during low-traffic windows:
- **Standard maintenance**: Tuesdays 02:00–04:00 UTC
- Minimum **48 hours notice** via email and status page
- Emergency patches may require shorter notice

## Monitoring and Status

Real-time status and incident history: `https://status.example.com`
Subscribe to email/SMS/Slack alerts for incidents.
