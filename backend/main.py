from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import auth
import models
import students
import fees
import staff
import academics
import attendance
from database import engine

# Tell SQLAlchemy to build all our tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bona School Management API")

# Crucial: This allows your Vite frontend to talk to this Python backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# Attach the API routes.
# NOTE: The routers themselves already define their prefixes (e.g. prefix="/api/students")
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router)
app.include_router(fees.router)
app.include_router(staff.router)
app.include_router(academics.router)
app.include_router(attendance.router)

# Serve static files from the built Vue app
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    # Fallback to index.html for Vue Router history mode
    @app.get("/{full_path:path}")
    async def serve_vue_app(full_path: str):
        # Ignore API routes (FastAPI routing handles actual API requests before this catch-all)
        # We should NOT blindly return 200 here, let FastAPI handle 404s if they start with api/
        # but wait, since this is a catch-all route, it handles EVERYTHING.
        # Actually, FastAPI evaluates routes in the order they are defined.
        # Since this catch-all is defined AFTER the app.include_router calls,
        # API requests will be matched by the routers first.
        # But if an API route is NOT found, it will fall through to here.
        if full_path.startswith("api/") or full_path.startswith("api"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API Route Not Found")

        # Try to serve a specific file if it exists
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise, serve index.html for Vue Router to handle
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"status": "online", "system": "Bona School Backend API (Static files not found)"}