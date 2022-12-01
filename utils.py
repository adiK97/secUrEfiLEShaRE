import bcrypt
from basicauth import encode
import json
from flask import Flask, request, redirect, send_from_directory, make_response
import ftplib
import dotenv
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

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


@app.route('/file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    authUsers = request.form['users'].split(",")
    print(uploaded_file, authUsers, type(authUsers))
    print(uploaded_file.filename)
    if not uploaded_file.filename == "":
        uploaded_file.save(uploaded_file.filename)

        key = Fernet.generate_key()
        f = Fernet(key)

        with open(uploaded_file.filename, 'rb') as original_file:
            original = original_file.read()
        encrypted = f.encrypt(original)

        with open ("enc_"+uploaded_file.filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        uploadedFiles.append(uploaded_file.filename)
        ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("uname"),os.getenv("pass") )
        ftp_server.encoding = "utf-8"
        with open("enc_"+uploaded_file.filename, "rb") as file:
            ftp_server.storbinary(f"STOR {uploaded_file.filename}", file)
        ftp_server.quit()

        with open("ftpServer/fileDetails.json", "r") as openfile:
            files  = json.load(openfile)

        files[uploaded_file.filename] = {"key":key.decode('utf-8'),"users":authUsers}

        with open("ftpServer/fileDetails.json", "w") as outfile:
            json.dump(files, outfile)
        return {'result':True}
    return {"result":False}


@app.route('/fileList', methods=['GET'])
def fileList():
    return uploadedFiles


@app.route('/download', methods=['POST'])
def download_file():
    data = request.get_json(force=True)
    filename = data["filename"]
    username = data["username"]
    with open("ftpServer/fileDetails.json", "r") as openfile:
        files  = json.load(openfile)
    
    if not filename in uploadedFiles or not username in files[filename]["users"]:
        print(filename in uploadedFiles)
        print(username in files[filename]["users"])
        return {"result":False}

    f = Fernet(files[filename]["key"].encode('utf-8'))

    ftp_server = ftplib.FTP(os.getenv("HOSTNAME"), os.getenv("uname"),os.getenv("pass") )
    ftp_server.encoding = "utf-8"    
    with open("downloaded_"+filename, "wb") as file:
    # Command for Downloading the file "RETR filename"
        ftp_server.retrbinary(f"RETR {filename}", file.write)
        
    with open("downloaded_"+filename, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)
    with open("Dec_downloaded_"+filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    response = make_response(send_from_directory("","Dec_downloaded_"+filename , as_attachment=True))
    response.headers['X-filename'] = filename
    return response
    # return send_from_directory("","Dec_downloaded_"+filename , as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)