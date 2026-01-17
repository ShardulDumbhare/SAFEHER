#!/usr/bin/env python3
"""
SAFEHER - Simple Quick Test
Just runs one test to verify backend is working
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

print("\n" + "="*50)
print("🚀 SAFEHER Backend - Quick Verification")
print("="*50 + "\n")

# Test 1: Health Check
print("Testing: GET /ping")
try:
    response = requests.get(f"{BASE_URL}/ping", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Server Status: {data.get('status')}")
        print(f"✅ Database: {data.get('database')}")
        print(f"\n🎉 Backend is working! 🎉\n")
        sys.exit(0)
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"❌ Response: {response.text}")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print(f"❌ Connection refused!")
    print(f"❌ Is the server running? Try: python app.py\n")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}\n")
    sys.exit(1)
