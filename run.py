import eventlet
eventlet.monkey_patch()

from database import init_db
from seed_data import seed_if_empty
from app import app, socketio

if __name__ == '__main__':
    with app.app_context():
        init_db()
        seed_if_empty()
    print("🚀 Tracksy starting on http://localhost:5000")
    print("📦 Admin:    http://localhost:5000/admin/dashboard")
    print("🏭 Supplier: http://localhost:5000/supplier/dashboard")
    print("📍 Customer: http://localhost:5000/customer/track")
    print("🚛 Driver:   http://localhost:5000/driver/dashboard")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
