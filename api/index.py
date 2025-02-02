# api/index.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os

def load_students_data():
    # Get the root directory (where vercel.json is located)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(root_dir, 'q-vercel-python.json')
    
    try:
        with open(json_path, 'r') as file:
            students_data = json.load(file)
            # Create a lookup dictionary for faster access
            return {student["name"]: student["marks"] for student in students_data}
    except Exception as e:
        print(f"Error loading students data: {e}")
        return {}

# Load the data when the module is imported
STUDENTS_DICT = load_students_data()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL and query parameters
        url = urlparse(self.path)
        query_params = parse_qs(url.query)
        
        # Get names from query parameters
        names = query_params.get('name', [])
        
        # Get marks for each name
        result = []
        for name in names:
            marks = STUDENTS_DICT.get(name, None)
            result.append(marks)
            
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
        return