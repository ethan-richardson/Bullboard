import respond
# We want to serve the login page here.
def login(server):
    html = b"Login page here."
    respond.send_response(server, b"200", b"text/html", str(len(html)).encode())
    server.wfile.write(html)

# We want to serve the register page here.
def register(server):
    html = b"Register page here."
    respond.send_response(server, b"200", b"text/html", str(len(html)).encode())
    server.wfile.write(html)
# TODO - Other functions dependent on the path will also go here #
