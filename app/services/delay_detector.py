import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Order, TrackingEvent, Alert, AlertType, AlertSeverity, OrderStatus
from app.services.notification_service import notification_service

scheduler = AsyncIOScheduler()

async def check_for_delays():
    """
    Background task: scans in_transit vehicles for inactivity.
    Runs every 5 minutes.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch all in_transit orders
        result = await db.execute(select(Order).where(Order.status == OrderStatus.IN_TRANSIT))
        orders = result.scalars().all()
        
        for order in orders:
            # 2. Get latest tracking event
            evt_res = await db.execute(
                select(TrackingEvent)
                .where(TrackingEvent.order_id == order.id)
                .order_by(TrackingEvent.timestamp.desc())
                .limit(1)
            )
            latest_evt = evt_res.scalars().first()
            
            if not latest_evt:
                continue
                
            # 3. If position unchanged for > 2 hours
            now = datetime.datetime.utcnow()
            diff = now - latest_evt.timestamp.replace(tzinfo=None)
            
            if diff.total_seconds() > 3600 * 2:
                # Potential delay detected
                alert = Alert(
                    order_id=order.id,
                    type=AlertType.DELAY,
                    message=f"Vehicle stuck at {order.origin_city} for >2h.",
                    severity=AlertSeverity.MEDIUM
                )
                db.add(alert)
                
                await notification_service.send_notification(
                    user_id=order.customer_id,
                    title="Potential Shipping Delay",
                    body=f"Your order {order.tracking_id} might be delayed due to inactivity."
                )
                
        await db.commit()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(check_for_delays, "interval", minutes=5)
        scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
