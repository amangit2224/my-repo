import requests

# Login first
print("Logging in...")
login_response = requests.post(
    "http://127.0.0.1:5000/api/auth/login",
    json={"email": "test@example.com", "password": "test123"}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print("Login successful!")
else:
    print(" Login failed!")
    exit()

# Upload file
print("\n Uploading report...")
headers = {"Authorization": f"Bearer {token}"}

# your actual filename
filename = "report1.pdf"  # or report1.jpg

try:
    with open(filename, 'rb') as f:
        files = {'file': f}
        upload_response = requests.post(
            "http://127.0.0.1:5000/api/report/upload",
            headers=headers,
            files=files
        )
    
    print("\nResponse:")
    print(upload_response.json())
    
    if upload_response.status_code == 200:
        print("\n SUCCESS! Report processed!")
    else:
        print("\nUpload failed!")
        
except FileNotFoundError:
    print(f"\nFile '{filename}' not found in backend folder!")
    print("Please copy your medical report to the backend folder and update the filename.")