import os
import sys
import subprocess
import time
import webbrowser
import asyncio
from pathlib import Path

# --- TRACKSY STARTUP BANNER ---
BANNER = """
\033[96m╔══════════════════════════════════════════════════════════════╗
║\033[0m   \033[92m🚚 TRACKSY — AI-Powered Logistics Optimization System\033[0m      \033[96m║
║\033[0m   \033[94mURL: http://localhost:8000\033[0m                                 \033[96m║
║\033[0m   \033[93mCredentials:\033[0m admin@tracksy.io / tracksy2024                \033[96m║
╚══════════════════════════════════════════════════════════════╝\033[0m
"""

def check_python_version():
    if sys.version_info < (3, 11):
        print("\033[91mError: Tracksy requires Python 3.11 or higher.\033[0m")
        sys.exit(1)

def ensure_db_exists():
    db_path = Path("tracksy.db")
    if not db_path.exists():
        print("\033[93mFirst run detected. Initializing database and seeding data...\033[0m")
        # Run seed.py synchronously
        try:
            from app.seed import seed_data
            asyncio.run(seed_data())
            print("\033[92mDatabase initialized and seeded successfully!\033[0m")
        except Exception as e:
            print(f"\033[91mError seeding database: {e}\033[0m")
            sys.exit(1)

def open_browser():
    time.sleep(2)  # Give uvicorn a moment to start
    webbrowser.open("http://localhost:8000/login")

def start_server():
    print(BANNER)
    
    # Open browser in a separate thread/process
    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Uvicorn
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
        log_level="info"
    )

if __name__ == "__main__":
    check_python_version()
    
    # Ensure .env exists
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("\033[93mCreating .env from .env.example...\033[0m")
            with open(".env.example", "r") as f_in, open(".env", "w") as f_out:
                f_out.write(f_in.read())
    
    # We need to make sure 'app' is in the path
    sys.path.append(os.getcwd())
    
    ensure_db_exists()
    start_server()
