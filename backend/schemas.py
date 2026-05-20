from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date
from enum import Enum


class GradeLevel(str, Enum):
    play_group = "Play Group"
    pp1 = "PP1"
    pp2 = "PP2"
    grade_1 = "Grade 1"
    grade_2 = "Grade 2"
    grade_3 = "Grade 3"
    grade_4 = "Grade 4"
    grade_5 = "Grade 5"
    grade_6 = "Grade 6"


class StudentStatus(str, Enum):
    active = "Active"
    graduated = "Graduated"
    transferred = "Transferred"


class UserRole(str, Enum):
    admin = "admin"
    principal = "principal"
    accountant = "accountant"
    teacher = "teacher"
    secretary = "secretary"


class AssessmentScore(str, Enum):
    ee = "EE"
    me = "ME"
    ae = "AE"
    be = "BE"


class Term(str, Enum):
    term_1 = "Term 1"
    term_2 = "Term 2"
    term_3 = "Term 3"


class PaymentType(str, Enum):
    tuition = "Tuition"
    uniforms = "Uniforms"
    transport = "Transport"
    exam_fees = "Exam Fees"


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    admission_number: str = Field(..., min_length=1, max_length=20)
    grade_level: GradeLevel
    status: StudentStatus = StudentStatus.active


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    grade_level: Optional[GradeLevel] = None
    status: Optional[StudentStatus] = None


class FeeBase(BaseModel):
    student_id: int
    amount: float = Field(..., gt=0, description="Payment amount must be positive")
    payment_type: PaymentType
    term: Term


class FeeCreate(FeeBase):
    pass


class FeeResponse(FeeBase):
    id: int
    payment_date: datetime
    recorded_by: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    student_id: int
    term: Term
    learning_area: str = Field(..., min_length=1, max_length=100)
    score: AssessmentScore
    remarks: Optional[str] = Field(None, max_length=500)


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentResponse(AssessmentBase):
    id: int

    class Config:
        from_attributes = True


class FeeStructureCreate(BaseModel):
    grade_level: GradeLevel
    term: Term
    fee_type: PaymentType
    amount: float = Field(..., gt=0)
    academic_year: int = Field(..., ge=2020, le=2100)


class FeeStructureResponse(FeeStructureCreate):
    id: int

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    student_id: int
    is_present: bool
    remarks: Optional[str] = Field(None, max_length=500)


class AttendanceResponse(AttendanceCreate):
    id: int
    date: date

    class Config:
        from_attributes = True


class PayrollCreate(BaseModel):
    staff_id: int
    payment_month: str = Field(..., pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    basic_salary: float = Field(..., ge=0)
    allowances: float = Field(0.0, ge=0)
    deductions: float = Field(0.0, ge=0)
    net_pay: float = Field(..., ge=0)


class PayrollResponse(PayrollCreate):
    id: int
    recorded_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0)
    category: Optional[str] = Field(None, max_length=100)
    justification: str = Field(..., min_length=1, max_length=500)


class ExpenseResponse(ExpenseCreate):
    id: int
    recorded_by: str
    expense_date: datetime

    class Config:
        from_attributes = True
