from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# Base properties shared by all student interactions
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    admission_number: str
    grade_level: str
    status: str = "Active"


# Used when creating a student (Vue sending data TO FastAPI)
class StudentCreate(StudentBase):
    pass


# Used when reading a student (FastAPI sending data TO Vue)
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True  # Tells Pydantic to read SQLAlchemy models


# Used when updating a student (partial updates allowed)
class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    grade_level: Optional[str] = None
    status: Optional[str] = None


# Fee Payment Schemas
class FeeBase(BaseModel):
    student_id: int
    amount: float
    payment_type: str
    term: str  # e.g., "Term 1", "Term 2", "Term 3"


class FeeCreate(FeeBase):
    pass


class FeeResponse(FeeBase):
    id: int
    payment_date: datetime
    recorded_by: str

    class Config:
        from_attributes = True


# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict


# --- HR & STAFF SCHEMAS ---
class UserBase(BaseModel):
    username: str
    name: str
    role: str  # admin, principal, finance, teacher
    kra_pin: Optional[str] = None
    nssf_number: Optional[str] = None
    nhif_number: Optional[str] = None
    job_title: Optional[str] = None
    date_of_hire: Optional[date] = None
    contract_type: Optional[str] = None
    accrued_leave_days: int = 0


class UserCreate(UserBase):
    password: str  # Required when creating a new employee


class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None  # Optional when editing
    kra_pin: Optional[str] = None
    nssf_number: Optional[str] = None
    nhif_number: Optional[str] = None
    job_title: Optional[str] = None
    date_of_hire: Optional[date] = None
    contract_type: Optional[str] = None
    accrued_leave_days: Optional[int] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# --- PAYROLL SCHEMAS ---
class PayrollBase(BaseModel):
    staff_id: int
    basic_salary: float
    allowances: float
    deductions: float
    net_pay: float
    payment_month: str


class PayrollCreate(PayrollBase):
    pass


class PayrollResponse(PayrollBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- ACADEMICS & CBC SCHEMAS ---
class AssessmentBase(BaseModel):
    student_id: int
    term: str
    learning_area: str
    score: str
    remarks: Optional[str] = None


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentResponse(AssessmentBase):
    id: int

    class Config:
        from_attributes = True


# --- ATTENDANCE SCHEMAS ---
class AttendanceCreate(BaseModel):
    student_id: int
    is_present: bool
    remarks: Optional[str] = None


class AttendanceResponse(AttendanceCreate):
    id: int
    date: date

    class Config:
        from_attributes = True

class StudentProfile(BaseModel):
    student: StudentResponse
    attendance_percentage: float
    assessments: list[AssessmentResponse]
    fee_balance: float
