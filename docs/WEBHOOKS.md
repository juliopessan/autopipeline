# 🔔 Webhook Integration Guide

## Overview

Webhooks allow real-time event notifications for your optimization programs. When events occur (experiments complete, anomalies detected, etc.), we send JSON payloads to your configured endpoints.

## Features

✅ Multiple event types (experiment_created, experiment_completed, anomaly_detected, program_completed)
✅ Automatic retries (3 attempts with backoff)
✅ Slack & Teams integration examples
✅ Custom integration support
✅ Test webhook functionality
✅ Webhook management UI in dashboard

## Quick Start

### 1. Create a Webhook

Go to Dashboard → 🔔 Webhooks → Create Webhook

**Fields:**
- **Name**: Descriptive name (e.g., "Slack Notifications")
- **URL**: Your webhook endpoint
- **Event Type**: Which events to trigger

### 2. Test the Webhook

Click the "Test" button to verify your endpoint works.

### 3. Receive Events

When events occur, we'll POST JSON to your URL.

## Webhook Payload

```json
{
  "event": "experiment_completed",
  "timestamp": "2025-03-23T12:00:00Z",
  "data": {
    "experiment_id": 42,
    "program_id": 5,
    "result": 1.25,
    "cost": 0.50,
    "duration_seconds": 120,
    "parameters": {"param1": 0.5, "param2": 0.8}
  }
}
```

## Event Types

| Event | Triggered When | Data Payload |
|-------|---|---|
| `experiment_created` | New experiment created | experiment_id, program_id, parameters |
| `experiment_completed` | Experiment finishes | experiment_id, result, cost, duration |
| `experiment_failed` | Experiment fails | experiment_id, error_message |
| `anomaly_detected` | Anomaly found | experiment_id, anomaly_score |
| `program_completed` | Program finishes | program_id, total_experiments |
| `all` | Any event | All of the above |

## Integration Guides

### Slack

1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. Enable Incoming Webhooks
4. Add New Webhook to Workspace
5. Copy webhook URL to dashboard

### Microsoft Teams

1. Open your Teams channel
2. Click ⋯ (More options) → Connectors
3. Search "Incoming Webhook"
4. Configure → Copy webhook URL
5. Paste in dashboard

### Custom Integration

```python
# Example Flask endpoint
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.json
    print(f"Event: {event['event']}")
    print(f"Data: {event['data']}")
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run()
```

## Retry Logic

If your endpoint returns non-2xx status:
- Attempt 1: Immediate
- Attempt 2: 30 seconds later
- Attempt 3: 2 minutes later

After 3 attempts, webhook is marked as failed.

## Security Best Practices

1. ✅ Use HTTPS endpoints only
2. ✅ Validate webhook source (check X-Delivery-ID header)
3. ✅ Implement timeout handling
4. ✅ Process webhooks asynchronously
5. ✅ Log all webhook deliveries

## Headers

Each webhook request includes:

```
Content-Type: application/json
User-Agent: Autopipeline-Webhook/1.0
X-Webhook-Event: experiment_completed
X-Delivery-ID: 42-1679584800.123456
```

## Testing

Use the "Test" button in Dashboard → Webhooks to send a test payload to your endpoint.

Test payload:
```json
{
  "event": "test",
  "timestamp": "2025-03-23T12:00:00Z",
  "data": {
    "test": true,
    "webhook_id": 1,
    "webhook_name": "Test Webhook"
  }
}
```

## Troubleshooting

**Webhook not firing?**
- Check webhook is enabled (green indicator)
- Verify event type matches
- Test webhook with "Test" button
- Check endpoint logs for POST requests

**Connection refused?**
- Verify URL is correct
- Check firewall allows outbound connections
- Ensure endpoint is running

**Timeout errors?**
- Implement request timeout handling
- Return response within 30 seconds
- Process heavy tasks asynchronously

## API Endpoints

### List Webhooks
```
GET /api/webhooks
```

### Create Webhook
```
POST /api/webhooks
{
  "name": "string",
  "url": "string",
  "event_type": "string"
}
```

### Get Webhook
```
GET /api/webhooks/{webhook_id}
```

### Update Webhook
```
PUT /api/webhooks/{webhook_id}
{
  "name": "string",
  "url": "string",
  "event_type": "string"
}
```

### Delete Webhook
```
DELETE /api/webhooks/{webhook_id}
```

### Toggle Webhook
```
PATCH /api/webhooks/{webhook_id}/toggle
```

### Test Webhook
```
POST /api/webhooks/{webhook_id}/test
```

### Get Logs
```
GET /api/webhooks/{webhook_id}/logs?limit=20
```

---

**Status**: ✅ Phase 4 Complete
