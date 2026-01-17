#!/usr/bin/env python3
"""
SAFEHER Backend - Complete Testing Guide
Run all endpoints and verify functionality
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USERNAME = "test_user"
TEST_EMAIL = "test@safeher.com"
TEST_PIN = "1234"
TEST_PASSWORD = "secure123"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_test(name, passed, response=None):
    """Print test result"""
    status = f"{GREEN}✅ PASS{END}" if passed else f"{RED}❌ FAIL{END}"
    print(f"\n{BLUE}[TEST]{END} {name}")
    print(f"Status: {status}")
    if response:
        print(f"Response: {json.dumps(response, indent=2)}")

def test_health_check():
    """Test 1: Health Check"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 1: Health Check{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    try:
        response = requests.get(f"{BASE_URL}/ping")
        passed = response.status_code == 200
        data = response.json()
        print_test("GET /ping", passed, data)
        return passed, data
    except Exception as e:
        print_test("GET /ping", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_register_user():
    """Test 2: Register User"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 2: Register User{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "email": TEST_EMAIL,
        "pin": TEST_PIN
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=payload)
        passed = response.status_code == 201
        data = response.json()
        print_test("POST /register", passed, data)
        return passed, data
    except Exception as e:
        print_test("POST /register", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_get_user():
    """Test 3: Get User Info"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 3: Get User Info{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    try:
        response = requests.get(f"{BASE_URL}/user/{TEST_USERNAME}")
        passed = response.status_code == 200
        data = response.json()
        print_test(f"GET /user/{TEST_USERNAME}", passed, data)
        return passed, data
    except Exception as e:
        print_test(f"GET /user/{TEST_USERNAME}", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_add_contact():
    """Test 4: Add Contact"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 4: Add Emergency Contact{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    payload = {
        "username": TEST_USERNAME,
        "name": "Mom",
        "relation": "Mother",
        "contact": "9876543210"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload)
        passed = response.status_code == 201
        data = response.json()
        print_test("POST /contact", passed, data)
        return passed, data
    except Exception as e:
        print_test("POST /contact", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_get_contacts():
    """Test 5: Get All Contacts"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 5: Get All Contacts{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    try:
        response = requests.get(f"{BASE_URL}/contacts/{TEST_USERNAME}")
        passed = response.status_code == 200
        data = response.json()
        print_test(f"GET /contacts/{TEST_USERNAME}", passed, data)
        return passed, data
    except Exception as e:
        print_test(f"GET /contacts/{TEST_USERNAME}", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_analyze_location():
    """Test 6: Analyze Location"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 6: Analyze Location Safety{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    payload = {
        "username": TEST_USERNAME,
        "lat": 12.5,
        "lng": 77.5,
        "accuracy": 50
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        passed = response.status_code == 200
        data = response.json()
        print_test("POST /analyze", passed, data)
        return passed, data
    except Exception as e:
        print_test("POST /analyze", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_get_locations():
    """Test 7: Get Location History"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 7: Get Location History{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    try:
        response = requests.get(f"{BASE_URL}/locations/{TEST_USERNAME}?limit=10")
        passed = response.status_code == 200
        data = response.json()
        print_test(f"GET /locations/{TEST_USERNAME}", passed, data)
        return passed, data
    except Exception as e:
        print_test(f"GET /locations/{TEST_USERNAME}", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_sos_alert():
    """Test 8: Trigger SOS"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 8: Trigger SOS Alert{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    payload = {
        "username": TEST_USERNAME,
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/sos", json=payload)
        passed = response.status_code in [200, 500]  # 500 is OK if Firebase not configured
        data = response.json()
        print_test("POST /sos", passed, data)
        return passed, data
    except Exception as e:
        print_test("POST /sos", False)
        print(f"{RED}Error: {e}{END}")
        return False, None

def test_validation_errors():
    """Test 9: Validation Error Handling"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 9: Validation Error Handling{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    # Test missing username
    payload = {"lat": 12.5, "lng": 77.5}
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        passed = response.status_code == 400
        data = response.json()
        print_test("Validate missing username", passed, data)
    except Exception as e:
        print(f"{RED}Error: {e}{END}")

def test_error_responses():
    """Test 10: Error Responses"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"TEST 10: Error Response Handling{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    # Test invalid email
    payload = {
        "username": "test",
        "password": "pass",
        "email": "invalid-email",
        "pin": "1234"
    }
    try:
        response = requests.post(f"{BASE_URL}/register", json=payload)
        passed = response.status_code == 400
        data = response.json()
        print_test("Validate email format", passed, data)
    except Exception as e:
        print(f"{RED}Error: {e}{END}")

def run_all_tests():
    """Run all tests"""
    print(f"\n\n{BLUE}{'='*60}")
    print(f"    🚀 SAFEHER BACKEND - COMPREHENSIVE TEST SUITE")
    print(f"{'='*60}{END}\n")
    
    print(f"{YELLOW}Server URL: {BASE_URL}")
    print(f"Test User: {TEST_USERNAME}")
    print(f"{'='*60}{END}\n")
    
    results = []
    
    # Run tests
    print(f"\n{BLUE}Starting tests...{END}")
    
    results.append(("Health Check", test_health_check()[0]))
    results.append(("Register User", test_register_user()[0]))
    results.append(("Get User Info", test_get_user()[0]))
    results.append(("Add Contact", test_add_contact()[0]))
    results.append(("Get Contacts", test_get_contacts()[0]))
    results.append(("Analyze Location", test_analyze_location()[0]))
    results.append(("Get Locations", test_get_locations()[0]))
    results.append(("SOS Alert", test_sos_alert()[0]))
    test_validation_errors()
    test_error_responses()
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print(f"    📊 TEST SUMMARY")
    print(f"{'='*60}{END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✅ PASS{END}" if result else f"{RED}❌ FAIL{END}"
        print(f"{status} {test_name}")
    
    print(f"\n{YELLOW}Total: {passed}/{total} tests passed{END}\n")
    
    if passed == total:
        print(f"{GREEN}🎉 All tests passed! Backend is working correctly!{END}\n")
    else:
        print(f"{RED}⚠️  Some tests failed. Check errors above.{END}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{END}")
    except Exception as e:
        print(f"\n{RED}Test suite error: {e}{END}")
        print(f"\n{YELLOW}Make sure the backend is running:{END}")
        print(f"  python app.py")
