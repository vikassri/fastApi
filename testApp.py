import requests, os
from faker import Faker
from pprint import pprint

fake = Faker()
hostname = os.uname()[1]

def create_users():
    for _ in range(5):
        req = requests.post(f'http://{hostname}:8000/register/?name={fake.name()}&email={fake.email()}&password={fake.password()}')
        if req.status_code == 200:
            print("successfully registered")
        else:
            print("Failed to register")

if __name__=='__main__':
#    create_users()
    req = requests.get(f'http://{hostname}:8000/register')
    for name in req.json():
        pprint(name)
