#!/usr/bin/env python3
"""
Bona School E2E Test - System Status Validator
Checks if backend, frontend, and database are ready for testing
"""

import requests
import json
import subprocess
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_backend():
    """Check if backend API is running"""
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
        print_error(f"Backend error: {str(e)}")
        return False

def check_frontend():
    """Check if frontend is running"""
    print_header("CHECKING FRONTEND")
    
    try:
        response = requests.get('http://localhost:5173/', timeout=2)
        print_success("Frontend is running")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Frontend is NOT running")
        print_info("Start with: cd frontend && npm run dev")
        return False
    except Exception as e:
        print_warning(f"Frontend connection: {str(e)}")
        return False

def check_database():
    """Check if PostgreSQL database is accessible"""
    print_header("CHECKING DATABASE")
    
    try:
        from database import SessionLocal
        db = SessionLocal()
        
        # Try a simple query
        from models import User
        user_count = db.query(User).count()
        print_success(f"Database connected")
        print(f"  Users in database: {user_count}")
        db.close()
        return True
    except ModuleNotFoundError:
        print_error("Cannot import database module")
        return False
    except Exception as e:
        print_error(f"Database error: {str(e)}")
        print_info("Verify PostgreSQL is running and connection string is correct")
        return False

def check_admin_user():
    """Check if admin user exists"""
    print_header("CHECKING ADMIN USER")
    
    try:
        from database import SessionLocal
        from models import User
        
        db = SessionLocal()
        admin = db.query(User).filter(User.role == 'admin').first()
        
        if admin:
            print_success(f"Admin user exists")
            print(f"  Username: {admin.username}")
            print(f"  Name: {admin.name}")
            db.close()
            return True
        else:
            print_warning("No admin user found")
            print_info("You may need to create one: python update_passwords.py")
            db.close()
            return False
    except Exception as e:
        print_error(f"Cannot check admin user: {str(e)}")
        return False

def check_test_data():
    """Check if test data exists (student Amani)"""
    print_header("CHECKING TEST DATA")
    
    try:
        from database import SessionLocal
        from models import Student
        
        db = SessionLocal()
        amani = db.query(Student).filter(
            Student.admission_number == 'BONA-100'
        ).first()
        
        if amani:
            print_success("Test student (Amani Joy) exists")
            print(f"  Student ID: {amani.id}")
            print(f"  Grade: {amani.grade_level}")
        else:
            print_warning("Test student does not exist yet")
            print_info("You will create this in Phase 2 of the test")
        
        db.close()
        return True
    except Exception as e:
        print_warning(f"Cannot check test data: {str(e)}")
        return False

def check_api_endpoints():
    """Check if key API endpoints are working"""
    print_header("CHECKING API ENDPOINTS")
    
    endpoints_to_check = [
        ('GET', '/api/auth/login', False),  # Should fail (POST not available)
        ('GET', '/', True),  # Should succeed
    ]
    
    results = []
    
    # Check without auth (login should work without token)
    try:
        response = requests.get('http://localhost:8000/', timeout=2)
        print_success(f"GET /")
        results.append(True)
    except:
        print_error(f"GET / failed")
        results.append(False)
    
    # Check with invalid token (should fail with 403)
    try:
        headers = {'Authorization': 'Bearer invalid_token'}
        response = requests.get('http://localhost:8000/api/students', 
                               headers=headers, timeout=2)
        if response.status_code == 403:
            print_success(f"GET /api/students with invalid token returns 403 (expected)")
            results.append(True)
        else:
            print_warning(f"GET /api/students returned {response.status_code} (expected 403)")
            results.append(False)
    except Exception as e:
        print_error(f"GET /api/students check failed: {str(e)}")
        results.append(False)
    
    return all(results)

def check_cors():
    """Check if CORS is properly configured"""
    print_header("CHECKING CORS")
    
    try:
        response = requests.options(
            'http://localhost:8000/api/students',
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'GET'
            },
            timeout=2
        )
        
        cors_header = response.headers.get('access-control-allow-origin')
        if cors_header:
            print_success(f"CORS is configured")
            print(f"  Allowed origin: {cors_header}")
            return True
        else:
            print_warning("CORS header not found in response")
            return False
    except Exception as e:
        print_warning(f"CORS check: {str(e)}")
        return False

def check_frontend_env():
    """Check if frontend .env file exists"""
    print_header("CHECKING FRONTEND ENVIRONMENT")
    
    import os
    
    frontend_paths = [
        'frontend/.env',
        'frontend/.env.local',
        'frontend/.env.development'
    ]
    
    for path in frontend_paths:
        if os.path.exists(path):
            print_success(f"Found: {path}")
            return True
    
    print_warning("No .env file found in frontend")
    print_info("Frontend will use default API URL: http://127.0.0.1:8000")
    return True  # Not critical, but good to have

def main():
    print(f"\n{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════╗")
    print("║  Bona School E2E Test - System Status Check   ║")
    print(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    results = {
        'Backend': check_backend(),
        'Frontend': check_frontend(),
        'Database': check_database(),
        'Admin User': check_admin_user(),
        'Test Data': check_test_data(),
        'API Endpoints': check_api_endpoints(),
        'CORS': check_cors(),
        'Frontend Config': check_frontend_env(),
    }
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {check:.<35} {status}")
    
    print(f"\n  {Colors.BLUE}Total: {passed}/{total} checks passed{Colors.END}")
    
    # Recommendations
    print_header("RECOMMENDATIONS")
    
    if results['Backend'] and results['Frontend'] and results['Database']:
        print_success("System is ready for E2E testing!")
        print("\nNext steps:")
        print("1. Open browser to http://localhost:5173/")
        print("2. Open incognito window for Phase 1 guard test")
        print("3. Follow E2E_TEST_EXECUTION_GUIDE.md")
        return 0
    else:
        print_error("System is NOT ready. Fix issues above before testing.")
        print("\nMissing components:")
        if not results['Backend']:
            print("  • Start backend: cd backend && python -m uvicorn main:app --reload")
        if not results['Frontend']:
            print("  • Start frontend: cd frontend && npm run dev")
        if not results['Database']:
            print("  • Start PostgreSQL and verify connection string")
        return 1

if __name__ == '__main__':
    sys.exit(main())
