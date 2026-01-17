"""
DB Adapter - Clean interface to database operations
Exposes high-level functions for app.py to use
"""
from database import (
    insert_user,
    insert_contact,
    insert_location,
    insert_sos,
    get_user
)
from validators import (
    validate_username,
    validate_email,
    validate_pin,
    validate_contact_phone,
    validate_coordinates,
    validate_accuracy,
    validate_name,
    validate_relation
)

def log_user(username, password, email, pin):
    """Log new user to database with validation"""
    # Validate all inputs
    valid, msg = validate_username(username)
    if not valid:
        return False, f"Username error: {msg}"
    
    valid, msg = validate_email(email)
    if not valid:
        return False, f"Email error: {msg}"
    
    valid, msg = validate_pin(pin)
    if not valid:
        return False, f"PIN error: {msg}"
    
    try:
        insert_user(username, password, email, pin)
        return True, "User registered successfully"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def log_contact(username, name, relation, contact):
    """Log new contact for user with validation"""
    # Validate all inputs
    valid, msg = validate_username(username)
    if not valid:
        return False, f"Username error: {msg}"
    
    valid, msg = validate_name(name)
    if not valid:
        return False, f"Name error: {msg}"
    
    valid, msg = validate_relation(relation)
    if not valid:
        return False, f"Relation error: {msg}"
    
    valid, msg = validate_contact_phone(contact)
    if not valid:
        return False, f"Contact error: {msg}"
    
    try:
        insert_contact(username, name, relation, contact)
        return True, "Contact added successfully"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def log_location(username, lat, lng, accuracy):
    """Log location with accuracy and validation"""
    # Validate inputs
    valid, msg = validate_username(username)
    if not valid:
        return False, f"Username error: {msg}"
    
    valid, msg = validate_coordinates(lat, lng)
    if not valid:
        return False, f"Coordinates error: {msg}"
    
    valid, msg = validate_accuracy(accuracy)
    if not valid:
        return False, f"Accuracy error: {msg}"
    
    try:
        insert_location(username, lat, lng, accuracy)
        return True, "Location logged successfully"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def log_sos(username):
    """Log SOS event with validation"""
    valid, msg = validate_username(username)
    if not valid:
        return False, f"Username error: {msg}"
    
    try:
        insert_sos(username)
        return True, "SOS logged successfully"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def user_exists(username):
    """Check if user exists"""
    valid, msg = validate_username(username)
    if not valid:
        return False
    
    try:
        return get_user(username) is not None
    except Exception as e:
        print(f"Error checking user: {e}")
        return False

