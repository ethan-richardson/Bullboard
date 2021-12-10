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
    return [None, body, response_code, content_type]

# Serves the registration page
def register(request):
    body = file.read_file(read_file_string + "frontend/pages/create_account.html")
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]

# Serves respective user profile
def profile(request):
    token = request.cookies.get('token')
    if token:
        body = functions.load_profile(token)
        if body:
            response_code = 200
            content_type = "text/html"
            return [None, body, response_code, content_type]
        else:
            return [None, b"You must log in", 403, "text/plain"]
    else:
        return [None, b"You must log in", 403, "text/plain"]

# Serves the edit profile page
def edit(request):
    body = file.read_file(read_file_string + "frontend/pages/edit_profile.html")
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]


# Serves the newsfeed with posts
def newsfeed(request):
    body = functions.load_newsfeed_profile(request.cookies.get('token'))
    newsfeed_elements = functions.create_post_elements()
    body = body.replace(b'{{posts}}', newsfeed_elements.encode())
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]

# Serves the interactive map
def map(request):
    body = file.read_file(read_file_string + "frontend/pages/live_map.html")
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]

# Serves the messages home page
def messages_home(request):
    body = file.read_file(read_file_string + "frontend/pages/messages_home.html")
    token = request.cookies.get('token')
    user = functions.get_user(token)
    user_elements = functions.create_ubit_elements(user)
    body = body.replace(b'{{ubits}}', user_elements.encode())
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]

# Serves the direct messages
def messages(request):
    receiver = functions.get_ubit(request)
    token = request.cookies.get('token')
    user = functions.get_user(token)
    body = file.read_file(read_file_string + "frontend/pages/direct_messages.html")
    if receiver:
        messages = database.get_messages(user['UBIT'], receiver)
        body = body.replace(b'{{current_ubit}}', receiver.encode())
        if messages:
            message_elements = functions.create_messages(messages)
            body = body.replace(b'{{msgs}}', message_elements.encode())
        else:
            body = body.replace(b'{{msgs}}', b'')
    else:
        body = body.replace(b'{{current_ubit}}', b'')
        body = body.replace(b'{{msgs}}', b'')
    user_elements = functions.create_ubit_elements(user)
    body = body.replace(b'{{ubits}}', user_elements.encode())
    response_code = 200
    content_type = "text/html"
    return [None, body, response_code, content_type]

# Respond to HTML paths here.
def resp_to_html_paths(request):
    path = request.path
    body = file.read_file(read_file_string + "frontend/pages%s" % path)
    response_code = 200
    if path.endswith(".css"):
        return [None, body, response_code, "text/css"]
    elif path.endswith(".js"):
        return [None, body, response_code, "text/javascript"]
    elif path.endswith(".png"):
        return [None, body, response_code, "image/png"]
    else:
        return [None, body, response_code, "image/jpeg"]

# Handles logout attempts
def logout(request):
    token = request.cookies.get('token')
    user = functions.get_user(token)
    if user:
        database.process_logout(user)
    headers = {
        'Set-Cookie': 'token=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT',
        'Location': ' /',
    }
    return [headers, None, 302, None]

# Handles login attempts
def login_attempt(request, data):
    user = database.verify_login(data)
    if user:
        #Create login token on successful login
        token = functions.login_token()
        database.store_token(user, token)
        header = {'Set-Cookie': 'token=' + token + '; Max-Age=3600; HttpOnly'}
        return [header, b"User Found", 200, "text/plain"]
    else:
        return ["", b"Content Not Found", 404, "text/plain"]

# Handles account creation
def create_account(request, data):
    if not functions.verify_email(data['email']):
        return [b"", b"Email is not valid or duplicate account exists", 404, "text/plain"]
    if functions.verify_password(data['password'], data['rePassword']):
        database.add_user(data)
        return [b"", b"User Added", 201, "text/plain"]
    else:
        return [b"", b"Password does not meet all requirements or does not match", 404, "text/plain"]

# Handles adding newsfeed post
def add_post(request, data):
    token = request.cookies.get('token')
    user = functions.get_user(token)
    if user:
        database.add_post(user, data)
        response_code = 201
        content_type = "text/html"
        return [b"", b"Post created", response_code, content_type]
    else:
        return [b"", b"You must log in", 403, "text/plain"]


# Handles profile editing
def edit_profile(request, data):
    token = request.cookies.get('token')
    user = functions.get_user(token)
    if user:
        image_string = functions.add_image(data['picture'])
        database.update_profile(data, image_string, token)
        response_code = 200
        content_type = "text/plain"
        return [b"", b"Profile Updated", response_code, content_type]
    else:
        return [b"", b"You must log in", 403, "text/plain"]


# Handles direct message sending
def send_message(request, data):
    token = request.cookies.get('token')
    user = functions.get_user(token)
    if user:
        database.add_message(user, data)
        response_code = 201
        content_type = "text/plain"
        return [b"", b"Message added", response_code, content_type]
    else:
        return [b"", b"You must log in", 403, "text/plain"]
