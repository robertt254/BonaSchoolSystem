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
import finance
from database import engine

# Tell SQLAlchemy to build all our tables in the database
models.Base.metadata.create_all(bind=engine)

# Automatic schema migrations for existing SQLite/PostgreSQL databases
def apply_migrations():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            # Check if using SQLite (which doesn't support ADD COLUMN IF NOT EXISTS easily)
            # or PostgreSQL. The error usually comes from PostgreSQL on Render.
            if engine.url.drivername.startswith("postgresql"):
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS kra_pin VARCHAR;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS nssf_number VARCHAR;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS nhif_number VARCHAR;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS job_title VARCHAR;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS date_of_hire DATE;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS contract_type VARCHAR;'))
                conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS accrued_leave_days INTEGER DEFAULT 0;'))
            elif engine.url.drivername.startswith("sqlite"):
                # SQLite workaround: check columns first
                cursor = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in cursor.fetchall()]

                if "kra_pin" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN kra_pin VARCHAR;'))
                if "nssf_number" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN nssf_number VARCHAR;'))
                if "nhif_number" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN nhif_number VARCHAR;'))
                if "job_title" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN job_title VARCHAR;'))
                if "date_of_hire" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN date_of_hire DATE;'))
                if "contract_type" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN contract_type VARCHAR;'))
                if "accrued_leave_days" not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN accrued_leave_days INTEGER DEFAULT 0;'))
            conn.commit()
    except Exception as e:
        print("Migration warning:", e)

# Run migrations before seeding
apply_migrations()

# Function to seed initial users into the database
def seed_users():
    from database import SessionLocal
    from auth import pwd_context
    db = SessionLocal()
    try:
        users_to_seed = [
            {"username": "admin", "password": "password", "name": "System Admin", "role": "admin"},
            {"username": "principal", "password": "password", "name": "School Principal", "role": "principal"},
            {"username": "teacher", "password": "password", "name": "Class Teacher", "role": "senior_teacher"},
            {"username": "finance", "password": "password", "name": "Finance Officer", "role": "finance"},
            {"username": "secretary", "password": "password", "name": "School Secretary", "role": "secretary"},
        ]

        for u in users_to_seed:
            existing = db.query(models.User).filter(models.User.username == u["username"]).first()
            if not existing:
                new_user = models.User(
                    username=u["username"],
                    name=u["name"],
                    role=u["role"],
                    hashed_password=pwd_context.hash(u["password"])
                )
                db.add(new_user)
        db.commit()
    finally:
        db.close()

# Seed users on startup
seed_users()

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
app.include_router(finance.router)

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