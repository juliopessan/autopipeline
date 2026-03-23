"""Webhook API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Webhook, User

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

class WebhookCreate(BaseModel):
    """Create webhook request"""
    name: str
    url: str
    event_type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Slack Notifications",
                "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
                "event_type": "experiment_completed"
            }
        }

class WebhookResponse(BaseModel):
    """Webhook response"""
    id: int
    name: str
    url: str
    event_type: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class WebhookTestRequest(BaseModel):
    """Test webhook request"""
    webhook_id: int
    test_data: dict = {
        "event": "test",
        "timestamp": "2025-03-23T12:00:00Z",
        "data": {"test": True}
    }

# ==================== ENDPOINTS ====================

@router.get("/", response_model=List[WebhookResponse])
async def list_webhooks(db: Session = Depends(get_db)):
    """List all webhooks"""
    webhooks = db.query(Webhook).all()
    return webhooks

@router.post("/", response_model=WebhookResponse)
async def create_webhook(webhook: WebhookCreate, db: Session = Depends(get_db)):
    """Create new webhook"""
    # Validate URL
    try:
        from urllib.parse import urlparse
        parsed = urlparse(webhook.url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL")
    except:
        raise HTTPException(status_code=400, detail="Invalid webhook URL")
    
    # Validate event type
    valid_events = [
        "experiment_created",
        "experiment_completed",
        "experiment_failed",
        "anomaly_detected",
        "program_completed",
        "all"
    ]
    
    if webhook.event_type not in valid_events:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid event type. Must be one of: {', '.join(valid_events)}"
        )
    
    # Create webhook
    db_webhook = Webhook(
        name=webhook.name,
        url=webhook.url,
        event_type=webhook.event_type,
        is_active=True
    )
    
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    
    return db_webhook

@router.get("/{webhook_id}", response_model=WebhookResponse)
async def get_webhook(webhook_id: int, db: Session = Depends(get_db)):
    """Get webhook by ID"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook

@router.put("/{webhook_id}", response_model=WebhookResponse)
async def update_webhook(webhook_id: int, webhook: WebhookCreate, 
                        db: Session = Depends(get_db)):
    """Update webhook"""
    db_webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not db_webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    db_webhook.name = webhook.name
    db_webhook.url = webhook.url
    db_webhook.event_type = webhook.event_type
    
    db.commit()
    db.refresh(db_webhook)
    
    return db_webhook

@router.delete("/{webhook_id}")
async def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    """Delete webhook"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    db.delete(webhook)
    db.commit()
    
    return {"status": "deleted", "webhook_id": webhook_id}

@router.patch("/{webhook_id}/toggle")
async def toggle_webhook(webhook_id: int, db: Session = Depends(get_db)):
    """Toggle webhook active status"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    webhook.is_active = not webhook.is_active
    db.commit()
    db.refresh(webhook)
    
    return {
        "webhook_id": webhook_id,
        "is_active": webhook.is_active
    }

@router.post("/{webhook_id}/test")
async def test_webhook(webhook_id: int, test_data: dict = None,
                      db: Session = Depends(get_db)):
    """Test webhook by sending test data"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    from webhooks.dispatcher import WebhookDispatcher
    
    dispatcher = WebhookDispatcher(db)
    success = dispatcher.send_test(webhook, test_data or {})
    
    if success:
        return {
            "status": "success",
            "webhook_id": webhook_id,
            "message": "Test webhook sent successfully"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send test webhook"
        )

@router.get("/{webhook_id}/logs")
async def get_webhook_logs(webhook_id: int, limit: int = 20,
                          db: Session = Depends(get_db)):
    """Get recent webhook delivery logs"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    # Mock logs (would query WebhookLog table in real app)
    return {
        "webhook_id": webhook_id,
        "logs": [
            {
                "timestamp": "2025-03-23T12:00:00Z",
                "status": "success",
                "status_code": 200,
                "event": "experiment_completed"
            }
        ]
    }
