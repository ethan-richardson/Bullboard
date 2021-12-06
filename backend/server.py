from aiohttp import web
import aiohttp
import routes
import actions
import database

# Handle GET requests here
async def get_handler(request):
    database.fetch_all() # for debugging
    # Get all the routes associated with a GET request
    allGetRoutes = routes.get_routes
    # Call the action that is associated with the current request
    action = allGetRoutes[request.path]
    headers = action(request)
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
    # data = data.decode('utf-8')
    allPostRoutes = routes.post_routes
    action = allPostRoutes[request.path]
    response = action(data)
    # Send a server response
    return web.Response(
        headers=response[0],
        body=response[1],
        status=response[2],
        content_type=response[3],
        charset="utf-8"
    )

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
                #await ws.send_str(msg.data + '/newsfeed')
                pass
        # If there is an exception, the socket will close
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed w/ exception %s' % ws.exception())
    # If we've reached the end of control flow, then the socket has closed
    print('websocket connection closed')
    return ws

async def image_handler(request):
    # if request.path.startswith("images/"):
    headers = actions.resp_to_html_paths(request)
    return web.Response(
        body=headers[0],
        status=headers[1],
        content_type=headers[2],
        charset="utf-8"
    )

app = web.Application()
app.add_routes([
    web.get('/login', get_handler),
    web.get('/', get_handler),
    web.get('/images/{name}', image_handler),
    web.get('/register', get_handler),
    web.get('/functions.js', get_handler),
    web.get('/styles.css', get_handler),
    web.post('/login_attempt', post_handler),
    web.post('/create_account', post_handler),
    web.get('/websocket', websocket_handler),
    web.get('/newsfeed', websocket_handler),
    web.get('/profile', get_handler)
])
# Run the server
web.run_app(app)