from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Vehicle, Driver, VehicleStatus
from app.schemas import VehicleOut, DriverOut
from app.auth import get_current_user, RoleChecker, UserRole

router = APIRouter()

@router.get("/vehicles", response_model=List[VehicleOut])
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle))
    return result.scalars().all()

@router.get("/drivers", response_model=List[DriverOut])
async def get_drivers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver))
    return result.scalars().all()

@router.get("/available", response_model=List[VehicleOut])
async def get_available_fleet(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.status == VehicleStatus.AVAILABLE))
    return result.scalars().all()

@router.get("/capacity")
async def get_fleet_capacity(db: AsyncSession = Depends(get_db)):
    # Collaborative Logistics: calculate unused capacity
    result = await db.execute(select(Vehicle).where(Vehicle.status == VehicleStatus.IN_TRANSIT))
    vehicles = result.scalars().all()
    
    # Mock calculation for demo
    total_unused = sum([v.capacity_kg * 0.3 for v in vehicles]) # Assume 30% average unused for demo
    return {
        "total_unused_kg": round(total_unused, 1),
        "available_on_major_routes": [
            {"route": "Mumbai→Delhi", "free_kg": 1800, "departure": "Tomorrow 14:00"},
            {"route": "Chennai→Bangalore", "free_kg": 450, "departure": "Today 22:00"}
        ]
    }
