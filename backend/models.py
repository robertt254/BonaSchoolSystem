from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    # The columns for our database table
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    role = Column(String)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    admission_number = Column(String, unique=True, index=True)
    grade_level = Column(String)
    status = Column(String, default="Active")  # Active, Graduated, Transferred


class FeePayment(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    # The Foreign Key: This links directly to the 'id' column in the 'students' table
    student_id = Column(Integer, ForeignKey("students.id"))
    
    amount = Column(Float)
    payment_type = Column(String)  # e.g., Tuition, Uniforms, Transport
    term = Column(String)  # e.g., "Term 1", "Term 2", "Term 3"
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    recorded_by = Column(String)  # To track which accountant logged it


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    term = Column(String)  # "Term 1", "Term 2", "Term 3"
    learning_area = Column(String)  # e.g., "Mathematics Activities", "Language Activities"
    score = Column(String)  # "EE", "ME", "AE", "BE"
    remarks = Column(String)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date, server_default=func.current_date())
    is_present = Column(Boolean, default=True)
    remarks = Column(String, nullable=True)
