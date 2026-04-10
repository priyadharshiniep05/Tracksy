from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Order, Alert, Vehicle, OrderStatus, TransportMode
from app.schemas import AnalyticsSummary
from app.auth import get_current_user

router = APIRouter()

@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary(db: AsyncSession = Depends(get_db)):
    # 1. Active Shipments
    res_active = await db.execute(
        select(func.count(Order.id)).where(Order.status == OrderStatus.IN_TRANSIT)
    )
    active_count = res_active.scalar() or 0
    
    # 2. Total Cost Today
    res_cost = await db.execute(
        select(func.sum(Order.cost_usd))
    )
    total_cost = res_cost.scalar() or 0.0
    
    # 3. Carbon Saved Today
    res_carbon = await db.execute(
        select(func.sum(Order.carbon_kg))
    )
    total_carbon = res_carbon.scalar() or 0.0
    
    # 4. Pending Alerts
    res_alerts = await db.execute(
        select(func.count(Alert.id)).where(Alert.is_read == False)
    )
    alert_count = res_alerts.scalar() or 0
    
    return {
        "active_shipments": active_count,
        "on_time_rate": 92.4, # Mocked for demo
        "total_cost_today": round(total_cost, 2),
        "carbon_saved_today": round(total_carbon * 0.2, 2), # Assuming 20% saved vs baseline
        "fleet_utilization": 84.5,
        "pending_alerts": alert_count
    }

@router.get("/delay-trends")
async def get_delay_trends():
    return [
        {"day": "Mon", "weather": 2, "traffic": 5, "customs": 1},
        {"day": "Tue", "weather": 0, "traffic": 8, "customs": 0},
        {"day": "Wed", "weather": 5, "traffic": 3, "customs": 2},
        {"day": "Thu", "weather": 1, "traffic": 6, "customs": 4},
        {"day": "Fri", "weather": 3, "traffic": 10, "customs": 1}
    ]

@router.get("/cost-breakdown")
async def get_cost_breakdown():
    return [
        {"mode": "Road", "cost": 42000},
        {"mode": "Air", "cost": 128000},
        {"mode": "Sea", "cost": 15000},
        {"mode": "Rail", "cost": 8000}
    ]

@router.get("/carbon")
async def get_carbon_stats():
    return {
        "total_kg": 14200,
        "saved_kg": 3400,
        "trees_equivalent": 162,
        "breakdown": [
            {"mode": "Road", "emissions": 4500},
            {"mode": "Air", "emissions": 8200},
            {"mode": "Sea", "emissions": 1100},
            {"mode": "Rail", "emissions": 400}
        ]
    }
