import random
import string
import json


def get_random_password_string(length):
    # password_characters = string.ascii_letters + string.digits + string.punctuation
    password_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_characters) for i in range(length))
    print("Random string password is:", password)
    data = {"name": "qradar", "type": "source", "pid": password,
            "fields": {
                "common": ["ip"],
                "credentials": ["token"],
            }}
    actual_json = json.dumps(data)
    print(json.dumps(data))
    f = open("qradar/data.json", "w")
    f.write(actual_json)
    f.close()

    # open and read the file after the appending:
    f = open("qradar/data.json", "r")
    print(f.read())


get_random_password_string(8)
