"""
Tracksy Global — Notification Service.
"""
from database import get_db

class NotificationService:
    @staticmethod
    def send(recipient_type, recipient_id, title, message, notif_type='info', order_id=None):
        try:
            db = get_db()
            db.execute(
                "INSERT INTO notifications (recipient_type, recipient_id, title, message, type, order_id) VALUES (?, ?, ?, ?, ?, ?)",
                (recipient_type, str(recipient_id), title, message, notif_type, order_id)
            )
            db.commit()
            print(f"[SMS SIMULATED] To: {recipient_type} {recipient_id} | {title} - {message}")
            
            from app import socketio
            socketio.emit('notification_new', {
                'title': title,
                'message': message,
                'type': notif_type,
                'order_id': order_id
            })
        except Exception as e:
            print(f"Error sending notification: {e}")
