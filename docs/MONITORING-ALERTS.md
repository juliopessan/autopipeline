# 📊 Monitoring & Alerts Guide

## Overview

Real-time monitoring and intelligent alerting for your experiments and system health.

## Features

### 1. Event Tracking
- Experiment lifecycle tracking
- Performance metrics
- Anomaly events
- Custom events

### 2. Alert Generation
- Cost spike alerts
- Duration alerts
- Error rate alerts
- Budget threshold alerts
- Severity classification

### 3. Notifications
- Webhook notifications
- Email alerts
- Slack integration
- Teams integration
- SMS alerts

### 4. Timeline Analysis
- Daily event tracking
- Event type distribution
- Trend analysis
- Historical view

### 5. Budget Monitoring
- Real-time budget tracking
- Threshold alerts
- Usage percentage
- Forecast remaining budget

## API Endpoints

### Health Check
```
GET /api/monitoring/health
```

### Get Summary
```
GET /api/monitoring/summary
```

Response:
```json
{
  "total_events": 150,
  "experiments_started": 50,
  "experiments_completed": 48,
  "anomalies_detected": 3,
  "alerts_triggered": 12,
  "critical_alerts": 2
}
```

### Log Experiment Started
```
POST /api/monitoring/experiment-started
{
  "experiment_id": 1,
  "program_id": 5
}
```

### Log Experiment Completed
```
POST /api/monitoring/experiment-completed
{
  "experiment_id": 1,
  "result": 1.25,
  "cost": 75.0,
  "duration": 3600
}
```

### Get Alerts
```
GET /api/monitoring/alerts?severity=critical&limit=50
```

### Evaluate Budget
```
POST /api/monitoring/evaluate-budget
{
  "spent": 700.0,
  "budget": 1000.0
}
```

## Dashboard Tabs

### 🚨 Active Alerts
- Real-time alert feed
- Severity filtering
- Alert details
- Timestamp tracking

### 📈 Events Timeline
- Daily event graph
- Event distribution
- Historical view
- Event summary table

### 💰 Budget Monitor
- Budget gauge
- Usage percentage
- Threshold visualization
- Budget alerts

### 📋 Event Logs
- Raw event listing
- Filterable view
- Experiment tracking
- Status indicators

## Alert Rules

### Cost Rules
- **Cost Spike**: When cost > 1.5x average (HIGH severity)
- **High Cost**: When cost per minute > $0.10 (HIGH severity)

### Performance Rules
- **Long Duration**: When duration > 2 hours (MEDIUM severity)
- **High Error Rate**: When errors > 10% (CRITICAL severity)

### Budget Rules
- **Budget Warning**: When spent > 80% of budget (HIGH severity)
- **Budget Exceeded**: When spent >= 100% of budget (CRITICAL severity)

## Notification Channels

Supported channels:
- Webhook (to webhooks configured in cost intelligence)
- Email (requires email service)
- Slack (requires Slack integration)
- Teams (requires Teams integration)
- SMS (requires SMS service)

## Best Practices

1. **Monitor Regularly** - Check dashboard daily
2. **Act on Critical** - Respond immediately to critical alerts
3. **Set Budgets** - Configure realistic monthly budgets
4. **Review Timeline** - Analyze trends weekly
5. **Configure Notifications** - Set up preferred channels

## Integration with Other Features

### With Cost Intelligence
- Alerts trigger based on cost rules
- Budget evaluation uses cost data
- Recommendations feed alert insights

### With ML Analytics
- Anomaly detection triggers events
- Forecast alerts based on trends
- Clustering groups by cost profile

### With Webhooks
- Alerts sent via webhooks
- Custom webhook handling
- Slack/Teams integration

