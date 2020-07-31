import random
import string

# get random string password with letters, digits, and symbols
def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(length))
    print("Random string password is:", password)

    f = open("data.json", "a")
    f.write({"a":"b"})
    f.close()
    # f.write(str({
    # "name": "qradar",
    # "type": "source",
    # "pid": password,
    # "fields": {
    #     "common": ["ip"],
    #     "credentials": ["token"],
    # },
    # "runner_script": "qradar/qradar_parham_getter.py",
    # "version": "7.3.0",
    # }))
    # f.close()

    #open and read the file after the appending:
    f = open("data.json", "r")
    print(f.readlines())

get_random_password_string(8)