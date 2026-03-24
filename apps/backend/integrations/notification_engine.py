"""Notification Engine for Alerts"""
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import json

class NotificationChannel(str, Enum):
    WEBHOOK = "webhook"
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    SMS = "sms"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Notification:
    """Represents a single notification"""
    
    def __init__(self, alert_type: str, message: str, 
                 severity: str, channels: List[NotificationChannel],
                 metadata: Dict = None):
        self.id = int(datetime.utcnow().timestamp() * 1000)
        self.alert_type = alert_type
        self.message = message
        self.severity = severity
        self.channels = channels
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow().isoformat()
        self.sent_at = None
        self.status = "pending"
    
    def to_dict(self):
        return {
            "id": self.id,
            "alert_type": self.alert_type,
            "message": self.message,
            "severity": self.severity,
            "channels": [c.value for c in self.channels],
            "created_at": self.created_at,
            "sent_at": self.sent_at,
            "status": self.status,
            "metadata": self.metadata
        }

class NotificationEngine:
    """Engine for managing notifications"""
    
    def __init__(self):
        self.notifications = []
        self.sent_count = 0
        self.failed_count = 0
    
    def create_notification(self, alert_type: str, message: str,
                          severity: str, 
                          channels: List[NotificationChannel],
                          metadata: Dict = None) -> Notification:
        """Create a new notification"""
        notification = Notification(alert_type, message, severity, channels, metadata)
        self.notifications.append(notification)
        return notification
    
    def send_notification(self, notification: Notification) -> bool:
        """Send notification through configured channels"""
        try:
            for channel in notification.channels:
                if channel == NotificationChannel.WEBHOOK:
                    self._send_webhook(notification)
                elif channel == NotificationChannel.EMAIL:
                    self._send_email(notification)
                elif channel == NotificationChannel.SLACK:
                    self._send_slack(notification)
                elif channel == NotificationChannel.TEAMS:
                    self._send_teams(notification)
                elif channel == NotificationChannel.SMS:
                    self._send_sms(notification)
            
            notification.sent_at = datetime.utcnow().isoformat()
            notification.status = "sent"
            self.sent_count += 1
            return True
        
        except Exception as e:
            notification.status = "failed"
            self.failed_count += 1
            print(f"Error sending notification: {e}")
            return False
    
    def _send_webhook(self, notification: Notification):
        """Send via webhook"""
        # Would call webhook endpoints configured for alerts
        pass
    
    def _send_email(self, notification: Notification):
        """Send via email"""
        # Would integrate with email service
        pass
    
    def _send_slack(self, notification: Notification):
        """Send via Slack webhook"""
        # Would integrate with Slack API
        pass
    
    def _send_teams(self, notification: Notification):
        """Send via Microsoft Teams webhook"""
        # Would integrate with Teams API
        pass
    
    def _send_sms(self, notification: Notification):
        """Send via SMS"""
        # Would integrate with SMS service
        pass
    
    def get_notifications(self, limit: int = 100) -> List[Dict]:
        """Get recent notifications"""
        return [n.to_dict() for n in self.notifications[-limit:]]
    
    def get_pending_notifications(self) -> List[Dict]:
        """Get pending notifications"""
        pending = [n for n in self.notifications if n.status == "pending"]
        return [n.to_dict() for n in pending]
    
    def get_statistics(self) -> Dict:
        """Get notification statistics"""
        total = len(self.notifications)
        pending = len([n for n in self.notifications if n.status == "pending"])
        sent = self.sent_count
        failed = self.failed_count
        
        return {
            "total_notifications": total,
            "pending": pending,
            "sent": sent,
            "failed": failed,
            "success_rate": (sent / (sent + failed) * 100) if (sent + failed) > 0 else 0
        }
