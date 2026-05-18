from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The Connection String: Tells Python exactly where the database lives
# Format: postgresql://username:password@localhost/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/bona_school_db"

# The Engine: The actual worker that handles the physical connection
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