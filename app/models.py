from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import datetime
import enum
import uuid

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPPLIER = "supplier"
    CUSTOMER = "customer"
    DRIVER = "driver"

class Priority(str, enum.Enum):
    URGENT = "urgent"
    STANDARD = "standard"
    ECONOMY = "economy"

class TransportMode(str, enum.Enum):
    ROAD = "road"
    AIR = "air"
    SEA = "sea"
    RAIL = "rail"
    MULTIMODAL = "multimodal"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELAYED = "delayed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class VehicleType(str, enum.Enum):
    TRUCK = "truck"
    VAN = "van"
    CARGO_PLANE = "cargo_plane"
    CONTAINER_SHIP = "container_ship"
    TRAIN = "train"

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_TRANSIT = "in_transit"
    MAINTENANCE = "maintenance"
    IDLE = "idle"

class FuelType(str, enum.Enum):
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    JET_FUEL = "jet_fuel"
    BUNKER = "bunker"

class AlertType(str, enum.Enum):
    DELAY = "delay"
    EMERGENCY = "emergency"
    DISRUPTION = "disruption"
    WEATHER = "weather"
    MAINTENANCE = "maintenance"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    full_name = Column(String)
    phone = Column(String)
    company = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    address = Column(String)
    country = Column(String)
    rating = Column(Float, default=5.0)
    total_orders = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4())[:8].upper())
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    origin_address = Column(String)
    origin_lat = Column(Float)
    origin_lon = Column(Float)
    origin_city = Column(String)
    origin_country = Column(String)
    
    dest_address = Column(String)
    dest_lat = Column(Float)
    dest_lon = Column(Float)
    dest_city = Column(String)
    dest_country = Column(String)
    
    weight_kg = Column(Float)
    volume_m3 = Column(Float)
    priority = Column(Enum(Priority), default=Priority.STANDARD)
    transport_mode = Column(Enum(TransportMode), default=TransportMode.ROAD)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    estimated_eta = Column(DateTime)
    actual_eta = Column(DateTime)
    distance_km = Column(Float)
    cost_usd = Column(Float)
    carbon_kg = Column(Float)
    route_json = Column(JSON)
    ai_explanation = Column(Text)
    delay_reason = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    delivered_at = Column(DateTime)
    
    is_international = Column(Boolean, default=False)
    goods_type = Column(String)
    special_instructions = Column(Text)

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True)
    type = Column(Enum(VehicleType))
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    capacity_kg = Column(Float)
    current_lat = Column(Float)
    current_lon = Column(Float)
    current_city = Column(String)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    fuel_type = Column(Enum(FuelType))
    last_maintenance = Column(DateTime)
    mileage_km = Column(Float, default=0.0)
    next_maintenance_due = Column(Float)

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    license_number = Column(String)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    rating = Column(Float, default=5.0)
    total_deliveries = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    current_lat = Column(Float)
    current_lon = Column(Float)

class TrackingEvent(Base):
    __tablename__ = "tracking_events"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String)
    message = Column(String)
    transport_mode = Column(Enum(TransportMode))
    speed_kmh = Column(Float)
    heading = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    type = Column(Enum(AlertType))
    message = Column(String)
    severity = Column(Enum(AlertSeverity))
    is_read = Column(Boolean, default=False)
    auto_rerouted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    body = Column(String)
    type = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DisruptionEvent(Base):
    __tablename__ = "disruptions"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String) # weather, traffic, etc.
    severity = Column(Float) # 0.0 to 1.0
    affected_region = Column(String)
    description = Column(String)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ends_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    impacted_orders_count = Column(Integer, default=0)

class RouteSegment(Base):
    __tablename__ = "route_segments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    segment_index = Column(Integer)
    mode = Column(Enum(TransportMode))
    from_lat = Column(Float)
    from_lon = Column(Float)
    from_name = Column(String)
    to_lat = Column(Float)
    to_lon = Column(Float)
    to_name = Column(String)
    distance_km = Column(Float)
    duration_min = Column(Integer)
    polyline_json = Column(JSON)
    status = Column(String)
