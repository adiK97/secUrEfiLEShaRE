import bcrypt
from basicauth import encode
import json
from flask import Flask, request
import ftplib
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


resource_file = "ftpServer/passwords.json"

def encode(username,password):
    return (bcrypt.hashpw((username+password).encode('utf-8'), bcrypt.gensalt())).decode('utf-8')

def add_user(username,password):
    with open(resource_file, "r") as openfile:
        passw  = json.load(openfile)

    if username in passw.keys():
        return "Failed"
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
        print("tes")
        print(test)
        if bcrypt.checkpw(check, test):
            return username
    return


@app.route('/addUser', methods=['GET', 'POST'])
def create_username():
    data = request.get_json(force=True)
    username,password = data["username"] , data["password"]
    if add_user(username,password):
         return username
    else:
        return "Failed"


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json(force=True)
    username,password = data["username"] , data["password"]
    if check_login(username,password):
        connectFTP()
        return username
    else:
       return "Failed"

def connectFTP():
    ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("USERNAME"),os.getenv("PASSWORD") )
    ftp_server.encoding = "utf-8"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)