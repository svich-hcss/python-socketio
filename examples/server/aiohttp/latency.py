from aiohttp import web

import socketio
import base64

IMG_PATH = 'test.jpg'

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


async def index(request):
    with open('latency.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
async def ping_from_client(sid):
    with open(IMG_PATH, 'rb') as file:
        image_data = base64.b64encode(file.read())
    await sio.emit('pong_from_server', {'image_data': image_data}, room=sid)

@sio.event
async def connect(sid, environment):
    print('connect ', sid)
    await sio.emit('pong_from_server', room=sid)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app)
