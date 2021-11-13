# Server will send a response to the client w/ the appropriate headers here.
def send_response(server, response_code, content_type, content_length):
    server.send_response(int(response_code))
    response_body = {b"Content-Type":content_type, b"Content-Length":content_length,
    b"X-Content-Type-Options":b"nosniff"}
    for k, v in response_body.items(): server.send_header(k, v)
    server.end_headers()

# Send a 404 Not Found here
def send_failure(server):
    server.send_response(404)
    response_body = {"Content-Type":"text/html", "Content-Length":13,
    "X-Content-Type-Options":"nosniff"}
    for k, v in response_body.items(): server.send_header(k, v)
    server.end_headers()
    server.wfile.write(b"404 Not Found")
