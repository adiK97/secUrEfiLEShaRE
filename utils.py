import bcrypt
from basicauth import encode
import json

resource_file = "ftpServer/passwords.json"

def encode(username,password):
    return (bcrypt.hashpw((username+password).encode('utf-8'), bcrypt.gensalt())).decode('utf-8')

def add_user(username,password):
    with open(resource_file, "r") as openfile:
        passw  = json.load(openfile)

    if username in passw.keys():
        raise Exception(username)
    else:
        passw[username] = str(encode(username,password))
        with open(resource_file, "w") as outfile:
            json.dump(passw, outfile)
        return username

def check_login(username,password):
    with open(resource_file, "r") as openfile:
        passw  = json.load(openfile)
    if username in passw.keys():
        check =(username+password).encode('utf-8')
        test = passw[username].encode('utf-8')
        if bcrypt.checkpw(check, test):
            return username
    return

def create_username(username,password):
     print(username)
     try: 
         username = add_user(username,password)
         print("Added User! %s"%username)
     except Exception as e:
         print("Failed to add user %s! ... user already exists??"%username)

def login(username,password):
     if check_login(username,password):
        return True
     else:
        return False

def create_group():
    pass