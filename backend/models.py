from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Date, Boolean, Text
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
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    guardian_name = Column(String(100), nullable=True)
    guardian_phone = Column(String(20), nullable=True)
    guardian2_name = Column(String(100), nullable=True)
    guardian2_phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    previous_school = Column(String(200), nullable=True)
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


class Payroll(Base):
    """Monthly salary disbursement record per staff member."""
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    payment_month = Column(String(7), nullable=False)          # YYYY-MM
    basic_salary = Column(Numeric(10, 2), nullable=False)
    allowances = Column(Numeric(10, 2), nullable=False, server_default="0")
    deductions = Column(Numeric(10, 2), nullable=False, server_default="0")
    net_pay = Column(Numeric(10, 2), nullable=False)
    recorded_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Expense(Base):
    """School operational expense record."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=True)
    justification = Column(String(500), nullable=False)
    recorded_by = Column(String(100), nullable=False)
    expense_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class Timetable(Base):
    """Weekly class schedule entry per grade."""
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(20), nullable=False, index=True)
    day_of_week = Column(String(10), nullable=False)
    period = Column(Integer, nullable=False)
    subject = Column(String(100), nullable=False)
    teacher_name = Column(String(100), nullable=True)
    start_time = Column(String(5), nullable=True)
    end_time = Column(String(5), nullable=True)
    term = Column(String(10), nullable=False)
    academic_year = Column(Integer, nullable=False)
    created_by = Column(String(100), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class LeaveRequest(Base):
    """Staff leave application and approval record."""
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
