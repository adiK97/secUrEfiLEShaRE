import bcrypt
from basicauth import encode
import json
from flask import Flask, request, redirect
import ftplib
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


resource_file = "ftpServer/passwords.json"
uploadedFiles = []


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
        return {"result":"Successful"}
    else:
        return {"result":"Failed"}


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json(force=True)
    username,password = data["username"] , data["password"]
    if check_login(username,password):
        connectFTP()
        return {"result":"Successful"}
    else:
        return {"result":"Failed"}

def connectFTP():
    global ftp_server
    ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("USERNAME"),os.getenv("PASSWORD") )
    ftp_server.encoding = "utf-8"


# @app.route('/uploadFile', methods=['POST'])
# def upload_file():
#     uploaded_file = request.files['file']
#     print(uploaded_file)
#     print(uploaded_file.filename)
#     if not uploaded_file.filename == "":
#         uploaded_file.save(uploaded_file.filename)
#         uploadedFiles.append(uploaded_file.filename)
#         with open(uploaded_file.filename, "rb") as file:
# # Command for Uploading the file "STOR filename"
#             ftp_server.storbinary(f"STOR {uploaded_file.filename}", file)
#         return "Uploaded"
#     return "Failed"


@app.route('/uploadFile', methods=['GET'])
def fileList():
    return uploadedFiles



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)