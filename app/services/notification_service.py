from typing import Optional
from app.database import AsyncSessionLocal
from app.models import Notification

class NotificationService:
    """
    In-app toasts and notification center persistence.
    """
    
    async def send_notification(
        self, 
        user_id: int, 
        title: str, 
        body: str, 
        type: str = "info"
    ):
        async with AsyncSessionLocal() as db:
            notif = Notification(
                user_id=user_id,
                title=title,
                body=body,
                type=type
            )
            db.add(notif)
            await db.commit()
            
            # In a real app, we'd also push to WebSocket here
            print(f"NOTIFICATION for User {user_id}: {title} - {body}")

notification_service = NotificationService()
