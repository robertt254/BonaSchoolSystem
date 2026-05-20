#!/usr/bin/env python3
"""
Bona School E2E Test - System Status Validator
Run from any directory: python check_system_status.py
"""

import os
import sys
import requests
from datetime import datetime

# Resolve the backend directory relative to this script — works from any CWD.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}\n{text}\n{'='*60}{Colors.END}\n")

def print_success(text): print(f"{Colors.GREEN}✓ {text}{Colors.END}")
def print_error(text):   print(f"{Colors.RED}✗ {text}{Colors.END}")
def print_warning(text): print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")
def print_info(text):    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def check_backend():
    print_header("CHECKING BACKEND")
    try:
        response = requests.get('http://localhost:8000/', timeout=2)
        print_success("Backend is running")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Backend is NOT running")
        print_info("Start with: cd backend && python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print_error(f"Backend error: {e}")
        return False


def check_frontend():
    print_header("CHECKING FRONTEND")
    try:
        requests.get('http://localhost:5173/', timeout=2)
        print_success("Frontend is running")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Frontend is NOT running")
        print_info("Start with: cd frontend && npm run dev")
        return False
    except Exception as e:
        print_warning(f"Frontend connection: {e}")
        return False


def check_database():
    print_header("CHECKING DATABASE")
    try:
        from database import SessionLocal
        from models import User
        db = SessionLocal()
        user_count = db.query(User).count()
        print_success("Database connected")
        print(f"  Users in database: {user_count}")
        db.close()
        return True
    except ModuleNotFoundError:
        print_error("Cannot import database module — run from the project root")
        return False
    except Exception as e:
        print_error(f"Database error: {e}")
        print_info("Verify PostgreSQL is running and DATABASE_URL in backend/.env is correct")
        return False


def check_admin_user():
    print_header("CHECKING ADMIN USER")
    try:
        from database import SessionLocal
        from models import User
        db = SessionLocal()
        admin = db.query(User).filter(User.role == 'admin').first()
        db.close()
        if admin:
            print_success(f"Admin user exists: {admin.username}")
            return True
        print_warning("No admin user — call POST /api/auth/setup-users to seed initial users")
        return False
    except Exception as e:
        print_error(f"Cannot check admin user: {e}")
        return False


def check_test_data():
    print_header("CHECKING TEST DATA")
    try:
        from database import SessionLocal
        from models import Student
        db = SessionLocal()
        amani = db.query(Student).filter(
            Student.admission_number == 'BONA-100'
        ).first()
        db.close()
        if amani:
            print_success(f"Test student exists — ID {amani.id}, Grade {amani.grade_level}")
        else:
            print_warning("Test student not found (will be created in Phase 2)")
        return True
    except Exception as e:
        print_warning(f"Cannot check test data: {e}")
        return False


def check_api_endpoints():
    print_header("CHECKING API ENDPOINTS")
    results = []

    try:
        response = requests.get('http://localhost:8000/', timeout=2)
        print_success(f"GET / → {response.status_code}")
        results.append(True)
    except Exception:
        print_error("GET / failed")
        results.append(False)

    # Invalid token should return 401 (Unauthorized), not 403 (Forbidden)
    try:
        headers = {'Authorization': 'Bearer invalid_token'}
        response = requests.get('http://localhost:8000/api/students/', headers=headers, timeout=2)
        if response.status_code == 401:
            print_success("GET /api/students/ with invalid token → 401 (correct)")
            results.append(True)
        else:
            print_warning(f"GET /api/students/ returned {response.status_code} (expected 401)")
            results.append(False)
    except Exception as e:
        print_error(f"GET /api/students/ check failed: {e}")
        results.append(False)

    return all(results)


def check_cors():
    print_header("CHECKING CORS")
    try:
        response = requests.options(
            'http://localhost:8000/api/students/',
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'GET'
            },
            timeout=2
        )
        cors_header = response.headers.get('access-control-allow-origin')
        if cors_header:
            print_success(f"CORS configured — allowed origin: {cors_header}")
            return True
        print_warning("CORS header missing from OPTIONS response")
        return False
    except Exception as e:
        print_warning(f"CORS check: {e}")
        return False


def check_frontend_env():
    print_header("CHECKING FRONTEND ENVIRONMENT")
    for path in ['frontend/.env', 'frontend/.env.local', 'frontend/.env.development']:
        full = os.path.join(SCRIPT_DIR, path)
        if os.path.exists(full):
            print_success(f"Found: {path}")
            return True
    print_warning("No .env file in frontend — using default VITE_API_URL=http://127.0.0.1:8000")
    return True


def main():
    print(f"\n{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════╗")
    print("║  Bona School E2E Test - System Status Check   ║")
    print(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.END}")

    results = {
        'Backend':        check_backend(),
        'Frontend':       check_frontend(),
        'Database':       check_database(),
        'Admin User':     check_admin_user(),
        'Test Data':      check_test_data(),
        'API Endpoints':  check_api_endpoints(),
        'CORS':           check_cors(),
        'Frontend Env':   check_frontend_env(),
    }

    print_header("SUMMARY")
    passed = sum(1 for v in results.values() if v)
    for check, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {check:.<35} {status}")

    print(f"\n  {Colors.BLUE}Total: {passed}/{len(results)} checks passed{Colors.END}")

    print_header("NEXT STEPS")
    if results['Backend'] and results['Frontend'] and results['Database']:
        print_success("System is ready for E2E testing!")
        print("  1. Open http://localhost:5173/ in your browser")
        print("  2. Open an incognito window for the auth guard test")
        print("  3. Follow E2E_TEST_EXECUTION_GUIDE.md")
        return 0
    else:
        print_error("System is NOT ready. Fix issues above before testing.")
        if not results['Backend']:
            print("  • cd backend && python -m uvicorn main:app --reload")
        if not results['Frontend']:
            print("  • cd frontend && npm run dev")
        if not results['Database']:
            print("  • Start PostgreSQL and check DATABASE_URL in backend/.env")
        return 1


if __name__ == '__main__':
    sys.exit(main())
