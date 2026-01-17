# SAFEHER Backend - Testing Guide

## 🚀 How to Test Your Backend

This guide shows you **3 ways to test** your SAFEHER backend.

---

## **METHOD 1: Automatic Testing (Easiest) ⚡**

### Prerequisites
```bash
pip install requests
```

### Run All Tests
```bash
python test_backend.py
```

**What it does:**
- ✅ Runs 10 comprehensive tests
- ✅ Tests all 9 API endpoints
- ✅ Validates error handling
- ✅ Shows results with colors
- ✅ Generates test report

**Expected Output:**
```
============================================================
    🚀 SAFEHER BACKEND - COMPREHENSIVE TEST SUITE
============================================================

Server URL: http://localhost:5000
Test User: test_user
============================================================

Starting tests...

✅ PASS Health Check
✅ PASS Register User
✅ PASS Get User Info
✅ PASS Add Contact
...

📊 TEST SUMMARY
============================================================
Total: 10/10 tests passed
🎉 All tests passed! Backend is working correctly!
```

---

## **METHOD 2: Manual Testing with cURL (Terminal) 📝**

### Start Your Server
```bash
python app.py
```

### Test Endpoints

#### 1️⃣ Health Check
```bash
curl http://localhost:5000/ping
```

**Expected Response (200 OK):**
```json
{
  "status": "Online",
  "project": "SAFEHER",
  "database": "Connected",
  "timestamp": "2025-01-17T14:30:00.123456"
}
```

---

#### 2️⃣ Register User
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah123",
    "password": "secure_password",
    "email": "sarah@example.com",
    "pin": "1234"
  }'
```

**Expected Response (201 Created):**
```json
{
  "status": "Success",
  "message": "User registered successfully"
}
```

---

#### 3️⃣ Get User Info
```bash
curl http://localhost:5000/user/sarah123
```

**Expected Response (200 OK):**
```json
{
  "username": "sarah123",
  "email": "sarah@example.com"
}
```

---

#### 4️⃣ Add Emergency Contact
```bash
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah123",
    "name": "Mom",
    "relation": "Mother",
    "contact": "9876543210"
  }'
```

**Expected Response (201 Created):**
```json
{
  "status": "Success",
  "message": "Contact added successfully"
}
```

---

#### 5️⃣ Get All Contacts
```bash
curl http://localhost:5000/contacts/sarah123
```

**Expected Response (200 OK):**
```json
{
  "username": "sarah123",
  "count": 1,
  "contacts": [
    {
      "name": "Mom",
      "relation": "Mother",
      "contact": "9876543210"
    }
  ]
}
```

---

#### 6️⃣ Analyze Location Safety
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah123",
    "lat": 12.5,
    "lng": 77.5,
    "accuracy": 50
  }'
```

**Expected Response (200 OK):**
```json
{
  "risk_level": "Low",
  "reason": "Area appears safe",
  "time": "14:30",
  "location_logged": true
}
```

---

#### 7️⃣ Get Location History
```bash
curl "http://localhost:5000/locations/sarah123?limit=10"
```

**Expected Response (200 OK):**
```json
{
  "username": "sarah123",
  "count": 1,
  "locations": [
    {
      "latitude": 12.5,
      "longitude": 77.5,
      "accuracy": 50,
      "timestamp": "2025-01-17 14:30:00"
    }
  ]
}
```

---

#### 8️⃣ Trigger SOS Alert
```bash
curl -X POST http://localhost:5000/sos \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah123",
    "name": "Sarah Doe"
  }'
```

**Expected Response (200 OK or 500 if Firebase not configured):**
```json
{
  "status": "Success",
  "message": "FCM Alert Sent"
}
```

---

#### 9️⃣ Test Error Handling - Missing Username
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 12.5,
    "lng": 77.5
  }'
```

**Expected Response (400 Bad Request):**
```json
{
  "error": "Username required"
}
```

---

#### 🔟 Test Error Handling - Invalid Email
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "pass",
    "email": "not-an-email",
    "pin": "1234"
  }'
```

**Expected Response (400 Bad Request):**
```json
{
  "error": "Registration failed",
  "message": "Email error: Invalid email format"
}
```

---

## **METHOD 3: Using Postman (GUI) 🖥️**

### Step 1: Download Postman
https://www.postman.com/downloads/

### Step 2: Create Requests

**New Request → POST**
- URL: `http://localhost:5000/register`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "username": "test_user",
  "password": "password",
  "email": "test@example.com",
  "pin": "1234"
}
```
- Send → Check Response

---

## 🔍 Testing Checklist

### ✅ Basic Tests
- [ ] `/ping` returns 200 with database status
- [ ] `/register` creates new user
- [ ] `/user/<username>` retrieves user info
- [ ] `/contact` adds emergency contact
- [ ] `/contacts/<username>` lists all contacts

### ✅ Location Tests
- [ ] `/analyze` analyzes location and logs
- [ ] `/locations/<username>` shows history
- [ ] Location validation works (invalid coords return 400)

### ✅ Emergency Tests
- [ ] `/sos` triggers alert
- [ ] Console shows "SOS RECEIVED FROM:"
- [ ] Firebase sends notification (if configured)

### ✅ Error Tests
- [ ] Missing username returns 400
- [ ] Invalid email returns 400
- [ ] Invalid coordinates return 400
- [ ] Invalid PIN returns 400

### ✅ Database Tests
- [ ] Data persists after restart
- [ ] Multiple users can register
- [ ] Multiple contacts per user work
- [ ] Location history is stored

---

## 📊 Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | User registered successfully |
| 400 | Bad Request | Missing username or invalid data |
| 401 | Unauthorized | Not implemented yet |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Firebase connection failed |
| 503 | Unavailable | Database connection lost |

---

## 🐛 Debugging Tips

### Check Logs
```bash
tail -f logs/safeher_errors.log     # Real-time error logs
cat logs/safeher_*.log               # View all logs
```

### Test Database Connection
```bash
python
>>> from database import get_connection
>>> conn = get_connection()
>>> print("Connected!" if conn else "Failed")
```

### Verify Imports
```bash
python test_backend.py
```

### Check Running Process
```bash
ps aux | grep python    # See if app.py is running
lsof -i :5000          # See what's using port 5000
```

---

## ⚠️ Common Issues

### Issue: Connection Refused
**Problem:** `Error: [Errno 111] Connection refused`
**Solution:** Start the server first
```bash
python app.py
```

### Issue: Database Connection Failed
**Problem:** `MySQL Error: Access denied`
**Solution:** Check .env file
```bash
cat .env
# Verify DB_HOST, DB_USER, DB_PASSWORD
```

### Issue: Port Already in Use
**Problem:** `Address already in use`
**Solution:** Kill existing process
```bash
lsof -i :5000           # Find process
kill -9 <PID>           # Kill it
python app.py           # Restart
```

### Issue: Module Not Found
**Problem:** `ModuleNotFoundError: No module named 'mysql'`
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🎯 Test Scenarios

### Scenario 1: New User Registration
```
1. Register user with POST /register
2. Verify with GET /user/<username>
3. Expected: User data returned
```

### Scenario 2: Emergency Contacts
```
1. Register user
2. Add 3 contacts with POST /contact
3. Retrieve with GET /contacts/<username>
4. Expected: All 3 contacts returned
```

### Scenario 3: Location Tracking
```
1. Register user
2. Submit 5 different locations with POST /analyze
3. Retrieve with GET /locations/<username>?limit=10
4. Expected: 5 location records in reverse order
```

### Scenario 4: Risk Detection
```
1. Test at 11 AM: lat=12.5, lng=77.5
   Expected: "Low" risk
2. Test at 11 PM: same coordinates
   Expected: "High" risk (night time)
3. Test in danger zone: lat=12.5, lng=77.5
   Expected: "Medium" risk (isolated zone)
```

---

## ✅ Success Criteria

Your backend is working correctly when:

✅ All 10 tests pass
✅ No errors in logs
✅ Response times < 500ms
✅ Database operations succeed
✅ Validation works on invalid input
✅ Error messages are descriptive
✅ Health check shows "Connected"
✅ Logs are created daily

---

## 📞 Need Help?

1. Check logs: `logs/safeher_errors.log`
2. Read README.md for API details
3. Review test_backend.py for examples
4. Check DEPLOYMENT.md for setup issues

---

**Happy Testing! 🚀**
