from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import request, respond, route
import cgi

# Using BaseHTTPRequestHandler as our request handler
class HTTP(BaseHTTPRequestHandler):

    # We'll GET requests in this function.
    def do_GET(self):
        # Create an object based on the current request
        req = request.Request(self.headers, "GET", self.path)
        # Create a router object to route based on the current request
        router = route.Router(self)
        route.add_paths(router)
        router.handle_request(req)
        # TODO - Do stuff according to the path here.
        
    # We'll handle POST requests in this function.
    def do_POST(self):
        # TODO - We'll have to escape the HTML and then save usernames/passwords
        # in a database.
        pass


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