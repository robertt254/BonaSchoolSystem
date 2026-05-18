# 🎓 Bona School Management System

A comprehensive full-stack web application for managing primary school operations, including student admissions, attendance tracking, financial management, and academic assessment.

## 🌟 Features

- **Authentication & Authorization**: JWT-based role-based access control (Admin, Teacher, Accountant, Principal)
- **Student Management**: Admissions, student records, and enrollment tracking
- **Attendance Tracking**: Daily attendance marking by grade
- **Financial Management**: Fee collection, payment recording, and financial statements
- **Academic Grading**: CBC curriculum grading system with report card generation
- **Dashboard Analytics**: Real-time statistics and financial reporting
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **API**: RESTful endpoints with CORS support

### Frontend
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **State Management**: Pinia
- **Styling**: Tailwind CSS
- **UI Components**: Custom Vue components

### Database
- PostgreSQL with foreign key relationships
- Models: User, Student, FeePayment, Attendance, Assessment

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- pip and npm package managers

## 🚀 Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Configure database URL

# Run migrations (if using Alembic)
# python -m alembic upgrade head

# Start backend server
python -m uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start development server
npm run dev
```

Frontend runs on: `http://localhost:5173`

## 💾 Database Setup

### PostgreSQL Configuration

```bash
# Create database
createdb bona_school_db

# Optional: Create user with password
createuser -P bona_user
```

Update `backend/.env`:
```
DATABASE_URL=postgresql://bona_user:password@localhost/bona_school_db
```

## 📖 Usage

### Phase 1: Security & Authentication
1. Test route guards (unauthenticated users redirected to login)
2. Admin login with credentials
3. Verify role-based menu visibility
4. Create new staff members (teachers, accountants)

### Phase 2: Student Admissions
1. Navigate to Student Directory
2. Add new students with admission numbers
3. Verify duplicate prevention

### Phase 3: Teacher Attendance
1. Login as teacher
2. Load students by grade
3. Mark daily attendance with remarks

### Phase 4: Financial Management
1. Record fee payments (tuition, transport, etc.)
2. Generate fee statements with calculations
3. Verify mathematical accuracy of balances

### Phase 5: Academic Grading
1. Select grade, term, and learning area
2. Assign CBC scores (EE, ME, AE, BE)
3. Generate student report cards

### Phase 6: Dashboard Analytics
1. View total students, revenue, and staff counts
2. Verify calculation accuracy
3. Test responsive design

## 🧪 Testing

### End-to-End Testing

Follow the comprehensive E2E test guide:

```bash
# Start backend
cd backend
python -m uvicorn main:app --reload

# In another terminal, start frontend
cd frontend
npm run dev

# Open browser to http://localhost:5173
# Follow E2E_TEST_EXECUTION_GUIDE.md for 6-phase test
```

### System Status Check

```bash
cd c:\Users\user\BonaSchoolSystem
python check_system_status.py
```

Verifies:
- Backend running on localhost:8000
- Frontend running on localhost:5173
- Database connection
- Admin user exists
- CORS configured

### Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to:
- Backend 500 errors
- Frontend blank screens
- RBAC not enforcing
- Database issues
- Math calculation errors

## 📁 Project Structure

```
BonaSchoolSystem/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Database connection
│   ├── auth.py              # Authentication endpoints
│   ├── students.py          # Student CRUD operations
│   ├── fees.py              # Financial management
│   ├── attendance.py        # Attendance tracking
│   ├── academics.py         # Grading and assessments
│   ├── staff.py             # Staff management
│   ├── requirements.txt     # Python dependencies
│   └── update_passwords.py  # Admin setup script
│
├── frontend/
│   ├── index.html           # Entry HTML
│   ├── src/
│   │   ├── main.js          # App entry point
│   │   ├── App.vue          # Root component
│   │   ├── router/index.js  # Route definitions
│   │   ├── stores/          # Pinia stores (auth, etc.)
│   │   ├── services/        # API service modules
│   │   ├── views/           # Page components
│   │   ├── components/      # Reusable components
│   │   └── assets/          # Styles and images
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── tailwind.config.js   # Tailwind CSS config
│
├── E2E_TEST_EXECUTION_GUIDE.md   # Step-by-step testing guide
├── TROUBLESHOOTING.md             # Common issues & fixes
├── check_system_status.py         # System validation script
└── README.md                       # This file
```

## 🔐 Security Features

- JWT token-based authentication with 120-minute expiry
- Password hashing with PBKDF2-SHA256
- Role-based access control (RBAC) enforced at both frontend and backend
- CORS configured for development
- SQL injection prevention via ORM
- Foreign key constraints for data integrity

## 📊 Database Schema

### Users Table
- id, username (unique), hashed_password, name, role

### Students Table
- id, first_name, last_name, admission_number (unique), grade_level, status

### Fees Table
- id, student_id (FK), amount, payment_type, term, payment_date, recorded_by

### Attendance Table
- id, student_id (FK), date, is_present, remarks

### Assessments Table
- id, student_id (FK), term, learning_area, score, remarks

## 🎯 CBC Grading Scale

- **EE** - Exceeding Expectations
- **ME** - Meeting Expectations
- **AE** - Approaching Expectations
- **BE** - Below Expectations

## 💰 Fee Structure

Standard CBC termly fees by grade:
- Play Group: 12,000 Ksh
- PP1-PP2: 15,000 Ksh
- Grade 1-6: 18,000-22,000 Ksh

## 📝 API Endpoints

### Authentication
- `POST /api/auth/login` - User login

### Students
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Fees
- `GET /api/fees/` - List payments
- `POST /api/fees/` - Record payment
- `GET /api/fees/statement/{student_id}` - Fee statement

### Attendance
- `GET /api/attendance/today/{grade}` - Today's attendance
- `POST /api/attendance/bulk` - Mark bulk attendance

### Academics
- `POST /api/academics/assessments` - Submit grades
- `GET /api/academics/reportcard/{student_id}` - Generate report card

### Staff
- `GET /api/staff/` - List staff
- `POST /api/staff/` - Create staff
- `DELETE /api/staff/{id}` - Remove staff

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

For issues, questions, or suggestions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [E2E_TEST_EXECUTION_GUIDE.md](E2E_TEST_EXECUTION_GUIDE.md)
3. Open an issue on GitHub

## 👨‍💻 Author

Developed for Bona School management needs.

---

**Status**: ✅ Market-ready (all 6 E2E test phases passing)
