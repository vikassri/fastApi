import requests
from faker import Faker
import json

fake = Faker()

for _ in range(0):
    req = requests.post(f'http://localhost:8000/register/?name={fake.name()}')
    if req.status_code == 200:
        print("successfully registered")
    else:
        print("Failed to register")

req = requests.get(f'http://localhost:8000/register')
for name in req.json():
    print(name)
