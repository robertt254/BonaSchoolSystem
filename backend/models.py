from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), index=True, nullable=False)
    admission_number = Column(String(20), unique=True, index=True, nullable=False)
    grade_level = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="Active")
    # Soft delete — never hard-delete student records
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class FeePayment(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    # Numeric(10, 2) avoids floating-point rounding errors for currency
    amount = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(String(50), nullable=False)
    term = Column(String(10), nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_by = Column(String(100), nullable=False)
    # Sequential receipt number — format BNS-{YEAR}-{seq:05d}
    receipt_number = Column(String(20), unique=True, nullable=True, index=True)


class FeeStructure(Base):
    """Configurable per-grade/per-term fee schedule. Replaces hardcoded dictionary in fees.py."""
    __tablename__ = "fee_structure"

    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(20), nullable=False)
    term = Column(String(10), nullable=False)
    fee_type = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    academic_year = Column(Integer, nullable=False)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    term = Column(String(10), nullable=False)
    learning_area = Column(String(100), nullable=False)
    score = Column(String(5), nullable=False)
    remarks = Column(String(500), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, server_default=func.current_date(), nullable=False)
    is_present = Column(Boolean, default=True, nullable=False)
    remarks = Column(String(500), nullable=True)


class AuditLog(Base):
    """Immutable record of every create/update/delete action in the system."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(10), nullable=False)       # CREATE | UPDATE | DELETE
    resource = Column(String(50), nullable=False)     # student | fee | assessment | attendance | staff
    resource_id = Column(Integer, nullable=True)
    detail = Column(String(2000), nullable=True)      # JSON string for extra context
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
