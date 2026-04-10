from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from app.database import get_db
from app.models import Alert, AlertSeverity, AlertType
from app.schemas import AlertOut
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AlertOut])
async def get_alerts(
    severity: Optional[AlertSeverity] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Alert)
    if severity:
        query = query.where(Alert.severity == severity)
        
    result = await db.execute(query.order_by(desc(Alert.created_at)))
    return result.scalars().all()

@router.patch("/{alert_id}/read")
async def mark_read(alert_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(update(Alert).where(Alert.id == alert_id).values(is_read=True))
    await db.commit()
    return {"status": "read"}

@router.post("/bulk-read")
async def bulk_read(db: AsyncSession = Depends(get_db)):
    await db.execute(update(Alert).values(is_read=True))
    await db.commit()
    return {"status": "all read"}
