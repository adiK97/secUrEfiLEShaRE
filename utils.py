import bcrypt
from basicauth import encode
import json
from flask import Flask, request, redirect, send_from_directory
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
        if bcrypt.checkpw(check, test):
            return username
    return


@app.route('/addUser', methods=['GET', 'POST'])
def create_username():
    data = request.get_json(force=True)
    username,password = data["username"] , data["password"]
    if add_user(username,password):
        return {"result":True, "username":username}
    else:
        return {"result":False}


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json(force=True)
    username,password = data["username"] , data["password"]
    if check_login(username,password):
        return {"result":True,"username":username}
    else:
        return {"result":False}

# def connectFTP():
#     global ftp_server
#     ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("USERNAME"),os.getenv("PASSWORD") )
#     ftp_server.encoding = "utf-8"


@app.route('/file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    print(uploaded_file)
    print(uploaded_file.filename)
    if not uploaded_file.filename == "":
        uploaded_file.save(uploaded_file.filename)
        uploadedFiles.append(uploaded_file.filename)
        ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("uname"),os.getenv("pass") )
        ftp_server.encoding = "utf-8"
        with open(uploaded_file.filename, "rb") as file:
            ftp_server.storbinary(f"STOR {uploaded_file.filename}", file)
        ftp_server.quit()
        return {'result':True}
    return {"result":False}


@app.route('/fileList', methods=['GET'])
def fileList():
    return uploadedFiles


@app.route('/file', methods=['GET'])
def download_file():
    data = request.get_json(force=True)
    filename = data["filename"]
    if not filename in uploadedFiles:
        return {"result":False}

    ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("uname"),os.getenv("pass") )
    ftp_server.encoding = "utf-8"    
    with open(filename, "wb") as file:
    # Command for Downloading the file "RETR filename"
        ftp_server.retrbinary(f"RETR {filename}", file.write)
    return send_from_directory("",filename , as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)