import json

import file
import database

#Change .. to Bullboard when finished

def login():
    body = file.read_file("../frontend/pages/login.html")
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
    queryMap = {'email': data.get('email'), 'password': data.get('password')}
    if database.verify_login(queryMap):
        #Create login token on successful login
        # login_token()
        return [b"User Found", 200, "text/plain"]
    else:
        return [b"Content Not Found", 404, "text/plain"]

def create_account(data):
    return
