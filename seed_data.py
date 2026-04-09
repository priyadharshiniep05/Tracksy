import sqlite3
import json
import random
from datetime import datetime, timedelta
from config import Config
from database import get_db

def seed_if_empty():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    if count > 0:
        print("Database already seeded.")
        return

    print("Seeding database...")
    
    cities = [
        {"name": "Mumbai", "lat": 19.0760, "lng": 72.8777},
        {"name": "Delhi", "lat": 28.6139, "lng": 77.2090},
        {"name": "Bengaluru", "lat": 12.9716, "lng": 77.5946},
        {"name": "Chennai", "lat": 13.0827, "lng": 80.2707},
        {"name": "Hyderabad", "lat": 17.3850, "lng": 78.4867},
        {"name": "Pune", "lat": 18.5204, "lng": 73.8567},
        {"name": "Ahmedabad", "lat": 23.0225, "lng": 72.5714},
        {"name": "Kolkata", "lat": 22.5726, "lng": 88.3639},
    ]

    suppliers = [
        ("ShipEase India Pvt Ltd", "Raj Sharma", "contact@shipease.in", "9876543210"),
        ("FastTrack Cargo", "Anita Desai", "info@fasttrack.in", "9876543211"),
        ("GreenHaul Logistics", "Vikram Singh", "hello@greenhaul.co.in", "9876543212")
    ]
    
    for s in suppliers:
        db.execute("INSERT INTO suppliers (name, contact_person, email, phone, city, lat, lng, rating, total_orders, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                   (s[0], s[1], s[2], s[3], 'Mumbai', 19.0, 72.8, 4.5, 120))

    vehicles = [
        ('MH01-TRUCK-1', 'truck', 5000, 20, 'diesel', 15000, 20000),
        ('DL02-VAN-5', 'van', 1500, 8, 'cng', 5000, 10000),
        ('KA05-EBIKE-9', 'bike', 50, 0.5, 'electric', 1000, 5000)
    ]
    for i, v in enumerate(vehicles):
        db.execute("INSERT INTO vehicles (registration, type, capacity_kg, capacity_cbm, driver_id, status, current_lat, current_lng, fuel_type, mileage_km, next_maintenance_due_km) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (v[0], v[1], v[2], v[3], i+1, 'available', cities[i]['lat'], cities[i]['lng'], v[4], v[5], v[6]))

    drivers = [
        ('Amit Patel', '9876543222', 'DL-12345'),
        ('Ravi Kumar', '9876543233', 'DL-23456'),
        ('Suresh Reddy', '9876543244', 'DL-34567')
    ]
    for i, d in enumerate(drivers):
        db.execute("INSERT INTO drivers (name, phone, license, vehicle_id, status, rating, total_deliveries) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (d[0], d[1], d[2], i+1, 'available', 4.8, 85))

    statuses = ['in_transit'] * 15 + ['delivered'] * 5 + ['delayed'] * 2 + ['pending'] * 2 + ['cancelled'] * 1
    
    for i in range(25):
        orig = random.choice(cities)
        dest = random.choice([c for c in cities if c != orig])
        status = statuses[i]
        
        # basic interpolation for "in_transit"
        curr_lat = orig['lat']
        curr_lng = orig['lng']
        if status == 'in_transit' or status == 'delayed':
            fraction = random.uniform(0.1, 0.9)
            curr_lat = orig['lat'] + (dest['lat'] - orig['lat']) * fraction
            curr_lng = orig['lng'] + (dest['lng'] - orig['lng']) * fraction
        elif status == 'delivered':
            curr_lat = dest['lat']
            curr_lng = dest['lng']
            
        waypoints = [[orig['lat'], orig['lng']], [curr_lat, curr_lng], [dest['lat'], dest['lng']]]

        # fix timestamps so datetime parser doesn't crash on sqlite string
        now = datetime.now()
        
        db.execute("""
            INSERT INTO orders (
                id, supplier_id, customer_name, customer_phone,
                origin_city, origin_lat, origin_lng,
                dest_city, dest_lat, dest_lng,
                weight_kg, volume_cbm, priority, status,
                current_lat, current_lng, route_json,
                eta, distance_km, ai_explanation, cost_estimate, carbon_kg, last_location_update, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"TRK-2025-{10000+i}", random.randint(1,3), f"Customer {i}", "9999999999",
            orig['name'], orig['lat'], orig['lng'],
            dest['name'], dest['lat'], dest['lng'],
            random.randint(10, 500), random.uniform(0.1, 5.0), random.choice(['casual', 'urgent']), status,
            curr_lat, curr_lng, json.dumps(waypoints),
            now + timedelta(hours=random.randint(2, 48)),
            random.randint(100, 1500), "AI calculated fastest route.",
            random.randint(50, 1500), random.uniform(5.0, 50.0),
            now, now - timedelta(days=1)
        ))
    db.commit()
    print("Database seeded with 25 orders, vehicles, and drivers.")

if __name__ == '__main__':
    from database import init_db
    init_db()
    seed_if_empty()
