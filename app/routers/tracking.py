import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models import Order, TrackingEvent, OrderStatus, TransportMode
from app.schemas import TrackingEventCreate, TrackingEventOut

router = APIRouter()

@router.get("/public/{tracking_id}")
async def public_track(tracking_id: str, db: AsyncSession = Depends(get_db)):
    """Public tracking endpoint — no auth required."""
    result = await db.execute(
        select(Order).where(Order.tracking_id == tracking_id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Tracking ID not found")
        
    # Get latest event
    evt_res = await db.execute(
        select(TrackingEvent)
        .where(TrackingEvent.order_id == order.id)
        .order_by(desc(TrackingEvent.timestamp))
        .limit(1)
    )
    latest_event = evt_res.scalars().first()
    
    return {
        "tracking_id": order.tracking_id,
        "status": order.status,
        "origin": {"city": order.origin_city, "lat": order.origin_lat, "lon": order.origin_lon},
        "dest": {"city": order.dest_city, "lat": order.dest_lat, "lon": order.dest_lon},
        "estimated_eta": order.estimated_eta,
        "current_pos": {
            "lat": latest_event.lat if latest_event else order.origin_lat,
            "lon": latest_event.lon if latest_event else order.origin_lon,
            "speed": latest_event.speed_kmh if latest_event else 0,
            "message": latest_event.message if latest_event else "Preparing for shipment"
        },
        "carbon_kg": order.carbon_kg,
        "mode": order.transport_mode
    }

@router.post("/update")
async def post_location(
    event: TrackingEventCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Driver posts location updates."""
    new_event = TrackingEvent(**event.model_dump())
    db.add(new_event)
    
    # Update order status if it was assigned
    result = await db.execute(select(Order).where(Order.id == event.order_id))
    order = result.scalars().first()
    if order and order.status == OrderStatus.ASSIGNED:
        order.status = OrderStatus.IN_TRANSIT
        
    await db.commit()
    return {"status": "recorded"}

@router.get("/live")
async def live_stream(request: Request, db: AsyncSession = Depends(get_db)):
    """SSE endpoint for live dashboard updates."""
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            
            # Fetch active shipments
            # Using a fresh session inside the generator
            from app.database import AsyncSessionLocal
            async with AsyncSessionLocal() as session:
                res = await session.execute(
                    select(Order).where(Order.status == OrderStatus.IN_TRANSIT)
                )
                active_orders = res.scalars().all()
                
                data = []
                for order in active_orders:
                    # Get latest event
                    evt_res = await session.execute(
                        select(TrackingEvent)
                        .where(TrackingEvent.order_id == order.id)
                        .order_by(desc(TrackingEvent.timestamp))
                        .limit(1)
                    )
                    evt = evt_res.scalars().first()
                    if evt:
                        data.append({
                            "id": order.id,
                            "tracking_id": order.tracking_id,
                            "lat": evt.lat,
                            "lon": evt.lon,
                            "mode": evt.transport_mode
                        })
            
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(5) # Poll every 5s for SSE simulation

    return StreamingResponse(event_generator(), media_type="text/event-stream")
