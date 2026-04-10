from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import DisruptionEvent
from app.services.disruption_engine import disruption_engine

router = APIRouter()

@router.get("/active")
async def get_active_disruptions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DisruptionEvent).where(DisruptionEvent.is_active == True))
    return result.scalars().all()

@router.post("/simulate")
async def simulate_disruption():
    """Demo button — creates a random disruption."""
    result = await disruption_engine.simulate_disruption()
    return result
