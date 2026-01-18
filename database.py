import mysql.connector
from mysql.connector import pooling
import os
from datetime import datetime
from logger import info, error, debug

# MySQL Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Shivam@14032005'),
    'database': os.getenv('DB_NAME', 'zoha')
}

# Create connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="safeher_pool",
        pool_size=10,
        pool_reset_session=True,
        **DB_CONFIG
    )
    info("Connection pool created successfully")
except Exception as e:
    error(f"Connection pool error: {e}")
    connection_pool = None

def get_connection():
    """Get connection from pool"""
    if connection_pool:
        return connection_pool.get_connection()
    else:
        # Fallback to direct connection if pool fails
        return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialize database with required tables"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create user_details table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_details (
                username VARCHAR(255) PRIMARY KEY,
                password TEXT NOT NULL,
                email VARCHAR(255) NOT NULL,
                pin VARCHAR(10) NOT NULL
            )
        ''')
        
        # Create contact_details table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                relation VARCHAR(100),
                contact VARCHAR(20) NOT NULL,
                FOREIGN KEY (username) REFERENCES user_details(username)
            )
        ''')
        
        # Create location table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS location (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                latitude DOUBLE,
                longitude DOUBLE,
                accuracy FLOAT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES user_details(username)
            )
        ''')
        
        # Create sos_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sos_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES user_details(username)
            )
        ''')
        
        conn.commit()
        cursor.close()
    except Exception as e:
        error(f"Error initializing database: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_user(username, password, email, pin):
    """Insert a new user into user_details table"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_details (username, password, email, pin) VALUES (%s, %s, %s, %s)',
            (username, password, email, pin)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        error(f"Error inserting user: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_contact(username, name, relation, contact):
    """Insert a contact for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Convert phone to integer, taking last 9 digits if needed to fit INT
        phone_str = str(contact).replace('+', '').replace('-', '').replace(' ', '')
        # If phone number is too long, take last 9 digits (for INT max value ~2.1 billion)
        if len(phone_str) > 9:
            phone_int = int(phone_str[-9:])
        else:
            phone_int = int(phone_str)
        
        cursor.execute(
            'INSERT INTO emergency_contacts (`contact-name`, `contact-phone`, `contact-relation`) VALUES (%s, %s, %s)',
            (name, phone_int, relation)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        error(f"Error inserting contact: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_location(username, latitude, longitude, accuracy):
    """Insert location data for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO location (username, latitude, longitude, accuracy) VALUES (%s, %s, %s, %s)',
            (username, latitude, longitude, accuracy)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        error(f"Error inserting location: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_sos(username):
    """Log an SOS call"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sos_logs (username) VALUES (%s)',
            (username,)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        error(f"Error logging SOS: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_user(username):
    """Get user details by username"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        error(f"Error getting user: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_user_contacts(username):
    """Get all contacts for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT `contact-name`, `contact-relation`, `contact-phone` FROM emergency_contacts', ())
        results = cursor.fetchall()
        cursor.close()
        return [{"name": r[0], "relation": r[1], "contact": str(r[2])} for r in results]
    except Exception as e:
        error(f"Error getting contacts: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_user_locations(username, limit=50):
    """Get location history for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT latitude, longitude, accuracy, timestamp 
            FROM location 
            WHERE username = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        ''', (username, limit))
        results = cursor.fetchall()
        cursor.close()
        return [{"latitude": r[0], "longitude": r[1], "accuracy": r[2], "timestamp": str(r[3])} for r in results]
    except Exception as e:
        error(f"Error getting locations: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_routine(username, title, time_from, time_to, location, days):
    """Insert a routine for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO routines (username, title, time_from, time_to, location, days, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())',
            (username, title, time_from, time_to, location, days)
        )
        conn.commit()
        cursor.close()
        return True, "Routine saved successfully"
    except Exception as e:
        error(f"Error inserting routine: {e}")
        return False, str(e)
    finally:
        if conn:
            conn.close()

def get_user_routines(username):
    """Get all routines for a user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, title, time_from, time_to, location, days FROM routines WHERE username = %s ORDER BY time_from ASC',
            (username,)
        )
        results = cursor.fetchall()
        cursor.close()
        return [{"id": r[0], "title": r[1], "timeFrom": str(r[2]), "timeTo": str(r[3]), "location": r[4], "days": r[5]} for r in results]
    except Exception as e:
        error(f"Error getting routines: {e}")
        return []
    finally:
        if conn:
            conn.close()

def delete_routine(routine_id):
    """Delete a routine by ID"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM routines WHERE id = %s', (routine_id,))
        conn.commit()
        cursor.close()
        return True, "Routine deleted successfully"
    except Exception as e:
        error(f"Error deleting routine: {e}")
        return False, str(e)
    finally:
        if conn:
            conn.close()

def check_location_against_routine(username, current_lat, current_lon):
    """
    Check if user's current location matches their routine location for current time.
    Returns: (is_at_correct_location, routine_info, distance_km)
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all routines for user
        cursor.execute(
            'SELECT id, title, time_from, time_to, location FROM routines WHERE username = %s',
            (username,)
        )
        routines = cursor.fetchall()
        cursor.close()
        
        from datetime import datetime
        current_time = datetime.now().time()
        
        # Check if user is currently in a scheduled routine
        for routine in routines:
            routine_id, title, time_from, time_to, routine_location = routine
            
            # Check if current time falls within routine time
            if time_from <= current_time <= time_to:
                # Calculate distance between current location and routine location
                distance = calculate_distance(current_lat, current_lon, routine_location)
                
                # If routine has specific location and user is far (>1km), it's a mismatch
                if routine_location and distance is not None and distance > 1.0:
                    return False, {
                        "routine_id": routine_id,
                        "title": title,
                        "location": routine_location,
                        "time_from": str(time_from),
                        "time_to": str(time_to)
                    }, distance
                elif routine_location and distance is not None:
                    return True, {
                        "routine_id": routine_id,
                        "title": title,
                        "location": routine_location,
                        "distance_km": round(distance, 2)
                    }, distance
        
        # No active routine at this time
        return True, None, 0
        
    except Exception as e:
        error(f"Error checking location against routine: {e}")
        return None, None, None
    finally:
        if conn:
            conn.close()

def calculate_distance(lat1, lon1, location_name):
    """
    Calculate distance from coordinates to a location name.
    For now, returns a placeholder - can integrate with geocoding API later.
    Returns distance in kilometers.
    """
    try:
        # This is a simplified version - in production, you'd use geocoding
        # to convert location_name to coordinates, then calculate distance
        
        # For now, we'll just return None if location_name is not specific coordinates
        # In future, integrate with Google Maps or similar API
        
        # Simple check: if location_name contains coordinates format
        if "," in str(location_name):
            try:
                parts = location_name.split(",")
                loc_lat = float(parts[0].strip())
                loc_lon = float(parts[1].strip())
                
                # Haversine formula to calculate distance
                from math import radians, sin, cos, sqrt, atan2
                
                R = 6371  # Earth's radius in kilometers
                
                lat1_rad = radians(float(lat1))
                lon1_rad = radians(float(lon1))
                lat2_rad = radians(loc_lat)
                lon2_rad = radians(loc_lon)
                
                dlat = lat2_rad - lat1_rad
                dlon = lon2_rad - lon1_rad
                
                a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                
                distance = R * c
                return distance
            except:
                return None
        return None
    except Exception as e:
        error(f"Error calculating distance: {e}")
        return None

# Initialize database on import
try:
    init_db()
    info("MySQL database initialized successfully")
except Exception as e:
    error(f"MySQL connection warning: {e}")
    error("Make sure MySQL is running and credentials are correct in environment variables")
