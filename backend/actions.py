import file
# We want to serve the login page here.
def login():
    body = file.read_file("Bullboard/frontend/pages/login.html")
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# We want to serve the register page here.
def register():
    body = b"Register page here."
    response_code = 200
    content_type = "text/html"
    return [body, response_code, content_type]

# Respond to HTML paths here.
def resp_to_html_paths(path):
    body = file.read_file("Bullboard/frontend/pages%s" % path)
    response_code = 200
    if path.endswith(".css"):
        return [body, response_code, "text/css"]
    elif path.endswith(".js"):
        return [body, response_code, "text/javascript"]
    elif path.endswith(".png"):
        return [body, response_code, "image/png"]
    else:
        return [body, response_code, "image/jpeg"]
    
def create_account(data):
    email = data["email"]
    password = data["password"]
    # TODO - Need to insert into database.
    # TODO - Do we want password requirements?
    pass