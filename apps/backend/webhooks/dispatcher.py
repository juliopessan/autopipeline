"""Webhook event dispatcher"""
import requests
from typing import Dict, Any
from datetime import datetime
import json
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class WebhookDispatcher:
    """Dispatch events to registered webhooks"""
    
    def __init__(self, db: Session):
        self.db = db
        self.timeout = 5  # seconds
    
    def dispatch(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch event to all matching webhooks
        
        Args:
            event_type: Type of event (e.g., "experiment_completed")
            data: Event data payload
        
        Returns:
            Dispatch results
        """
        from models import Webhook
        
        # Find matching webhooks
        webhooks = self.db.query(Webhook).filter(
            (Webhook.event_type == event_type) | (Webhook.event_type == "all"),
            Webhook.is_active == True
        ).all()
        
        results = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "webhooks_triggered": len(webhooks),
            "deliveries": []
        }
        
        # Send to each webhook
        for webhook in webhooks:
            delivery = self.send(webhook, event_type, data)
            results["deliveries"].append(delivery)
        
        return results
    
    def send(self, webhook, event_type: str, data: Dict[str, Any]) -> Dict:
        """Send webhook to single endpoint"""
        payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        delivery = {
            "webhook_id": webhook.id,
            "webhook_name": webhook.name,
            "url": webhook.url,
            "status": "pending",
            "status_code": None,
            "error": None,
            "attempts": 0
        }
        
        # Retry logic
        max_attempts = 3
        for attempt in range(max_attempts):
            delivery["attempts"] = attempt + 1
            
            try:
                response = requests.post(
                    webhook.url,
                    json=payload,
                    timeout=self.timeout,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "Autopipeline-Webhook/1.0",
                        "X-Webhook-Event": event_type,
                        "X-Delivery-ID": f"{webhook.id}-{datetime.utcnow().timestamp()}"
                    }
                )
                
                delivery["status_code"] = response.status_code
                
                if response.status_code < 300:
                    delivery["status"] = "success"
                    logger.info(f"Webhook {webhook.id} delivered successfully")
                    break
                else:
                    delivery["error"] = f"HTTP {response.status_code}"
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Webhook {webhook.id} failed with {response.status_code}, "
                            f"retrying ({attempt + 1}/{max_attempts})"
                        )
                    else:
                        delivery["status"] = "failed"
            
            except requests.Timeout:
                delivery["error"] = "Timeout"
                delivery["status"] = "timeout"
                logger.warning(f"Webhook {webhook.id} timeout")
                
            except requests.ConnectionError:
                delivery["error"] = "Connection error"
                delivery["status"] = "connection_error"
                logger.warning(f"Webhook {webhook.id} connection error")
                
            except Exception as e:
                delivery["error"] = str(e)
                delivery["status"] = "error"
                logger.error(f"Webhook {webhook.id} error: {e}")
        
        return delivery
    
    def send_test(self, webhook, test_data: Dict = None) -> bool:
        """Send test webhook"""
        test_payload = test_data or {
            "event": "test",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "test": True,
                "webhook_id": webhook.id,
                "webhook_name": webhook.name
            }
        }
        
        try:
            response = requests.post(
                webhook.url,
                json=test_payload,
                timeout=self.timeout,
                headers={
                    "Content-Type": "application/json",
                    "X-Webhook-Event": "test",
                    "X-Test": "true"
                }
            )
            
            return response.status_code < 300
        except Exception as e:
            logger.error(f"Test webhook failed: {e}")
            return False
