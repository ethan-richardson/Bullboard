import json
import file
import database
import functions

#Change this based on your file extensions
read_file_string = "../"

# Serves the login page
def login(request):
    body = file.read_file(read_file_string + "frontend/pages/index.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Serves the registration page
def register(request):
    body = file.read_file(read_file_string + "frontend/pages/create_account.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Serves respective user profile
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

# Serves the edit profile page
def edit(request):
    body = file.read_file(read_file_string + "frontend/pages/edit_profile.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]


# Serves the newsfeed with posts
def newsfeed(request):
    body = file.read_file(read_file_string + "frontend/pages/newsfeed.html")
    newsfeed_elements = functions.create_post_elements()
    body = body.replace(b'{{posts}}', newsfeed_elements.encode())
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Serves the interactive map
def map(request):
    body = file.read_file(read_file_string + "frontend/pages/live_map.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Serves the direct messages
def messages(request):
    body = file.read_file(read_file_string + "frontend/pages/direct_messages.html")
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

# Handles login attempts
def login_attempt(request, data):
    if database.verify_login(data):
        #Create login token on successful login
        token = functions.login_token()
        database.store_token(data['email'], token)
        header = {'Set-Cookie': 'token=' + token + '; Max-Age=3600; HttpOnly'}
        return [header, b"User Found", 200, "text/plain"]
    else:
        return ["", b"Content Not Found", 404, "text/plain"]

# Handles account creation
def create_account(request, data):
    if functions.verify_password(data['password'], data['rePassword']):
        database.add_user(data)
        return [b"", b"User Added", 201, "text/plain"]
    else:
        return [b"", b"Password does not meet all requirements or does not match", 404, "text/plain"]

#Loads newsfeed
def newsfeed(request):
    body = file.read_file_as_list(read_file_string + "frontend/pages/newsfeed.html")
    authenticated = []
    idx = body.index('    <div id="list">\n')
    collection = database.fetch_all()
    for doc in collection:
        if len(doc["Token"]) != 0:
            authenticated.append(doc["Email"])
            # TODO - Insert HTML here in newsfeed page.
    for user in authenticated:
        if user not in body[idx+1]:
           body[idx+1] = user + body[idx+1]
    encoded = ''.join(ele for ele in body).encode()
    response_code = 200
    content_type = "text/html"
    return [encoded, response_code, content_type]

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
