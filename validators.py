"""
Input Validators - Validate all user inputs before database operations
"""
import re

def validate_username(username):
    """Validate username (3-50 chars, alphanumeric + underscore)"""
    if not username or len(username) < 3 or len(username) > 50:
        return False, "Username must be 3-50 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Valid"

def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    return True, "Valid"

def validate_pin(pin):
    """Validate PIN (4-6 digits)"""
    if not pin or len(pin) < 4 or len(pin) > 6:
        return False, "PIN must be 4-6 digits"
    if not pin.isdigit():
        return False, "PIN must contain only digits"
    return True, "Valid"

def validate_contact_phone(contact):
    """Validate phone number (10-15 digits)"""
    if not contact:
        return False, "Contact is required"
    # Remove common formatting characters
    clean_contact = re.sub(r'[-()\s+]', '', contact)
    if not clean_contact.isdigit():
        return False, "Contact must be numeric (with optional formatting)"
    if len(clean_contact) < 10 or len(clean_contact) > 15:
        return False, "Contact must be 10-15 digits"
    return True, "Valid"

def validate_coordinates(lat, lng):
    """Validate latitude and longitude"""
    try:
        lat = float(lat)
        lng = float(lng)
    except (ValueError, TypeError):
        return False, "Coordinates must be numbers"
    
    if lat < -90 or lat > 90:
        return False, "Latitude must be between -90 and 90"
    if lng < -180 or lng > 180:
        return False, "Longitude must be between -180 and 180"
    
    return True, "Valid"

def validate_accuracy(accuracy):
    """Validate location accuracy"""
    try:
        accuracy = float(accuracy)
    except (ValueError, TypeError):
        return False, "Accuracy must be a number"
    
    if accuracy < 0:
        return False, "Accuracy cannot be negative"
    if accuracy > 10000:
        return False, "Accuracy seems invalid (> 10km)"
    
    return True, "Valid"

def validate_name(name):
    """Validate name (2-100 chars, letters and spaces)"""
    if not name or len(name) < 2 or len(name) > 100:
        return False, "Name must be 2-100 characters"
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    return True, "Valid"

def validate_relation(relation):
    """Validate relation field (optional, max 50 chars)"""
    if relation and len(relation) > 50:
        return False, "Relation must be less than 50 characters"
    return True, "Valid"
