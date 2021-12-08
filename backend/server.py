from aiohttp import web
import aiohttp
import routes
import actions
import database

# Handle GET requests here
async def get_handler(request):
    # Get all the routes associated with a GET request
    allGetRoutes = routes.get_routes
    # Call the action that is associated with the current request
    action = allGetRoutes[request.path]
    response = action(request)
    # Send a server response
    return web.Response(
        headers=response[0],
        body=response[1],
        status=response[2],
        content_type=response[3],
        charset="utf-8"
    )

# Handle POST requests here
async def post_handler(request):
    data = await request.json()
    allPostRoutes = routes.post_routes
    action = allPostRoutes[request.path]
    response = action(request, data)
    # Send a server response
    return web.Response(
        headers=response[0],
        body=response[1],
        status=response[2],
        content_type=response[3],
        charset="utf-8"
    )

clients = []

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    clients.append(ws)
    await ws.prepare(request)
    print("A new client has connected!")
    # We're waiting for requests here
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif "x" in msg.data and "y" in msg.data:
                for client in clients:
                    if client != ws:
                        await client.send_str(msg.data)
        # If there is an exception, the socket will close
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed w/ exception %s' % ws.exception())
    # If we've reached the end of control flow, then the socket has closed
    print('websocket connection closed')
    clients.remove(ws)
    return ws

async def image_handler(request):
    response = actions.resp_to_html_paths(request)
    return web.Response(
        headers=response[0],
        body=response[1],
        status=response[2],
        content_type=response[3],
        charset="utf-8"
    )

async def message_handler(request):
    if request.method == "GET":
        response = actions.messages(request)
    elif request.method == "POST":
        data = await request.json()
        response = actions.send_message(request, data)
    return web.Response(
        body=response[1],
        status=response[2],
        content_type=response[3],
        charset="utf-8"
    )

app = web.Application()
app.add_routes([
    web.get('/login', get_handler),
    web.get('/', get_handler),
    web.get('/images/{name}', image_handler),
    web.get('/images/prof_pics/{name}', image_handler),
    web.get('/register', get_handler),
    web.get('/functions.js', get_handler),
    web.get('/canvas.js', get_handler),
    web.get('/styles.css', get_handler),
    web.post('/login_attempt', post_handler),
    web.post('/create_account', post_handler),
    web.get('/websocket', websocket_handler),
    web.get('/newsfeed', get_handler),
    web.get('/profile', get_handler),
    web.post('/edit_profile', post_handler),
    web.get('/edit', get_handler),
    web.get('/map', get_handler),
    web.get('/messages', message_handler),
    web.post('/add_post', post_handler),
    web.get('/logout', get_handler),
    web.get('/messages/{ubit}', message_handler),
    web.post('/messages/{ubit}', message_handler),
])
# Run the server
web.run_app(app)