import json
import secrets
import file
import database
import re

#Change .. to Bullboard when finished

def login():
    body = file.read_file("../frontend/pages/index.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# We want to serve the register page here.
def register():
    body = file.read_file("../frontend/pages/create_account.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Respond to HTML paths here.
def resp_to_html_paths(path):
    if path.startswith("images"):
        body = file.read_file("../frontend/%s" % path)
    else:
        body = file.read_file("../frontend/pages%s" % path)
    response_code = 200
    if path.endswith(".css"):
        return [body, response_code, "text/css"]
    elif path.endswith(".js"):
        return [body, response_code, "text/javascript"]
    elif path.endswith(".png"):
        return [body, response_code, "image/png"]
    else:
        return [body, response_code, "image/jpeg"]

def login_attempt(data):
    if database.verify_login(data):
        #Create login token on successful login
        token = login_token()
        database.store_token(data['email'], token)
        header = {'Set-Cookie': 'token=' + token + '; Max-Age=3600; HttpOnly'}
        return [header, b"User Found", 200, "text/plain"]
    else:
        return ["", b"Content Not Found", 404, "text/plain"]

def create_account(data):
    if verify_password(data['password'], data['rePassword']):
        database.add_user(data)
        return [b"", b"User Added", 201, "text/plain"]
    else:
        return [b"", b"Password does not meet all requirements or does not match", 404, "text/plain"]

def verify_password(password, password2):
    if password != password2:
        return False
    if re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
        return True
    else:
        return False

def login_token():
    return secrets.token_hex(16)
