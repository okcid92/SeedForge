import sys
sys.path.insert(0, '/home/okcid/Desktop/SeedForge')

import requests
import urllib.parse

# Test direct sans Flask
query = "ubuntu"
url = f"https://yts.mx/api/v2/list_movies.json?query_term={urllib.parse.quote(query)}&limit=5"

print(f"Testing YTS API: {url}")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
except Exception as e:
    print(f"Error: {e}")
