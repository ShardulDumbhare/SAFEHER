from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from ai_engine import run_ai_risk_check
from db_adapter import log_location, log_sos, log_user, log_contact, user_exists
from database import get_user, get_user_contacts, get_user_locations, get_connection
from logger import info, error, warning, debug
import firebase_admin
from firebase_admin import credentials, messaging

# --- 1. INITIALIZATION ---
app = Flask(__name__)
CORS(app)

# --- 2. FIREBASE SETUP (With Error Protection) ---
current_directory = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_directory, "firebase_key.json")

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
    info("Firebase is connected and ready!")
except Exception as e:
    error(f"Firebase initialization error: {e}")
    error("Make sure 'firebase_key.json' is in the same folder as app.py")

# --- 3. ERROR HANDLER ---
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "Endpoint does not exist"}), 404

@app.errorhandler(500)
def internal_error(error):
    error(f"Internal Server Error: {error}")
    return jsonify({"error": "Internal Server Error", "message": "Please try again later"}), 500

# --- 4. API ENDPOINTS ---

@app.route('/ping', methods=['GET'])
def ping():
    """Health check with database connectivity verification"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        info("Health check passed")
        return jsonify({
            "status": "Online",
            "project": "SAFEHER",
            "database": "Connected",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        error(f"Health check failed: {e}")
        return jsonify({
            "status": "Online",
            "project": "SAFEHER",
            "database": "Disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503

@app.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    pin = data.get('pin')
    
    # Validate all required fields
    if not all([username, password, email, pin]):
        warning(f"Registration attempt with missing fields: {username}")
        return jsonify({"error": "Missing required fields: username, password, email, pin"}), 400
    
    # Log attempt
    debug(f"Registration attempt for username: {username}")
    
    # Register user
    success, message = log_user(username, password, email, pin)
    
    if success:
        info(f"User registered successfully: {username}")
        return jsonify({"status": "Success", "message": message}), 201
    else:
        warning(f"Registration failed for {username}: {message}")
        return jsonify({"error": "Registration failed", "message": message}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze location safety"""
    data = request.get_json() or {}
    username = data.get('username')
    lat = data.get('lat')
    lng = data.get('lng')
    accuracy = data.get('accuracy', 0)
    
    # Validate username
    if not username:
        warning("Analyze request without username")
        return jsonify({"error": "Username required"}), 400
    
    # Validate location
    if lat is None or lng is None:
        warning(f"Analyze request from {username} without location")
        return jsonify({"error": "Location required"}), 400
    
    debug(f"Analyzing location for {username}: lat={lat}, lng={lng}")
    
    # Log location
    success, message = log_location(username, lat, lng, accuracy)
    if not success:
        warning(f"Location logging failed for {username}: {message}")
    
    # Run AI risk check
    risk, reason = run_ai_risk_check(lat, lng)
    
    info(f"Risk analysis completed for {username}: {risk}")
    
    return jsonify({
        "risk_level": risk,
        "reason": reason,
        "time": datetime.now().strftime("%H:%M"),
        "location_logged": success
    }), 200

@app.route('/sos', methods=['POST'])
def trigger_sos():
    """Trigger SOS emergency alert"""
    data = request.get_json() or {}
    username = data.get('username')
    user_name = data.get('name', 'User')
    
    # Validate username
    if not username:
        warning("SOS triggered without username")
        return jsonify({"error": "Username required"}), 400
    
    info(f"🚨 SOS RECEIVED FROM: {username}")
    
    # Log SOS event
    success, message = log_sos(username)
    if not success:
        error(f"SOS logging failed for {username}: {message}")
    
    try:
        # Send Real Push Notification
        msg = messaging.Message(
            notification=messaging.Notification(
                title="🚨 SAFEHER EMERGENCY",
                body=f"SOS Alert: {user_name} needs immediate help!"
            ),
            topic="safety"
        )
        messaging.send(msg)
        info("✅ FCM alert sent")
        return jsonify({"status": "Success", "message": "FCM Alert Sent"}), 200
    except Exception as e:
        error("❌ FCM failed, fallback triggered")
        error(f"ALERT: {username}")
        warning(f"Firebase error: {e}")
        return jsonify({"status": "Error", "message": "FCM failed but SOS logged"}), 500

@app.route('/contact', methods=['POST'])
def add_contact():
    """Add emergency contact"""
    data = request.get_json() or {}
    username = data.get('username')
    name = data.get('name')
    relation = data.get('relation', 'Emergency Contact')
    contact = data.get('contact')
    
    # Validate required fields
    if not all([username, name, contact]):
        warning("Add contact request with missing fields")
        return jsonify({"error": "Missing required fields: username, name, contact"}), 400
    
    debug(f"Adding contact for {username}: {name}")
    
    # Add contact
    success, message = log_contact(username, name, relation, contact)
    
    if success:
        info(f"Contact added for {username}: {name}")
        return jsonify({"status": "Success", "message": message}), 201
    else:
        warning(f"Contact addition failed for {username}: {message}")
        return jsonify({"error": "Failed to add contact", "message": message}), 400

@app.route('/contacts/<username>', methods=['GET'])
def get_contacts(username):
    """Get all emergency contacts for a user"""
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    debug(f"Fetching contacts for {username}")
    
    try:
        contacts = get_user_contacts(username)
        info(f"Retrieved {len(contacts)} contacts for {username}")
        return jsonify({
            "username": username,
            "contacts": contacts,
            "count": len(contacts)
        }), 200
    except Exception as e:
        error(f"Error fetching contacts for {username}: {e}")
        return jsonify({"error": "Failed to fetch contacts", "message": str(e)}), 500

@app.route('/locations/<username>', methods=['GET'])
def get_locations(username):
    """Get location history for a user"""
    limit = request.args.get('limit', 50, type=int)
    
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    if limit > 1000 or limit < 1:
        return jsonify({"error": "Limit must be between 1 and 1000"}), 400
    
    debug(f"Fetching last {limit} locations for {username}")
    
    try:
        locations = get_user_locations(username, limit)
        info(f"Retrieved {len(locations)} location records for {username}")
        return jsonify({
            "username": username,
            "locations": locations,
            "count": len(locations)
        }), 200
    except Exception as e:
        error(f"Error fetching locations for {username}: {e}")
        return jsonify({"error": "Failed to fetch locations", "message": str(e)}), 500

@app.route('/user/<username>', methods=['GET'])
def get_user_info(username):
    """Get user information (username, email)"""
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    debug(f"Fetching user info for {username}")
    
    try:
        user = get_user(username)
        if not user:
            warning(f"User not found: {username}")
            return jsonify({"error": "User not found"}), 404
        
        # Return only safe fields (not password/pin)
        info(f"User info retrieved for {username}")
        return jsonify({
            "username": user[0],
            "email": user[2]
        }), 200
    except Exception as e:
        error(f"Error fetching user {username}: {e}")
        return jsonify({"error": "Failed to fetch user", "message": str(e)}), 500

# --- 5. LAUNCH ---
if __name__ == '__main__':
    info("Starting SAFEHER Flask Application")
    app.run(debug=True, host='0.0.0.0', port=5000)
