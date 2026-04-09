from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Import and register blueprints
from routes.admin import admin_bp
from routes.supplier import supplier_bp
from routes.customer import customer_bp
from routes.driver import driver_bp
from routes.api import api_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(supplier_bp, url_prefix='/supplier')
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(driver_bp, url_prefix='/driver')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

def background_tasks():
    """Background simulator thread for advancing routes and checking delays."""
    import eventlet
    from services.ai_engine import check_for_delays, advance_vehicles
    while True:
        eventlet.sleep(15)
        try:
            with app.app_context():
                advance_vehicles(socketio)
                check_for_delays(socketio)
        except Exception as e:
            print(f"[Simulation Error] {e}")

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

# Start background simulation
socketio.start_background_task(background_tasks)
