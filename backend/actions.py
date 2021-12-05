import json
import file
import database
import functions

#Change .. to Bullboard when finished

read_file_string = "../"

def login():
    body = file.read_file(read_file_string + "frontend/pages/index.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# We want to serve the register page here.
def register():
    body = file.read_file(read_file_string + "frontend/pages/create_account.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Respond to HTML paths here.
def resp_to_html_paths(request):
    path = request.path
    body = file.read_file(read_file_string + "frontend/pages%s" % path)
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
        token = functions.login_token()
        database.store_token(data['email'], token)
        header = {'Set-Cookie': 'token=' + token + '; Max-Age=3600; HttpOnly'}
        return [header, b"User Found", 200, "text/plain"]
    else:
        return ["", b"Content Not Found", 404, "text/plain"]

def create_account(data):
    if functions.verify_password(data['password'], data['rePassword']):
        database.add_user(data)
        return [b"", b"User Added", 201, "text/plain"]
    else:
        return [b"", b"Password does not meet all requirements or does not match", 404, "text/plain"]

#Loads newsfeed
def newsfeed():
    body = file.read_file(read_file_string + "frontend/pages/newsfeed.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

#Loads user profile
def profile(request):
    token = request.cookies.get('token')
    if token:
        body = functions.load_profile(token)
        if body:
            response_code = 200
            content_type = "text/html"
            return [body, response_code, content_type]
        else:
            return [b"", b"You must log in", 403, "text/plain"]
    else:
        return [b"", b"You must log in", 403, "text/plain"]


def add_post(request):
    return

def update_account(request):

    return
