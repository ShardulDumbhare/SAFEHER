import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Shivam@14032005',
        database='zoha'
    )
    cursor = conn.cursor()
    
    # Get all routines
    cursor.execute('SELECT * FROM routines')
    rows = cursor.fetchall()
    print(f'✓ Found {len(rows)} routines in database:\n')
    
    for row in rows:
        print(f'ID: {row[0]}')
        print(f'  Username: {row[1]}')
        print(f'  Title: {row[2]}')
        print(f'  Time: {row[3]} - {row[4]}')
        print(f'  Location: {row[5]}')
        print(f'  Days: {row[6]}')
        print(f'  Created: {row[7]}')
        print()
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
