import respond
# We want to serve the login page here.
def login(server):
    html = open("../../Bullboard1/frontend/pages/login.html", "rb").read()
    respond.send_response(server, b"200", html, len(html))
    server.wfile.write(html)

# We want to serve the register page here.
def register(server):
    html = open("../../Bullboard1/frontend/pages/create_account.html", "rb").read()
    respond.send_response(server, b"200", html, len(html))
    server.wfile.write(html)
# TODO - Other functions dependent on the path will also go here #
