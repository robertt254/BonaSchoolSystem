import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# The Connection String: Tells Python exactly where the database lives
# Format: postgresql://username:password@localhost/database_name
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# The Engine: The actual worker that handles the physical connection
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# The Session: What we use to actually talk to the database (add rows, delete rows)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The Base: All our future database models (like User or Student) will inherit from this
Base = declarative_base()

# A helper function to safely open and close database connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
