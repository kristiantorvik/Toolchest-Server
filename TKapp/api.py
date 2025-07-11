import requests

# Local URL
API_URL = "http://127.0.0.1:8000"

# Fly.io URL
# API_URL = "https://toolchestserver.fly.dev/"
API_KEY = "1234"


def fetch(endpoint):
    response = requests.get(
        f"{API_URL}/{endpoint}",
        headers={"x-api-key": API_KEY})
    return response.json() if response.status_code == 200 else []


def post(endpoint, data):
    headers = {"x-api-key": API_KEY, 'Content-Type': 'application/json'}
    response = requests.post(f"{API_URL}/{endpoint}", json=data, headers=headers)
    return response


def delete(endpoint):
    response = requests.delete(
        f"{API_URL}/{endpoint}",
        headers={"x-api-key": API_KEY})
    return response.json() if response.status_code == 200 else []


def patch(endpoint, data):
    headers = {"x-api-key": API_KEY, 'Content-Type': 'application/json'}
    response = requests.patch(f"{API_URL}/{endpoint}", json=data, headers=headers)
    return response

