from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import cgi
# Using BaseHTTPRequestHandler as our request handler
class HTTP(BaseHTTPRequestHandler):

    # Function that handles GET requests
    # TODO - We should try and avoid these big conditionals. Find a better way to do this.
    def do_GET(self):
        if self.path.endswith("/"):
            # TODO - Root page is served here. Login page here?
            # temporary placeholder for content
            helloHTML = "<html> <body> <h1> Hello World! </h1> </body> </html>"
            args = [["Content-Type", "text/html"], ["Content-Length", len(helloHTML)],
            ["X-Content-Type-Options", "nosniff"]]
            # Send 200 OK response
            self.send_response(200)
            # Set the headers of the server response
            for header in args: self.send_header(header[0], header[1])
            self.end_headers()
            # Send the server response
            self.wfile.write(helloHTML.encode())
        elif self.path.endswith("/login"):
            # TODO - Login page is served here.
            login = "Login"
            args = [["Content-Type", "text/html"], ["Content-Length", len(login)],
            ["X-Content-Type-Options", "nosniff"]]
            # Send 200 OK response
            self.send_response(200)
            # Set the headers of the server response
            for header in args: self.send_header(header[0], header[1])
            self.end_headers()
            # Send the server response
            self.wfile.write(login.encode())
        elif self.path.endswith("/register"):
            # TODO - Register page is served here.
            register = "Register"
            args = [["Content-Type", "text/html"], ["Content-Length", len(register)],
            ["X-Content-Type-Options", "nosniff"]]
            # Send 200 OK response
            self.send_response(200)
            # Set the headers of the server response
            for header in args: self.send_header(header[0], header[1])
            self.end_headers()
            # Send the server response
            self.wfile.write(register.encode())
        elif self.path.endswith("/home"):
            # TODO - Home page (for each user) is served here.
            home = "Home"
            args = [["Content-Type", "text/html"], ["Content-Length", len(home)],
            ["X-Content-Type-Options", "nosniff"]]
            # Send 200 OK response
            self.send_response(200)
            # Set the headers of the server response
            for header in args: self.send_header(header[0], header[1])
            self.end_headers()
            # Send the server response
            self.wfile.write(home.encode())
        # If the condition reaches here, send a 404.
        else:
            msg = "Content is missing."
            args = [["Content-Type", "text/html"], ["Content-Length", len(msg)],
            ["X-Content-Type-Options", "nosniff"]]
            # Send 404 Not Found
            self.send_response(404)
            # Set the headers of the server response
            for header in args: self.send_header(header[0], header[1])
            self.end_headers()
            # Send the server response
            self.wfile.write(msg.encode())
    
    # We'll handle POST requests in this function.
    def do_POST(self):
        # TODO - We'll have to escape the HTML and then save usernames/passwords
        # in a database.
        None
            
# TODO - Need to figure how to implement WebSockets with the HTTP library.
# TODO - Using BaseHTTPRequestHandler doesn't take care of multi-threading.
# Run the server
def main():
    HOST = "localhost"
    PORT = 8000
    server_address = (HOST, PORT)
    server = HTTPServer(server_address, HTTP)
    print("Server running on port %s" % PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()