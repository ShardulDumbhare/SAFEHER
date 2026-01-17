import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Shivam@14032005',
        database='zoha'
    )
    cursor = conn.cursor()
    
    # Check if routines table exists
    cursor.execute("SHOW TABLES LIKE 'routines'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print('✓ Routines table EXISTS')
        cursor.execute('DESCRIBE routines')
        cols = cursor.fetchall()
        print('Table structure:')
        for col in cols:
            print(f'  {col[0]}: {col[1]}')
        
        # Check for data
        cursor.execute('SELECT COUNT(*) FROM routines')
        count = cursor.fetchone()[0]
        print(f'\nData in table: {count} rows')
    else:
        print('✗ Routines table DOES NOT EXIST')
        print('Creating routines table now...')
        cursor.execute('''
            CREATE TABLE routines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                time_from TIME NOT NULL,
                time_to TIME NOT NULL,
                location VARCHAR(255),
                days VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES user_details(username) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        print('✓ Routines table CREATED successfully')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
