import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from app.database import get_db
from app.models import Order, User, Supplier, Vehicle, Driver, OrderStatus, Priority, TransportMode, TrackingEvent
from app.schemas import OrderCreate, OrderOut, TrackingEventOut
from app.auth import get_current_user, RoleChecker, UserRole
from app.services.route_optimizer import route_optimizer
from app.services.eta_engine import eta_engine
from app.services.carbon_calculator import carbon_calculator
from app.services.ai_explanation import ai_explanation as ai_expr

router = APIRouter()

@router.get("/", response_model=List[OrderOut])
async def get_orders(
    status: Optional[OrderStatus] = None,
    priority: Optional[Priority] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order)
    if current_user.role == UserRole.SUPPLIER:
        # Supplier sees only their orders
        sup_res = await db.execute(select(Supplier).where(Supplier.user_id == current_user.id))
        supplier = sup_res.scalars().first()
        if supplier:
            query = query.where(Order.supplier_id == supplier.id)
    elif current_user.role == UserRole.CUSTOMER:
        query = query.where(Order.customer_id == current_user.id)
    elif current_user.role == UserRole.DRIVER:
        drv_res = await db.execute(select(Driver).where(Driver.user_id == current_user.id))
        driver = drv_res.scalars().first()
        if driver:
            query = query.where(Order.driver_id == driver.id)
            
    if status:
        query = query.where(Order.status == status)
    if priority:
        query = query.where(Order.priority == priority)
        
    result = await db.execute(query.order_by(desc(Order.created_at)))
    return result.scalars().all()

@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.SUPPLIER, UserRole.ADMIN]))
):
    # Lookup supplier
    sup_res = await db.execute(select(Supplier).where(Supplier.user_id == current_user.id))
    supplier = sup_res.scalars().first() if current_user.role == UserRole.SUPPLIER else None
    
    # Calculate routes metrics
    best_routes = await route_optimizer.optimize(
        {"lat": order_in.origin_lat, "lon": order_in.origin_lon},
        {"lat": order_in.dest_lat, "lon": order_in.dest_lon},
        order_in.weight_kg,
        order_in.priority,
        order_in.transport_mode
    )
    
    best = best_routes[0]
    eta_data = await eta_engine.calculate_eta(
        best['mode'], 
        best['distance_km'], 
        order_in.origin_lat, 
        order_in.origin_lon
    )
    
    new_order = Order(
        **order_in.model_dump(),
        supplier_id=supplier.id if supplier else None,
        status=OrderStatus.PENDING,
        distance_km=best['distance_km'],
        cost_usd=best['cost_usd'],
        carbon_kg=best['carbon_kg'],
        estimated_eta=eta_data['eta'],
        ai_explanation=ai_expr.generate_route_explanation(best),
        route_json={"segments": best_routes}
    )
    
    # Auto-assign if road mode
    if order_in.transport_mode == TransportMode.ROAD:
        v_res = await db.execute(select(Vehicle).where(Vehicle.status == "available").limit(1))
        vehicle = v_res.scalars().first()
        if vehicle:
            new_order.vehicle_id = vehicle.id
            new_order.driver_id = vehicle.driver_id
            new_order.status = OrderStatus.ASSIGNED
            vehicle.status = "in_transit"
            
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status")
async def update_status(order_id: int, status: OrderStatus, db: AsyncSession = Depends(get_db)):
    await db.execute(update(Order).where(Order.id == order_id).values(status=status))
    if status == OrderStatus.DELIVERED:
        await db.execute(update(Order).where(Order.id == order_id).values(delivered_at=datetime.datetime.utcnow()))
    await db.commit()
    return {"status": "success"}

@router.get("/{order_id}/tracking", response_model=List[TrackingEventOut])
async def get_tracking(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TrackingEvent)
        .where(TrackingEvent.order_id == order_id)
        .order_by(desc(TrackingEvent.timestamp))
    )
    return result.scalars().all()
