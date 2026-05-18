# 🧪 Bona School E2E System Test - Execution Guide

## ✅ Pre-Test Checklist

Before starting, ensure:
- [ ] Backend is running: `python -m uvicorn main:app --reload`
- [ ] Frontend is running: `npm run dev`
- [ ] Database (PostgreSQL) is running and accessible
- [ ] Fresh incognito browser window ready
- [ ] Admin account exists with credentials
- [ ] You have a teacher account (or will create one in Phase 1)
- [ ] You have accountant account (or will use admin)
- [ ] Terminal windows visible to monitor for errors

---

## 🔐 Phase 1: Security & System Administration (The Bouncer Test)

**Duration:** ~10 minutes
**Critical Path:** Auth Guard → Admin Login → Layout Check → HR Creation → Self-Delete Prevention

### Test 1.1: The Guard Test (JWT Route Protection)
**Objective:** Verify unauthenticated users are blocked from protected routes

```
ACTION:
1. Open fresh incognito browser window
2. Navigate to: http://localhost:5173/finance

EXPECTED RESULT:
✓ Immediately redirect to login page
✓ URL changes to http://localhost:5173/login
✓ No loading of Finance Dashboard

CHECK:
- Browser console (F12) for any errors
- Network tab shows 403 or redirect response
```

**If test fails:**
- ❌ White screen: Check backend terminal for errors
- ❌ Finance page loads: Router guard not working (check beforeEach in router/index.js)
- ❌ No redirect: localStorage or token not being checked

### Test 1.2: Admin Login
```
ACTION:
1. You should already be on login page
2. Enter Admin credentials:
   - Username: [your-admin-username]
   - Password: [your-admin-password]
3. Click "Sign In"

EXPECTED RESULT:
✓ Redirect to Dashboard homepage
✓ URL is http://localhost:5173/
✓ User name appears in header/navbar

CHECK:
- Backend terminal: Should see POST /api/auth/login with 200 status
- Network tab: Response contains access_token
- Console: No JWT decode errors
```

**If test fails:**
- ❌ "Invalid username or password": Check database for admin user
- ❌ Blank page: Check browser console for fetch errors
- ❌ 401 error: Verify credentials in database

### Test 1.3: The Layout Test (Role-Based Menu)
```
ACTION:
1. Look at left sidebar navigation menu
2. Count visible menu items

EXPECTED RESULT (Admin sees all):
✓ Dashboard
✓ Administration (Admin Dashboard)
✓ Student Directory (Staff)
✓ Roll Call (Academics/Attendance)
✓ Grading (Academics)
✓ Finance (Accountant section)
✓ Statements (Fee reports)
✓ HR (Staff management)

CHECK:
- No menu items hidden or grayed out
- All icons display properly
- Sidebar expands/collapses smoothly
```

**If test fails:**
- ❌ Menu items missing: Check AppLayout.vue for role-based conditionals
- ❌ Menu won't open: Check sidebar component for JavaScript errors

### Test 1.4: HR Creation (Create New Teacher Account)
```
ACTION:
1. Click "Administration" in sidebar → "Staff & HR"
   OR click menu: "System" → "Staff & HR"
2. Click "+ Hire New Staff" button
3. Fill in form:
   - Name: [e.g., "Jane Mwalimu"]
   - Username: mwalimu1
   - Password: password123
   - Role: Teacher
   - Email: mwalimu1@bona.school
4. Click "Save Staff Member"

EXPECTED RESULT:
✓ Green success toast/alert
✓ New teacher appears in staff list
✓ New teacher can log in with these credentials

CHECK:
- Backend terminal: POST /api/staff with 200 status
- Staff list updates without page reload
- Console: No errors during submission
```

**Database Verification:**
```sql
-- Verify in PostgreSQL:
SELECT username, role FROM users WHERE username = 'mwalimu1';
-- Should return: mwalimu1 | teacher
```

**If test fails:**
- ❌ Form won't submit: Check form validation (required fields)
- ❌ "Username already exists": Try different username
- ❌ 500 error: Check backend terminal for database error

### Test 1.5: The Safety Check (Self-Delete Prevention)
```
ACTION:
1. Still in HR section, find your Admin account in the list
2. Look for "Revoke Access" or "Delete" button on your Admin row
3. Click it

EXPECTED RESULT:
✓ Red error message/alert appears
✓ Error text: "Cannot revoke your own admin access"
   OR "Cannot delete your own account"
   OR similar
✓ Admin account remains in list, unchanged

CHECK:
- Error appears immediately (not after page reload)
- Console: Check for any JavaScript errors
- Backend terminal: Should see 403 Forbidden response
```

**If test fails:**
- ❌ Button does nothing: Check onClick handler in staff.py
- ❌ Account gets deleted: Critical security bug! Check authorization logic
- ❌ Different error message: Still good if it prevents deletion

**🟢 Phase 1 Complete if:**
- ✓ Guard prevented access to /finance
- ✓ Admin login worked with real credentials
- ✓ All menu items visible for admin role
- ✓ Created new teacher account successfully
- ✓ Cannot delete own admin account

---

## 👥 Phase 2: Admissions (The Database Test)

**Duration:** ~8 minutes
**Critical Path:** Add Student → Verify in DB → Duplicate Prevention

### Test 2.1: Navigate to Student Directory
```
ACTION:
1. From sidebar, click "Administration" → "Student Directory"
   OR click menu: "System" → "Student Directory"
2. You should see a list of existing students (if any)

EXPECTED RESULT:
✓ Student Directory page loads
✓ Table with columns: Name, Admission #, Grade, Status
✓ "+Add New Student" button visible
```

### Test 2.2: Add New Student
```
ACTION:
1. Click "+ Add New Student" button
2. Fill form:
   - First Name: Amani
   - Last Name: Joy
   - Admission Number: BONA-100
   - Grade Level: Grade 2
   - Status: Active
3. Click "Save Student"

EXPECTED RESULT:
✓ Green success message
✓ Student "Amani Joy" appears in table
✓ Admission Number shows as "BONA-100"
✓ Grade shows as "Grade 2"

CHECK:
- Backend terminal: POST /api/students/ with 201 status
- Network tab: Response includes student ID
- Console: No validation errors
```

**Database Verification:**
```sql
-- Verify in PostgreSQL:
SELECT id, first_name, last_name, admission_number, grade_level FROM students 
WHERE admission_number = 'BONA-100';
```

**If test fails:**
- ❌ Form validation error: Check required fields
- ❌ 400 Bad Request: Check data format matches schema
- ❌ Student doesn't appear: Check network response for actual saved ID

### Test 2.3: The Duplicate Test (Admission Number Uniqueness)
```
ACTION:
1. Click "+ Add New Student" again
2. Fill form:
   - First Name: TestDuplicate
   - Last Name: Student
   - Admission Number: BONA-100  (SAME AS ABOVE)
   - Grade Level: Grade 3
3. Click "Save Student"

EXPECTED RESULT:
✓ Red error message appears
✓ Error text includes: "Admission number already exists"
   OR "Duplicate admission number"
   OR "BONA-100 already registered"
✓ Student is NOT added to table
✓ User remains on form (not redirected)

CHECK:
- Backend terminal: POST /api/students/ with 400 or 409 status
- Console: Error message is readable
- Network tab: Response contains error detail
```

**If test fails:**
- ❌ No error message: Backend not validating uniqueness
- ❌ Duplicate student added: DATABASE CONSTRAINT FAILED
- ❌ 500 error: Check backend terminal, likely unique constraint violation

**Database Verification:**
```sql
-- Check unique constraint:
SELECT COUNT(*) FROM students WHERE admission_number = 'BONA-100';
-- Should return: 1 (only one Amani Joy)
```

**🟢 Phase 2 Complete if:**
- ✓ Added Amani Joy with admission BONA-100
- ✓ Duplicate rejection with clear error message
- ✓ Database has exactly one student with BONA-100

---

## 👨‍🏫 Phase 3: The Teacher's Morning (RBAC & Attendance)

**Duration:** ~12 minutes
**Critical Path:** Role Switch → RBAC Check → Load Students → Mark Attendance

### Test 3.1: Role Switch (Logout & Login as Teacher)
```
ACTION:
1. Click user profile icon or logout button (top right)
2. Click "Logout"
3. You should be back on Login page
4. Enter Teacher credentials:
   - Username: mwalimu1
   - Password: password123
5. Click "Sign In"

EXPECTED RESULT:
✓ Redirect to Dashboard
✓ Teacher view loads (different from Admin)
✓ Header shows "mwalimu1" or "Jane Mwalimu"
✓ No console errors

CHECK:
- Backend terminal: POST /api/auth/login with 200
- New access_token saved to localStorage
- Network tab: Token is different from previous login
```

**If test fails:**
- ❌ Login fails: Verify teacher account was created in Phase 1
- ❌ Dashboard is empty/white: Check browser console for errors
- ❌ Still shows admin menu: Token not updated, try hard refresh (Ctrl+F5)

### Test 3.2: The RBAC Test (Role-Based Menu)
```
ACTION:
1. Look at left sidebar menu as logged-in teacher
2. Compare with admin menu from Phase 1

EXPECTED RESULT (Teacher sees LIMITED menu):
✓ Dashboard (should be there)
✓ Academics (Roll Call, Grading)
✓ MISSING: Finance, Statements, HR, Administration
✓ Grayed out or hidden sections

TEACHER SHOULD NOT SEE:
❌ Finance
❌ Fee Statements
❌ Staff/HR
❌ Admin Dashboard

CHECK:
- Role in browser: localStorage.user_role should be "teacher"
- Sidebar: Use AppLayout.vue role checks
- Try typing /finance directly: Should redirect or show 403
```

**Navigation Test:**
```
ACTION:
1. Try to manually navigate to: http://localhost:5173/finance

EXPECTED RESULT:
✓ Redirect back to /dashboard
  OR show "Access Denied" message
  OR stay on current page
```

**If test fails:**
- ❌ Finance page loads: RBAC not enforced properly
- ❌ Menu items visible: Check conditional rendering in sidebar
- ❌ Can access /finance route: Backend or router guard needs update

### Test 3.3: Load Students for Grade 2
```
ACTION:
1. Click "Academics" → "Roll Call"
   OR use sidebar: "Academics" → "Roll Call"
2. Look for Grade selector dropdown
3. Select "Grade 2"
4. Click "Load Students" button

EXPECTED RESULT:
✓ Loading spinner appears briefly
✓ Student list appears with:
  - Amani Joy (BONA-100)
  - Any other Grade 2 students
✓ Each row has a checkbox or "Present/Absent" toggle
✓ A "Remarks" text field per student

CHECK:
- Backend terminal: GET /api/attendance/today/Grade%202 with 200
- Console: No fetch errors
- Network tab: Student data returned as JSON array
```

**If test fails:**
- ❌ No students load: Check backend for grade filtering
- ❌ Wrong grade's students: Backend filtering issue
- ❌ 500 error: Check terminal for query error

### Test 3.4: Mark Attendance
```
ACTION:
1. Find "Amani Joy" row in the loaded students
2. Mark attendance:
   - Checkbox/Toggle: Set to "ABSENT"
   - Remarks field: Type "Fever"
3. Look for other students, mark a few as "PRESENT"
4. Click "Submit Roll Call" or "Save Attendance"

EXPECTED RESULT:
✓ Green success message appears
✓ Message: "Attendance recorded successfully" or similar
✓ Amani's record shows:
  - Status: Absent
  - Remarks: Fever
  - Date: Today's date

CHECK:
- Backend terminal: POST /api/attendance/bulk with 200
- Console: No errors during submit
- Network tab: Request includes all marked students
```

**Database Verification:**
```sql
-- Verify in PostgreSQL:
SELECT student_id, date, is_present, remarks FROM attendance 
WHERE date = TODAY() 
ORDER BY date DESC LIMIT 5;

-- Should show:
-- [Amani's ID] | 2026-05-18 | false | Fever
```

**If test fails:**
- ❌ "Submit" button does nothing: Check form submission in AttendancePage.vue
- ❌ 400/422 error: Check request payload format
- ❌ 500 error: Check terminal for database constraint issue

**🟢 Phase 3 Complete if:**
- ✓ Teacher account logged in successfully
- ✓ Finance/HR/Admin hidden from teacher menu
- ✓ Grade 2 students loaded correctly
- ✓ Attendance marked with remarks saved to DB

---

## 💰 Phase 4: The Financial Engine (Math & Foreign Keys)

**Duration:** ~15 minutes
**Critical Path:** Record Payments → Verify Foreign Keys → Generate Statement → Verify Math

### Test 4.1: Role Switch to Accountant
```
ACTION:
1. Logout (top right)
2. Login with:
   - Username: [accountant-username] OR use admin
   - Password: [accountant-password]
3. Dashboard should load

EXPECTED RESULT:
✓ Finance menu visible
✓ Fee Ledger option available
```

### Test 4.2: Record Payment 1 (Tuition)
```
ACTION:
1. Click "Finance" → "Fee Ledger"
   OR menu: "Finance" → "Fee Ledger"
2. Click "+ Record Payment"
3. Fill form:
   - Student: "Amani Joy" (select from dropdown)
   - Payment Category: "Tuition"
   - Term: "Term 1"
   - Amount: 5000
   - Payment Date: Today
4. Click "Save Payment"

EXPECTED RESULT:
✓ Green success message
✓ Payment appears in Fee Ledger table with:
  - Student: Amani Joy
  - Category: Tuition
  - Amount: 5,000
  - Date: Today
  - Recorded By: [accountant name]

CHECK:
- Backend terminal: POST /api/fees/ with 200/201
- Network tab: Response includes payment ID
- Console: No errors
```

**Database Verification:**
```sql
-- Check foreign key and payment record:
SELECT fee_id, student_id, amount, payment_type, term, payment_date
FROM fees 
WHERE student_id IN (SELECT id FROM students WHERE admission_number = 'BONA-100');

-- Should show:
-- [ID] | [Amani's ID] | 5000.00 | Tuition | Term 1 | 2026-05-18
```

**If test fails:**
- ❌ Student dropdown empty: Students not loaded in fee form
- ❌ "Student not found" error: Foreign key issue, check student_id
- ❌ Amount shows as 0: Form parsing issue
- ❌ 400 error: Schema mismatch, check payment_type values

### Test 4.3: Record Payment 2 (Transport)
```
ACTION:
1. Click "+ Record Payment" again
2. Fill form:
   - Student: "Amani Joy"
   - Payment Category: "Transport"
   - Term: "Term 1"
   - Amount: 2000
3. Click "Save Payment"

EXPECTED RESULT:
✓ Green success message
✓ Both payments now show in ledger:
  - Payment 1: Tuition, 5,000
  - Payment 2: Transport, 2,000
✓ Total for Amani: 7,000

CHECK:
- Fee Ledger table shows both rows
- No duplication
- Dates are correct
```

### Test 4.4: Generate Fee Statement
```
ACTION:
1. Click "Finance" → "Statements"
   OR menu: "Finance" → "Fee Statements"
2. Select student dropdown: "Amani Joy"
3. Select term: "Term 1"
4. Click "Generate Report" or "View Statement"

EXPECTED RESULT (on printable statement):
✓ Header with school name and logo
✓ Student details:
  - Name: Amani Joy
  - Admission: BONA-100
  - Grade: Grade 2
  - Term: Term 1

✓ Fee Breakdown shows:
  - Expected Fee for Grade 2: [CBC standard amount, likely 15,000]
  - Payments:
    * Tuition: 5,000
    * Transport: 2,000
  - Total Paid: 7,000
  - Outstanding Balance: [15,000 - 7,000] = 8,000

CHECK:
- Math is correct: 5,000 + 2,000 = 7,000 ✓
- Outstanding: 15,000 - 7,000 = 8,000 ✓
- No negative balances
- Currency format (Ksh) is correct
```

**The Math Test Details:**
```
Grade 2 CBC Standard Fee: 15,000 Ksh (from fees.CBC_TERMLY_FEES)
Amani's Payments:
  - Tuition: 5,000
  - Transport: 2,000
  - TOTAL PAID: 7,000

Statement Should Calculate:
  Expected Fee ............ 15,000
  - Total Paid ........... (7,000)
  = Outstanding Balance ... 8,000
```

**If Math is Wrong:**
- ❌ Outstanding shows 8,000 but should be different: CBC_TERMLY_FEES incorrect
- ❌ Shows negative balance: Payment recorded wrong
- ❌ Total Paid wrong: Sum query issue in backend

**If test fails:**
- ❌ Blank statement: Check console for render errors
- ❌ "Student not found": Student ID not in fees table
- ❌ Wrong amounts: Check if payments saved correctly in Phase 4.2-4.3

### Test 4.5: Print Statement
```
ACTION:
1. On the statement, click "Print" button
2. Browser print dialog opens
3. Look at preview

EXPECTED RESULT:
✓ Print preview shows clean layout
✓ No buttons or sidebar visible
✓ Only statement content visible
✓ Page margins look professional
✓ Can click "Cancel" to go back

CHECK:
- @media print CSS is working
- No layout breaks
- Readability is good
```

**🟢 Phase 4 Complete if:**
- ✓ Payment 1 (5,000 Tuition) recorded
- ✓ Payment 2 (2,000 Transport) recorded
- ✓ Both payments visible in ledger with correct date/accountant
- ✓ Statement shows Total Paid = 7,000
- ✓ Statement shows Outstanding Balance = 8,000
- ✓ Print preview works without errors

---

## 📊 Phase 5: End of Term Academics (Grading & Report Card)

**Duration:** ~10 minutes
**Critical Path:** Grade Entry → Submit → Generate Report Card

### Test 5.1: Navigate to CBC Grading
```
ACTION:
1. Login as Teacher (mwalimu1) - might need to logout first
2. Click "Academics" → "Grading"
   OR menu: "Academics" → "CBC Grading"
3. You should see:
   - Grade selector
   - Term selector
   - Learning Area selector

EXPECTED RESULT:
✓ Grade field loads
✓ Term field loads
✓ Learning Area dropdown shows options:
  - Mathematics Activities
  - Language Activities
  - Environmental Activities
  - Religious Education
  - (etc., based on your system)
```

### Test 5.2: Select Grade 2, Term 1, Math Activities
```
ACTION:
1. Grade dropdown: Select "Grade 2"
2. Term dropdown: Select "Term 1"
3. Learning Area dropdown: Select "Mathematics Activities"
4. Click "Load Students" or "Fetch Assessments"

EXPECTED RESULT:
✓ Amani Joy appears in list
✓ Each student shows score options:
  - EE (Exceeding Expectations)
  - ME (Meeting Expectations)
  - AE (Approaching Expectations)
  - BE (Below Expectations)
✓ Remarks text field per student
```

**If test fails:**
- ❌ No students load: Check backend grading/assessment API
- ❌ Grade options don't show: Check Assessment schema
- ❌ 500 error: Check academics.py for query issues

### Test 5.3: Grade Amani Joy
```
ACTION:
1. Find Amani Joy row
2. Select Score: "EE" (click radio or dropdown)
3. In Remarks field, type: "Excellent counting skills"
4. Look for other students in list, grade them too (any scores):
   - If there are other Grade 2 students, give them scores
5. Click "Submit Grades" or "Save Assessments"

EXPECTED RESULT:
✓ Green success message
✓ Grades saved to database
✓ Can see confirmation:
  - "Assessments recorded" or similar
  - Amani's record shows EE + remark

CHECK:
- Backend terminal: POST /api/academics/assessments (or similar) with 200
- Console: No validation errors
- Network tab: Bulk request with all students
```

**Database Verification:**
```sql
-- Check assessment record:
SELECT student_id, learning_area, score, remarks 
FROM assessments 
WHERE student_id IN (SELECT id FROM students WHERE admission_number = 'BONA-100')
AND learning_area = 'Mathematics Activities'
AND term = 'Term 1';

-- Should show:
-- [Amani's ID] | Mathematics Activities | EE | Excellent counting skills
```

**If test fails:**
- ❌ Submit button does nothing: Check form handler in grading component
- ❌ 400 error: Check score format (should be "EE", not "Exceeding Expectations")
- ❌ 500 error: Check academics.py bulk insert logic

### Test 5.4: Generate Report Card
```
ACTION:
1. Go to "Academics" → "Report Card"
2. Select student: "Amani Joy"
3. Select term: "Term 1"
4. Click "Generate Report Card" or "View Report"

EXPECTED RESULT (on report card):
✓ School header with:
  - School name: "Bona School"
  - School logo/branding
  - Contact details (if included)

✓ Student information:
  - Name: Amani Joy
  - Admission: BONA-100
  - Grade: Grade 2
  - Term: Term 1

✓ Learning Areas section showing:
  - Mathematics Activities ............ EE
  - [Other areas graded]
  - Teacher Remark: "Excellent counting skills"

✓ Grading Key at bottom:
  - EE = Exceeding Expectations
  - ME = Meeting Expectations
  - AE = Approaching Expectations
  - BE = Below Expectations

✓ Teacher signature line (if applicable)
✓ Principal signature line (if applicable)

CHECK:
- All grades and remarks from Phase 5.3 appear
- No blank sections
- Formatting is clean and professional
- Print-friendly layout
```

**If Report Card is blank/missing:**
- ❌ No grades showing: Check assessment query in academics.py
- ❌ Wrong student: Student_id mismatch
- ❌ No teacher remark: Check remarks field not being saved

### Test 5.5: Print Report Card
```
ACTION:
1. On report card, click "Print" button
2. Print preview opens

EXPECTED RESULT:
✓ Preview looks perfect
✓ No buttons visible in preview
✓ Sidebars hidden
✓ Content fills page nicely
✓ Click "Cancel" returns to screen
```

**🟢 Phase 5 Complete if:**
- ✓ Assigned Amani EE score in Math with remark
- ✓ Report card displays:
  - Correct student info
  - Correct grade (EE)
  - Correct remark ("Excellent counting skills")
  - Professional layout with school header
- ✓ Print preview works without errors

---

## 📈 Phase 6: The Executive View (Dashboard Analytics)

**Duration:** ~5 minutes
**Critical Path:** Dashboard Load → Verify Cards → Check Numbers

### Test 6.1: Navigate to Dashboard
```
ACTION:
1. Login as Admin (if not already)
2. Click "Dashboard" from sidebar
   OR click logo to go home
3. Wait for page to fully load (Promise.all data fetching)

EXPECTED RESULT:
✓ Dashboard loads completely
✓ No loading spinners stuck
✓ No blank areas
✓ No error toasts
✓ Analytics cards visible

CHECK:
- Backend terminal: Multiple GET requests (students, staff, fees, etc.)
- Console (F12): No JavaScript errors
- Network tab: All dashboard API calls return 200
```

**If test fails:**
- ❌ Blank screen: Check DashboardHome.vue for render errors
- ❌ Loading spinner never stops: Promise.all taking too long, check API responses
- ❌ 500 error in terminal: Check dashboard API endpoints

### Test 6.2: Verify Analytics Cards - TOTAL STUDENTS
```
ACTION:
1. Look for card titled "Total Students" or "Students Enrolled"
2. Note the number displayed

EXPECTED RESULT:
✓ Card shows: 1
  (Because we added only Amani Joy in Phase 2)

HOW TO VERIFY:
- Backend should query: SELECT COUNT(*) FROM students WHERE status = 'Active'
- Should return 1 (just Amani)
- Or if there are existing students from before, count should include all

MANUAL CHECK:
- Remember: You added Amani Joy in Phase 2
- So minimum is 1
- If you see 0: Query issue
- If you see 10+: Pre-existing data from setup
```

### Test 6.3: Verify Analytics Cards - TOTAL REVENUE
```
ACTION:
1. Look for card titled "Total Revenue" or "Total Fees Collected"
2. Note the currency amount

EXPECTED RESULT:
✓ Card shows: KES 7,000.00
  (From Amani's payments: 5,000 + 2,000)

HOW TO VERIFY:
- Backend should query: SELECT SUM(amount) FROM fees
- Should return 7000 (7000.00)
- Currency formatting should show: Ksh 7,000 or KES 7,000

MANUAL CHECK:
- Tuition: 5,000 ✓
- Transport: 2,000 ✓
- TOTAL: 7,000 ✓

FORMULA:
sum(fees.amount) WHERE [all payments from Phase 4]
```

**If Revenue is Wrong:**
- ❌ Shows 0: fees table query broken
- ❌ Shows 5,000: Second payment not recorded
- ❌ Shows 10,000+: Payments recorded twice or test data exists

### Test 6.4: Verify Analytics Cards - ACTIVE STAFF
```
ACTION:
1. Look for card titled "Active Staff", "Teachers", or "Staff Members"
2. Note the number displayed

EXPECTED RESULT:
✓ Card shows: At least 1
  (The teacher mwalimu1 we created in Phase 1)

MINIMUM EXPECTED:
- 1 Admin (you)
- 1 Teacher (mwalimu1 created)
- Possibly 1 Accountant

HOW TO VERIFY:
- Backend should query: SELECT COUNT(*) FROM users WHERE role != 'student'
- OR: SELECT COUNT(*) FROM staff WHERE is_active = true

If you created:
- Admin account: +1
- Teacher (mwalimu1): +1
- Accountant: +1
- Total should be 3+
```

**If Staff Count is Wrong:**
- ❌ Shows 0: users table not connected
- ❌ Shows 1: Only counting admin, not teacher we created

### Test 6.5: Check Card Styling & Responsiveness
```
ACTION:
1. Look at all cards:
   - Colors: Should match brand colors
   - Icons: Should display properly
   - Numbers: Should be readable
   - Currency: Should format correctly
2. Resize browser window:
   - Desktop (1920px): Cards should be 4 columns or grid
   - Tablet (768px): Cards should stack nicely
   - Mobile (375px): Cards should be 1 column

EXPECTED RESULT:
✓ All cards visible and readable at all sizes
✓ Numbers are bold/large for visibility
✓ No text overflow
✓ Icons are colorful (not broken)
```

### Test 6.6: Check for Data Freshness
```
ACTION:
1. Go back to Phase 4 Finance section
2. Record a new payment for Amani (add another 1,000)
3. Return to Dashboard without refresh
4. Check if Total Revenue updated

EXPECTED RESULT (Option A - Auto-Refresh):
✓ Revenue updates to 8,000 automatically

EXPECTED RESULT (Option B - Manual Refresh):
✓ User must refresh (F5) to see new total
✓ After refresh, shows 8,000

ACCEPTABLE: Either is fine, but auto-refresh is better UX
```

**If Data is Stale:**
- ⚠️ Card shows old number: This is OK if user knows to refresh
- ⚠️ Never updates: Check if API call is being made on page load

**🟢 Phase 6 Complete if:**
- ✓ Dashboard loads without errors
- ✓ Total Students card shows ≥1
- ✓ Total Revenue card shows KES 7,000
- ✓ Active Staff card shows ≥1 (likely 3+)
- ✓ Cards are responsive and well-formatted
- ✓ All numbers are mathematically correct

---

## 🎉 FINAL VALIDATION

### All 6 Phases Passed = MARKET-READY ✅

If you completed all phases with:
- ✓ No 500 errors in backend terminal
- ✓ No "Uncaught" errors in browser console
- ✓ No blank/stuck loading screens
- ✓ All data correctly saved and retrieved
- ✓ All calculations mathematically correct
- ✓ RBAC properly enforcing permissions
- ✓ Foreign keys maintaining data integrity
- ✓ Print previews rendering correctly

**THEN:** You have a production-ready software product.

---

## 🔍 Troubleshooting Quick Reference

### Silent Failures (Button clicks do nothing)
```
CHECK:
1. Browser console (F12) for JavaScript errors
2. Network tab: Is fetch request being made?
3. Backend terminal: Any error logs?

LIKELY CAUSE:
- Form validation failing silently
- API endpoint mismatch
- Token expired (refresh page)
- Frontend-backend version mismatch
```

### Red Backend Errors
```
WATCH FOR:
- 400 Bad Request: Data format mismatch
- 401 Unauthorized: Token expired or invalid
- 403 Forbidden: Insufficient permissions (RBAC)
- 404 Not Found: Endpoint doesn't exist
- 500 Internal Server Error: Backend bug

SOLUTION:
1. Check backend terminal full error message
2. Search database for missing foreign keys
3. Verify form data matches schema
4. Check PostgreSQL is running
```

### Blank White Screen
```
PRESS: F12 to open Developer Tools
CHECK: Console tab for errors
LOOK FOR:
- "ReferenceError: [name] is not defined"
- "Cannot read property 'x' of undefined"
- "Failed to fetch [URL]"

FIX:
- Hard refresh (Ctrl+Shift+R) to clear cache
- Check backend is running
- Verify frontend `.env` has correct API URL
```

### "Cannot find variable: localStorage"
```
CAUSE: Running server-side rendering or special environment
FIX:
- Ensure you're in browser environment
- Check auth store for typeof checks
```

### Math Wrong on Statement
```
VERIFY:
1. CBC_TERMLY_FEES['Grade 2'] value in fees.py
2. Sum of all payments in fees table
3. Formula: Expected - Paid = Outstanding

CHECK QUERY:
SELECT SUM(amount) FROM fees WHERE student_id = [ID];
```

---

## 📋 Test Results Checklist

Use this to track completion:

### Phase 1: Security ✅/❌
- [ ] Route guard blocks /finance
- [ ] Admin login successful
- [ ] All menu items visible for admin
- [ ] New teacher account created
- [ ] Cannot delete own admin account

### Phase 2: Admissions ✅/❌
- [ ] Added Amani Joy, BONA-100, Grade 2
- [ ] Duplicate admission number rejected
- [ ] Student appears in directory

### Phase 3: Teacher's Morning ✅/❌
- [ ] Teacher mwalimu1 can login
- [ ] Finance/HR hidden from teacher menu
- [ ] Grade 2 students loaded
- [ ] Attendance marked (Amani absent, Fever)
- [ ] Attendance saved to database

### Phase 4: Financial Engine ✅/❌
- [ ] Payment 1: 5,000 Tuition recorded
- [ ] Payment 2: 2,000 Transport recorded
- [ ] Both appear in Fee Ledger
- [ ] Statement generated
- [ ] Math correct: 5,000+2,000=7,000
- [ ] Outstanding: 15,000-7,000=8,000
- [ ] Print preview works

### Phase 5: Academics ✅/❌
- [ ] Amani graded EE in Math
- [ ] Remark saved: "Excellent counting skills"
- [ ] Report card displays all info
- [ ] Report card print preview works

### Phase 6: Dashboard ✅/❌
- [ ] Dashboard loads without errors
- [ ] Total Students ≥1
- [ ] Total Revenue = 7,000
- [ ] Active Staff ≥1
- [ ] All numbers correct
- [ ] Cards responsive

---

**Good luck with your test drive! Report back with any issues.** 🚀

