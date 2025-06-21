import requests

API_URL = "http://127.0.0.1:8000"

def fetch(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}")
    return response.json() if response.status_code == 200 else []

def post(endpoint, data):
    response = requests.post(f"{API_URL}/{endpoint}", json=data)
    return response
