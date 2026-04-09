import sqlite3
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database with the full application schema."""
    conn = get_db()
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            supplier_id INTEGER,
            customer_name TEXT,
            customer_phone TEXT,
            origin_city TEXT, origin_lat REAL, origin_lng REAL,
            dest_city TEXT, dest_lat REAL, dest_lng REAL,
            weight_kg REAL,
            volume_cbm REAL,
            priority TEXT,
            status TEXT,
            vehicle_id INTEGER,
            driver_id INTEGER,
            assigned_at TIMESTAMP,
            pickup_at TIMESTAMP,
            eta TIMESTAMP,
            delivered_at TIMESTAMP,
            current_lat REAL, current_lng REAL,
            route_json TEXT,
            ai_explanation TEXT,
            cost_estimate REAL,
            carbon_kg REAL,
            distance_km REAL,
            last_location_update TIMESTAMP,
            cancellation_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, contact_person TEXT, email TEXT, phone TEXT,
            city TEXT, lat REAL, lng REAL,
            rating REAL, total_orders INTEGER, created_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration TEXT, type TEXT,
            capacity_kg REAL, capacity_cbm REAL,
            driver_id INTEGER, status TEXT,
            current_lat REAL, current_lng REAL,
            fuel_type TEXT,
            mileage_km REAL, last_maintenance TIMESTAMP,
            next_maintenance_due_km REAL
        );

        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, phone TEXT, license TEXT,
            vehicle_id INTEGER, status TEXT,
            rating REAL, total_deliveries INTEGER,
            current_lat REAL, current_lng REAL
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_type TEXT, recipient_id TEXT,
            title TEXT, message TEXT, type TEXT,
            is_read INTEGER DEFAULT 0, created_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS disruption_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT, type TEXT,
            description TEXT, detected_at TIMESTAMP,
            resolved INTEGER DEFAULT 0, new_eta TIMESTAMP,
            new_route_json TEXT
        );
        """)
