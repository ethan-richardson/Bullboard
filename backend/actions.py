import respond, file
# We want to serve the login page here.
def login(server):
    file_ = file.read_file("Bullboard/frontend/pages/login.html")
    respond.send_response(server, b"200", b"text/html", str(len(file_)).encode())
    server.wfile.write(file_)

# We want to serve the register page here.
def register(server):
    html = b"Register page here."
    respond.send_response(server, b"200", b"text/html", str(len(html)).encode())
    server.wfile.write(html)

# Respond to HTML paths here.
def resp_to_html_paths(server):
    file_= file.read_file("Bullboard/frontend/pages%s" % server.path)
    if server.path.endswith(".css"):
        respond.send_response(server, b"200", b"text/css", str(len(file_)).encode())
    elif server.path.endswith(".js"):
        respond.send_response(server, b"200", b"text/javascript", str(len(file_)).encode())
    elif server.path.endswith(".png"):
        respond.send_response(server, b"200", b"image/png", str(len(file_)).encode())
    else:
        respond.send_response(server, b"200", b"image/jpeg", str(len(file_)).encode())
    server.wfile.write(file_)

def handle_socket(server):
    print("hello")
    pass
    #respond.send_response(server, b"101", b"")
# TODO - Other functions dependent on the path will also go here #
