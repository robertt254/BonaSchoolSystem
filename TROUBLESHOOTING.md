# 🔧 E2E Test Troubleshooting Guide

This guide covers the most common issues you might encounter during testing and how to fix them.

---

## 🚨 Critical Issues

### Issue: Backend Shows 500 Error When Creating Student

**Symptom:**
```
POST /api/students/ - "500 Internal Server Error"
Backend terminal shows: sqlalchemy.exc.IntegrityError
```

**Causes & Solutions:**

#### Cause 1: Duplicate Admission Number
```sql
-- Check database:
SELECT * FROM students WHERE admission_number = 'BONA-100';
-- If it exists, admission number is taken
-- Solution: Use different admission number in Phase 2
```

#### Cause 2: Grade Level Not in System
```python
# In students.py, check your schema allows any string
# But in fees.py, only specific grades have fees:
CBC_TERMLY_FEES = {
    "Play Group": 12000.00,
    "PP1": 15000.00,
    "PP2": 15000.00,
    "Grade 1": 18000.00,
    "Grade 2": 18000.00,  # ← Make sure "Grade 2" is spelled exactly
    ...
}
# Solution: Use exact grade names from CBC_TERMLY_FEES
```

#### Cause 3: Column Constraint Violation
```
Solution: Check models.py for NOT NULL or unique constraints
- Ensure all required fields are provided
- Check for typos in field names
```

**Fix:**
```bash
# Clear and restart database (CAUTION: Loses all data)
1. Delete the database or drop tables
2. Restart backend: python -m uvicorn main:app --reload
3. Try again

# OR: Check logs more carefully
python -m uvicorn main:app --reload
# Look at full error message before the "500"
```

---

### Issue: Frontend Blank Screen During Login

**Symptom:**
```
- Click "Sign In"
- Page goes completely white
- No error message
- Stuck forever
```

**Diagnosis:**
```
Press F12 to open Developer Tools
- Go to "Console" tab
- Look for red error message
- Go to "Network" tab
- Look for failed requests (red status codes)
```

**Common Causes:**

#### Cause 1: Backend Not Running
```
Error in console: "Failed to fetch"
Network shows: No response from localhost:8000

Fix:
1. Check terminal: Is backend terminal still open?
2. Restart: cd backend && python -m uvicorn main:app --reload
3. Refresh browser: Ctrl+F5
```

#### Cause 2: CORS Error
```
Error in console: "Access to XMLHttpRequest from origin..."
Network shows: CORS error or 0 status

Fix in backend/main.py:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # ← Check this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Restart backend after edit.
```

#### Cause 3: Auth Store Error
```
Error in console: "Cannot read property 'split' of null"
Likely in: auth.js when decoding JWT

Check auth store:
- localStorage has 'access_token' key? (Check under Application tab)
- Token format valid? (Should have 3 parts separated by dots)

Fix:
1. Clear localStorage: 
   - Go to Application tab in DevTools
   - Storage → Local Storage → http://localhost:5173
   - Delete all entries
2. Try login again
```

---

### Issue: Teacher Can Still See Finance Menu (RBAC Broken)

**Symptom:**
```
- Login as teacher (mwalimu1)
- Finance, HR, Admin links still visible
- Can navigate to /finance directly
```

**Diagnosis:**

#### Check 1: Token Doesn't Have Role
```javascript
// In browser console, paste this:
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[1]));
console.log(payload.role);
// If it shows nothing or "admin": TOKEN WRONG

Fix in backend/auth.py:
```python
def login(...):
    ...
    to_encode = {
        "sub": user.username,
        "role": user.role,  # ← Make sure this is there
        "exp": expire
    }
    ...
```

Restart backend.
```

#### Check 2: Frontend Not Reading Role
```javascript
// In browser console:
const role = localStorage.getItem('user_role');
console.log(role);
// If it shows "admin" or null: ISSUE

Check auth.js:
```javascript
const assignedRole = decodedPayload.role || determineRoleFromUsername(username)
user.value = { 
    username: decodedPayload.sub, 
    role: assignedRole,  // ← Check this assignment
    name: assignedName 
}
localStorage.setItem('user_role', assignedRole);  // ← Check this save
```

Restart frontend.
```

#### Check 3: Sidebar Not Checking Role
```vue
<!-- In AppLayout.vue or sidebar component:
Look for something like: -->
<template v-if="userRole === 'admin'">
  <!-- Finance link -->
</template>

Make sure every protected menu item has the check.
```

---

### Issue: Attendance Marks But Doesn't Appear in List

**Symptom:**
```
1. Mark Amani as Absent, write "Fever"
2. Click "Submit Roll Call"
3. Green success message appears
4. Refresh page
5. Amani shows as Present again (not Absent)
```

**Causes:**

#### Cause 1: Same-Day Update Issue
```python
# In attendance.py, check the bulk_attendance function:
def log_bulk_attendance(...):
    for record in records:
        existing = db.query(models.Attendance).filter(
            models.Attendance.student_id == record.student_id,
            models.Attendance.date == date.today()  # ← Check this condition
        ).first()
        
        if existing:
            existing.is_present = record.is_present
            existing.remarks = record.remarks
        else:
            new_entry = models.Attendance(**record.model_dump())
            db.add(new_entry)
    
    db.commit()  # ← Make sure this is there!

If date comparison is wrong, it creates duplicates instead of updating.
```

**Fix:**
- Verify the date format matches today's date
- Ensure `db.commit()` is being called
- Check backend logs show no errors

#### Cause 2: Frontend Not Refreshing
```javascript
// After submitting attendance, frontend should:
// Option A: Refetch data automatically
// Option B: Tell user to refresh

Check AttendancePage.vue:
- After submit success, does it refetch?
- Or does user need F5?

This is acceptable either way.
```

---

## 🟡 Non-Critical Issues

### Issue: Fee Statement Math is Off

**Symptom:**
```
Outstanding Balance is wrong or negative
Total Paid doesn't match entered payments
```

**Diagnosis:**

Check the calculation in FeeStatement.vue or backend:
```python
# In fees.py:
CBC_TERMLY_FEES = {
    "Grade 2": 15000.00,  # ← Is this number correct?
}

# Calculation should be:
expected_fee = CBC_TERMLY_FEES[student.grade_level]
total_paid = db.query(func.sum(models.FeePayment.amount)).filter(
    models.FeePayment.student_id == student.id,
    models.FeePayment.term == "Term 1"
).scalar() or 0

outstanding = expected_fee - total_paid
```

**Example Math Check:**
```
Grade 2 Expected: 15,000
Payment 1 (Tuition): 5,000
Payment 2 (Transport): 2,000
Total Paid: 7,000
Outstanding: 15,000 - 7,000 = 8,000 ✓

If you see:
- Outstanding = 8,000 ✓ Correct
- Outstanding = 10,000 ✗ Payment 2 didn't save
- Outstanding = 15,000 ✗ Payments not counted
- Outstanding = -2,000 ✗ Math formula inverted (expected - paid is WRONG)
```

**Fix:**

1. Check CBC_TERMLY_FEES value for the grade
2. Verify payments saved in database:
```sql
SELECT SUM(amount) FROM fees WHERE student_id = [AMANI'S_ID] AND term = 'Term 1';
```
3. Verify formula in backend/frontend

---

### Issue: Print Preview Shows Buttons

**Symptom:**
```
Click "Print" on statement
Print preview appears
But "Print", "Close", "Cancel" buttons still visible
```

**Cause:**
CSS @media print rules not applied correctly

**Fix:**

In FeeStatement.vue or ReportCard.vue, add:
```css
@media print {
  .no-print {
    display: none !important;
  }
  
  .print-content {
    width: 100%;
    padding: 0;
    margin: 0;
  }
}
```

Then add class to buttons:
```vue
<button class="no-print">Print</button>
<button class="no-print">Close</button>

<div class="print-content">
  <!-- Statement content here -->
</div>
```

---

### Issue: Dashboard Shows 0 for Everything

**Symptom:**
```
- Total Students: 0 (but Amani exists)
- Total Revenue: 0 (but paid 7,000)
- Active Staff: 0 (but logged in as admin)
```

**Causes:**

#### Cause 1: Wrong Database Connection
```sql
-- In PostgreSQL, check if data exists:
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM fees;
SELECT COUNT(*) FROM users;

If all return 0: Wrong database or tables empty
```

#### Cause 2: Query Not Filtering Correctly
```python
# In dashboard endpoint, check queries are correct:

# Should be:
students_count = db.query(models.Student).filter(
    models.Student.status == "Active"
).count()

# NOT:
students_count = db.query(models.Student).filter(
    models.Student.status == "Deleted"  # ← Wrong!
).count()
```

#### Cause 3: Frontend Not Displaying Numbers
```javascript
// In DashboardHome.vue:
<div class="stat-card">{{ totalStudents }}</div>

// Check:
1. API returns correct number? (Check Network tab)
2. Variable is updated? (Check Vue dev tools)
3. Template displays it? (Check HTML)

If API returns 1 but displays 0:
- Check data binding
- Check computed properties
- Check watch functions
```

---

### Issue: "Student Not Found" When Recording Fee

**Symptom:**
```
Select student dropdown: Shows "Amani Joy"
Click "Record Payment"
Get error: "Student not found"
```

**Cause:**
Dropdown shows display name but sends wrong ID

**Fix in fees route:**
```python
@router.post("/", response_model=schemas.FeeResponse)
def record_payment(fee: schemas.FeeCreate, ...):
    student = db.query(models.Student).filter(
        models.Student.id == fee.student_id  # ← Check this matches
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
```

**In dropdown component:**
```vue
<!-- In fee form, when selecting student:
Should send ID, not name -->
<select v-model="form.student_id">
  <option :value="student.id">{{ student.first_name }} {{ student.last_name }}</option>
</select>
<!-- ✓ Correct: :value="student.id" -->

<!-- NOT:
<select v-model="form.student_name">
  <option>{{ student.first_name }}</option>
</select>
← Wrong: Sends name not ID
```

---

## 🔍 Debugging Commands

### Check Database Data

```bash
# PostgreSQL PSQL
psql -U postgres -d bona_school_db

# Then run these queries:

-- List all tables
\dt

-- Check students
SELECT id, first_name, admission_number, grade_level FROM students;

-- Check fees
SELECT id, student_id, amount, payment_type, term, payment_date FROM fees;

-- Check attendance
SELECT id, student_id, date, is_present, remarks FROM attendance;

-- Check users
SELECT id, username, role FROM users;

-- Check assessments
SELECT id, student_id, learning_area, score FROM assessments;
```

### Check Backend Logs

```bash
# Terminal running backend:
python -m uvicorn main:app --reload

# Watch for:
# - 400: Bad request (data mismatch)
# - 401: Unauthorized (token issue)
# - 403: Forbidden (RBAC issue)
# - 404: Not found (endpoint or resource missing)
# - 500: Internal error (bug in code)

# Get full traceback:
# It should appear in the terminal, not browser
```

### Check Frontend Console

```javascript
// In browser F12 Console, useful commands:

// Check token
localStorage.getItem('access_token')

// Decode JWT
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[1]));
console.log(payload);

// Check user role
localStorage.getItem('user_role')

// Check API URL
fetch('http://localhost:8000/')
  .then(r => r.json())
  .then(d => console.log(d))

// Clear localStorage
localStorage.clear()
```

---

## 🚀 Recovery Steps

### If Backend Crashes

```bash
# Stop backend (Ctrl+C in terminal)
# Fix the issue
# Restart:
cd backend
python -m uvicorn main:app --reload
```

### If Database is Corrupted

```bash
# Option 1: Drop and recreate (LOSES DATA)
psql -U postgres -c "DROP DATABASE bona_school_db;"
psql -U postgres -c "CREATE DATABASE bona_school_db;"

# Restart backend (it will recreate tables)

# Option 2: Just clear tables (keeps structure)
psql -U postgres -d bona_school_db -c "
  TRUNCATE TABLE assessments;
  TRUNCATE TABLE attendance;
  TRUNCATE TABLE fees;
  TRUNCATE TABLE students;
  TRUNCATE TABLE users;
"
```

### If Frontend Cache is Stale

```bash
# Hard refresh browser:
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Or:
1. F12 to open DevTools
2. Settings (⚙️)
3. Check "Disable cache (while DevTools open)"
4. Refresh
```

### If Something Seems Frozen

```bash
# Try these in order:

1. Refresh browser: F5
2. Hard refresh: Ctrl+Shift+R
3. Clear cache: DevTools → Application → Clear Storage
4. Close browser tab completely
5. Stop backend: Ctrl+C
6. Stop frontend: Ctrl+C
7. Restart both
8. Open fresh browser window
```

---

## 📞 When All Else Fails

### Collect Debug Info

```bash
# 1. Backend error (from terminal):
   Copy the full Python traceback

# 2. Frontend error (from F12 Console):
   Take screenshot of red error message
   Note the exact text

# 3. Network request:
   F12 → Network tab
   Right-click failed request
   Copy as cURL

# 4. Database state:
   SELECT * FROM [table] WHERE [condition];
```

### Common Last-Resort Fixes

1. **Restart everything:**
   - Close browser
   - Stop backend (Ctrl+C)
   - Stop frontend (Ctrl+C)
   - Wait 5 seconds
   - Start backend again
   - Start frontend again
   - Open fresh browser window

2. **Clear all state:**
   - `localStorage.clear()` in browser console
   - Restart browsers
   - Stop and restart both servers

3. **Reset database:**
   ```bash
   # Delete database file (if SQLite):
   rm backend/test.db
   
   # Or drop and recreate (if PostgreSQL):
   dropdb bona_school_db
   createdb bona_school_db
   
   # Restart backend
   ```

4. **Update dependencies:**
   ```bash
   cd backend
   pip install --upgrade -r requirements.txt
   
   cd ../frontend
   npm install
   ```

---

## ✅ Validation Checklist

Before declaring an issue "fixed":

- [ ] No red errors in browser console (F12)
- [ ] No 5xx errors in backend terminal
- [ ] No frozen/loading spinners
- [ ] Action completed and data saved
- [ ] Refresh browser shows persistent data
- [ ] No "Cannot read property X of undefined"
- [ ] Role-based access respected
- [ ] Math/calculations are correct

---

**If you're still stuck, review the [E2E_TEST_EXECUTION_GUIDE.md](E2E_TEST_EXECUTION_GUIDE.md) and try the exact steps there. 🚀**
