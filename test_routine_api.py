import requests
import time
import json

time.sleep(1)

# Test POST /routine
payload = {
    'username': 'demo_user',
    'title': 'Yoga Class',
    'timeFrom': '08:00:00',
    'timeTo': '09:30:00',
    'location': 'Yoga Studio',
    'days': 'Mon,Wed,Fri'
}

print("Testing POST /routine...")
response = requests.post('http://localhost:5000/routine', json=payload)
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')

time.sleep(1)

# Test GET /routines/<username>
print("\nTesting GET /routines/demo_user...")
response = requests.get('http://localhost:5000/routines/demo_user')
print(f'Status: {response.status_code}')
print(json.dumps(response.json(), indent=2))

# Verify in database
print("\n\nVerifying data in database...")
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Shivam@14032005',
    database='zoha'
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM routines WHERE username = %s', ('demo_user',))
rows = cursor.fetchall()
print(f'Found {len(rows)} routines for demo_user:')
for row in rows:
    print(f'  ID: {row[0]}, Title: {row[2]}, Time: {row[3]} - {row[4]}, Location: {row[5]}, Days: {row[6]}')
cursor.close()
conn.close()
