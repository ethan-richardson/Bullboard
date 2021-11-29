from aiohttp import web
import aiohttp
import routes

# Handle GET requests here
async def get_handler(request):
    # Get all the routes associated with a GET request
    allGetRoutes = routes.get_routes
    # Call the action that is associated with the current request
    action = allGetRoutes[request.path]
    headers = action() if '.' not in request.path else action(request.path)
    # Send a server response
    return web.Response(
        body=headers[0],
        status=headers[1],
        content_type=headers[2],
        charset="utf-8"
    )

# Handle POST requests here
async def post_handler(request):
    data = await request.json()
    allPostRoutes = routes.post_routes
    action = allPostRoutes[request.path]
    headers = action(data)
    # Send a server response
    return web.Response(
        body=headers[0],
        status=headers[1],
        content_type=headers[2],
        charset="utf-8"
    )
 
# TODO - Right now, a client is connected any time we receive a request for /websocket
# TODO - but we might only want to connect a client if their logged in
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("A new client has connected!")
    # We're waiting for requests here
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                # this will probably change
                await ws.send_str(msg.data + '/answer')
        # If there is an exception, the socket will close
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed w/ exception %s' % ws.exception())
    # If we've reached the end of control flow, then the socket has closed
    print('websocket connection closed')
    return ws


app = web.Application()
# TODO - there might be a better way to do this.
app.add_routes([
    web.get('/login', get_handler),
    web.get('/', get_handler),
    web.get('/register', get_handler),
    web.get('/functions.js', get_handler),
    web.get('/styles.css', get_handler),
    web.get('/Bull_Board_Mat.png', get_handler),
    web.get('/bull_knocker.jpeg', get_handler),
    web.get('/welcome_mat.png', get_handler),
    web.post('/login_attempt', post_handler),
    web.post('/create-account', post_handler),
    web.get('/websocket', websocket_handler)
])
# Run the server
web.run_app(app)

