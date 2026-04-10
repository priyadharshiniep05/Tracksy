from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base
from app.routers import auth, orders, fleet, tracking, alerts, analytics, disruptions, websocket
from app.services.delay_detector import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Start background scheduler
    start_scheduler()
    
    yield
    
    # Shutdown
    stop_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])
app.include_router(fleet.router, prefix=f"{settings.API_V1_STR}/fleet", tags=["fleet"])
app.include_router(tracking.router, prefix=f"{settings.API_V1_STR}/tracking", tags=["tracking"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["alerts"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(disruptions.router, prefix=f"{settings.API_V1_STR}/disruptions", tags=["disruptions"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# Root routes for templates
@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@app.get("/admin/orders")
async def admin_orders(request: Request):
    return templates.TemplateResponse("admin/orders.html", {"request": request})

@app.get("/admin/fleet")
async def admin_fleet(request: Request):
    return templates.TemplateResponse("admin/fleet.html", {"request": request})

@app.get("/admin/analytics")
async def admin_analytics(request: Request):
    return templates.TemplateResponse("admin/analytics.html", {"request": request})

@app.get("/supplier/dashboard")
async def supplier_dashboard(request: Request):
    return templates.TemplateResponse("supplier/dashboard.html", {"request": request})

@app.get("/supplier/new-order")
async def supplier_new_order(request: Request):
    return templates.TemplateResponse("supplier/new_order.html", {"request": request})

@app.get("/track/{tracking_id}")
async def customer_tracking(request: Request, tracking_id: str):
    return templates.TemplateResponse("customer/live.html", {"request": request, "tracking_id": tracking_id})

@app.get("/driver/dashboard")
async def driver_dashboard(request: Request):
    return templates.TemplateResponse("driver/dashboard.html", {"request": request})

@app.get("/driver/navigation")
async def driver_navigation(request: Request):
    return templates.TemplateResponse("driver/navigation.html", {"request": request})
