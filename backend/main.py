from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Attach the login routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router)
app.include_router(fees.router)
app.include_router(staff.router)
app.include_router(academics.router)
app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Bona School Backend API"}