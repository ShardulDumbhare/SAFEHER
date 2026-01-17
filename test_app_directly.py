import sys
sys.path.insert(0, 'c:\\Users\\ASUS\\OneDrive\\Desktop\\SAFEHER')

try:
    print("Importing app...")
    from app import app
    print("✓ App imported successfully")
    
    print("\nTesting Flask routes...")
    with app.test_client() as client:
        # Test /ping
        print("Testing /ping...")
        response = client.get('/ping')
        print(f"  Status: {response.status_code}")
        
        # Test /routine POST
        print("Testing /routine POST...")
        response = client.post('/routine', json={
            'username': 'test_user',
            'title': 'Test Routine',
            'timeFrom': '10:00:00',
            'timeTo': '11:00:00',
            'location': 'Test Location',
            'days': 'Mon,Tue'
        })
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.get_json()}")
        
        # Test /routines GET
        print("Testing /routines GET...")
        response = client.get('/routines/test_user')
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.get_json()}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
