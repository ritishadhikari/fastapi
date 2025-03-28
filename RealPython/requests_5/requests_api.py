import requests
from typing import Optional
from pydantic import BaseModel
import json


url = "http://localhost:8000/items/"
headers = {"Content-Type": "application/json"}
data = {"name": "ritish","description": "about myself","price": 100.0,"tax": 10.0}

response = requests.post(url=url, 
                         headers=headers, 
                         data=json.dumps(data))
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
