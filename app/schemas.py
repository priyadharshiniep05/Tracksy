from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.models import UserRole, Priority, TransportMode, OrderStatus, VehicleType, VehicleStatus, FuelType, AlertType, AlertSeverity

# Auth
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER
    company: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Supplier
class SupplierBase(BaseModel):
    company_name: str
    contact_email: EmailStr
    contact_phone: str
    address: str
    country: str

class SupplierOut(SupplierBase):
    id: int
    rating: float
    total_orders: int

    class Config:
        from_attributes = True

# Order
class OrderBase(BaseModel):
    origin_address: str
    origin_lat: float
    origin_lon: float
    origin_city: str
    origin_country: str
    dest_address: str
    dest_lat: float
    dest_lon: float
    dest_city: str
    dest_country: str
    weight_kg: float
    volume_m3: float
    priority: Priority = Priority.STANDARD
    transport_mode: TransportMode = TransportMode.ROAD
    goods_type: str
    special_instructions: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    tracking_id: str
    status: OrderStatus
    estimated_eta: Optional[datetime] = None
    actual_eta: Optional[datetime] = None
    distance_km: Optional[float] = None
    cost_usd: Optional[float] = None
    carbon_kg: Optional[float] = None
    ai_explanation: Optional[str] = None
    delay_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Vehicle
class VehicleBase(BaseModel):
    license_plate: str
    type: VehicleType
    capacity_kg: float
    fuel_type: FuelType
    next_maintenance_due: float

class VehicleOut(VehicleBase):
    id: int
    driver_id: Optional[int] = None
    current_lat: Optional[float] = None
    current_lon: Optional[float] = None
    current_city: Optional[str] = None
    status: VehicleStatus
    last_maintenance: Optional[datetime] = None
    mileage_km: float

    class Config:
        from_attributes = True

# Driver
class DriverBase(BaseModel):
    license_number: str

class DriverOut(DriverBase):
    id: int
    user_id: int
    vehicle_id: Optional[int] = None
    rating: float
    total_deliveries: int
    is_available: bool
    current_lat: Optional[float] = None
    current_lon: Optional[float] = None

    class Config:
        from_attributes = True

# Tracking
class TrackingEventBase(BaseModel):
    lat: float
    lon: float
    status: str
    message: str
    transport_mode: TransportMode
    speed_kmh: float
    heading: float

class TrackingEventCreate(TrackingEventBase):
    order_id: int

class TrackingEventOut(TrackingEventBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Alert
class AlertOut(BaseModel):
    id: int
    order_id: int
    type: AlertType
    message: str
    severity: AlertSeverity
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Analytics
class AnalyticsSummary(BaseModel):
    active_shipments: int
    on_time_rate: float
    total_cost_today: float
    carbon_saved_today: float
    fleet_utilization: float
    pending_alerts: int
