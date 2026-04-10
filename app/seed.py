import asyncio
import datetime
import random
from sqlalchemy import select
from app.database import AsyncSessionLocal, engine, Base
from app.models import (
    User, Supplier, Vehicle, Driver, Order, TrackingEvent, 
    UserRole, TransportMode, Priority, OrderStatus, VehicleType, FuelType, VehicleStatus
)
from app.auth import get_password_hash

# Coordinate Hubs
HUBS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Hamburg": (53.5511, 9.9937),
    "Rotterdam": (51.9244, 4.4777),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Dubai": (25.2048, 55.2708),
    "Singapore": (1.3521, 103.8198),
    "Shanghai": (31.2304, 121.4737),
    "Tokyo": (35.6762, 139.6503),
    "São Paulo": (-23.5505, -46.6333),
    "Nairobi": (-1.2921, 36.8219),
}

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # 1. Create Users
        users_data = [
            ("admin@tracksy.io", UserRole.ADMIN, "Admin User"),
            ("supplier@demo.com", UserRole.SUPPLIER, "Global Supplier Co."),
            ("customer@demo.com", UserRole.CUSTOMER, "Happy Customer"),
            ("driver@demo.com", UserRole.DRIVER, "Pro Driver"),
        ]
        
        users = {}
        for email, role, name in users_data:
            hashed = get_password_hash("tracksy2024")
            u = User(email=email, hashed_password=hashed, role=role, full_name=name)
            db.add(u)
            users[role] = u
        
        await db.flush()

        # 2. Create Supplier & Driver detail
        supplier = Supplier(user_id=users[UserRole.SUPPLIER].id, company_name="Global Supplier Co.", country="India")
        db.add(supplier)
        
        driver = Driver(user_id=users[UserRole.DRIVER].id, license_number="DL-123456789", is_available=True)
        db.add(driver)
        
        await db.flush()

        # 3. Create Vehicles
        vehicles_data = [
            ("MH-01-AX-1234", VehicleType.TRUCK, 12000, FuelType.DIESEL),
            ("DL-02-BY-5678", VehicleType.VAN, 2000, FuelType.ELECTRIC),
            ("N908TK", VehicleType.CARGO_PLANE, 80000, FuelType.JET_FUEL),
            ("EVER-GREEN-01", VehicleType.CONTAINER_SHIP, 2000000, FuelType.BUNKER),
            ("TR-INDIA-101", VehicleType.TRAIN, 500000, FuelType.DIESEL),
            ("MH-04-AB-1234", VehicleType.TRUCK, 15000, FuelType.DIESEL),
        ]
        
        vehicles = []
        for plate, v_type, cap, fuel in vehicles_data:
            v = Vehicle(
                license_plate=plate, type=v_type, capacity_kg=cap, fuel_type=fuel,
                status=VehicleStatus.AVAILABLE, next_maintenance_due=10000,
                current_lat=HUBS["Mumbai"][0], current_lon=HUBS["Mumbai"][1],
                current_city="Mumbai"
            )
            db.add(v)
            vehicles.append(v)
        
        await db.flush()
        
        # Assign driver to one vehicle
        driver.vehicle_id = vehicles[0].id
        vehicles[0].driver_id = driver.id

        # 4. Seed Orders (25 total)
        orders_config = [
            # 8 Domestic India
            ("Mumbai", "Delhi", TransportMode.ROAD, Priority.STANDARD),
            ("Chennai", "Bangalore", TransportMode.ROAD, Priority.URGENT),
            ("Kolkata", "Hyderabad", TransportMode.ROAD, Priority.ECONOMY),
            ("Delhi", "Mumbai", TransportMode.ROAD, Priority.STANDARD),
            ("Bangalore", "Chennai", TransportMode.ROAD, Priority.STANDARD),
            ("Hyderabad", "Kolkata", TransportMode.ROAD, Priority.STANDARD),
            ("Mumbai", "Chennai", TransportMode.ROAD, Priority.STANDARD),
            ("Delhi", "Bangalore", TransportMode.ROAD, Priority.URGENT),
            # 5 India -> Europe
            ("Chennai", "Hamburg", TransportMode.SEA, Priority.ECONOMY),
            ("Mumbai", "Rotterdam", TransportMode.SEA, Priority.STANDARD),
            ("Delhi", "London", TransportMode.AIR, Priority.URGENT),
            ("Kolkata", "Hamburg", TransportMode.SEA, Priority.STANDARD),
            ("Mumbai", "London", TransportMode.AIR, Priority.STANDARD),
            # 4 India -> USA
            ("Delhi", "New York", TransportMode.AIR, Priority.URGENT),
            ("Mumbai", "Los Angeles", TransportMode.AIR, Priority.STANDARD),
            ("Chennai", "New York", TransportMode.AIR, Priority.STANDARD),
            ("Bangalore", "Los Angeles", TransportMode.AIR, Priority.STANDARD),
            # 3 Intra-Asia
            ("Delhi", "Dubai", TransportMode.MULTIMODAL, Priority.STANDARD),
            ("Mumbai", "Singapore", TransportMode.SEA, Priority.STANDARD),
            ("Chennai", "Tokyo", TransportMode.SEA, Priority.STANDARD),
            # 3 S.America / Africa
            ("Mumbai", "São Paulo", TransportMode.SEA, Priority.ECONOMY),
            ("Delhi", "Nairobi", TransportMode.AIR, Priority.STANDARD),
            ("Chennai", "Nairobi", TransportMode.SEA, Priority.STANDARD),
            # 2 In-Transit with events
            ("Mumbai", "Delhi", TransportMode.ROAD, Priority.STANDARD),
            ("London", "New York", TransportMode.AIR, Priority.URGENT),
        ]

        for i, (orig, dest, mode, prio) in enumerate(orders_config):
            orig_coords = HUBS[orig]
            dest_coords = HUBS[dest]
            
            status = OrderStatus.PENDING
            if i >= 23: # Last 2 are in-transit
                status = OrderStatus.IN_TRANSIT
            elif i >= 20: # Some assigned
                status = OrderStatus.ASSIGNED
                
            order = Order(
                supplier_id=supplier.id,
                customer_id=users[UserRole.CUSTOMER].id,
                origin_city=orig, origin_lat=orig_coords[0], origin_lon=orig_coords[1], origin_address=f"{orig} Port/Hub", origin_country="India",
                dest_city=dest, dest_lat=dest_coords[0], dest_lon=dest_coords[1], dest_address=f"{dest} Delivery", dest_country="Global",
                weight_kg=500 + (i * 100), volume_m3=2.5,
                priority=prio, transport_mode=mode, status=status,
                estimated_eta=datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(2, 20)),
                distance_km=random.randint(500, 15000), cost_usd=random.randint(200, 5000),
                carbon_kg=random.randint(50, 2000),
                goods_type="Electronics" if i % 2 == 0 else "Pharma",
                ai_explanation=f"Optimized {mode.value} route selected for {prio.value} delivery."
            )
            
            if status == OrderStatus.IN_TRANSIT:
                order.vehicle_id = vehicles[i % len(vehicles)].id
                order.driver_id = driver.id
            
            db.add(order)
            await db.flush()
            
            # 5. Tracking events for in-transit orders
            if status == OrderStatus.IN_TRANSIT:
                for step in range(5):
                    # Simple interpolation for demo waypoints
                    t_lat = orig_coords[0] + (dest_coords[0] - orig_coords[0]) * (step / 10.0)
                    t_lon = orig_coords[1] + (dest_coords[1] - orig_coords[1]) * (step / 10.0)
                    evt = TrackingEvent(
                        order_id=order.id, lat=t_lat, lon=t_lon,
                        status="In Transit", message=f"Approaching waypoint {step+1}",
                        transport_mode=mode, speed_kmh=60 if mode == TransportMode.ROAD else 800,
                        heading=45.0
                    )
                    db.add(evt)
        
        # 1 Order currently delayed
        order_delayed = await db.scalar(select(Order).where(Order.status == OrderStatus.IN_TRANSIT).limit(1))
        if order_delayed:
            order_delayed.status = OrderStatus.DELAYED
            order_delayed.delay_reason = "Weather"

        await db.commit()
        print("Seed complete: 4 Users, 6 Vehicles, 25 Orders created.")

if __name__ == "__main__":
    asyncio.run(seed_data())
