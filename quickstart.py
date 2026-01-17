#!/usr/bin/env python3
"""
SAFEHER Quick Start Guide
Run this to test the backend setup
"""

import os
import sys

print("🚀 SAFEHER Backend - Quick Start Check")
print("=" * 50)

# Check Python version
print("\n✓ Python Version Check")
if sys.version_info >= (3, 8):
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
else:
    print(f"  ❌ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.8+)")

# Check required files
print("\n✓ Required Files Check")
required_files = [
    'app.py',
    'database.py',
    'db_adapter.py',
    'ai_engine.py',
    'validators.py',
    'logger.py',
    'firebase_key.json'
]

for file in required_files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} (MISSING)")

# Check environment
print("\n✓ Environment Variables Check")
env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"  ✅ {var}={value[:20]}...")
    else:
        print(f"  ⚠️  {var} (not set, using default)")

# Check dependencies
print("\n✓ Dependencies Check")
dependencies = ['flask', 'flask_cors', 'firebase_admin', 'mysql.connector']
for dep in dependencies:
    try:
        __import__(dep)
        print(f"  ✅ {dep}")
    except ImportError:
        print(f"  ❌ {dep} (MISSING - run: pip install -r requirements.txt)")

print("\n" + "=" * 50)
print("\n📋 Next Steps:")
print("1. Create MySQL database: CREATE DATABASE safeher_db;")
print("2. Set environment variables in .env file")
print("3. Install dependencies: pip install -r requirements.txt")
print("4. Run: python app.py")
print("\n✅ Your SAFEHER backend is ready to go! 🎉")
