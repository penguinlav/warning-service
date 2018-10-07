import json
from aiohttp import web
from aiohttp_session import session_middleware
import socketio
from motor import motor_asyncio as ma
import hashlib
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from datetime import datetime

from aiohttp_session import get_session

from settings import *
from middlewares import authorize
from routes import routes

from chat.models import Message 

from utils import AliasDict


sio = socketio.AsyncServer(logger=True, engineio_logger=True)# , cookie=None)

@web.middleware
async def error_middleware(request, handler):
    # try:
    print(request)
    return await handler(request)
        # if response.status != 404:
        #     return response
        # message = response.message
    # except web.HTTPException as ex:
    #     if ex.status != 404:
    #         raise
    #     message = ex.reason
    # return web.json_response({'error': message})


app = web.Application(middlewares=[
    # error_middleware,
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest(), httponly=False)),
    authorize
])

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

app.client = ma.AsyncIOMotorClient(MONGO_HOST)
app.db = app.client[MONGO_DB_NAME]

app.users = AliasDict()

app.core_states = {
    'cp': False,
    'lab1': False,
    'lab2': False,
    'lab3': False,
    'lec1': False,
    'lec2': False,    
    'lec3': False,            
}

sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    return web.Response(text="It's api", content_type='text/html')


from collections import defaultdict
from auth.models import User

class NSws(socketio.AsyncNamespace):
    clients = {} # sid-> client
    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('app')
        super(NSws, self).__init__(*args, **kwargs)
        

    async def on_connect(self, sid, environ):
        request = environ['aiohttp.request']

        session = await get_session(request)
        user = session.get('user')
        self.server.logger.info(f"User connected: {user}")
        if user is None: 
            raise Exception("User not found")
        if self.clients.get(sid) is not None:
            raise Exception(f'Already have the sid: {sid} for user {user}')

        self.clients[sid] = User(self.app.db, {'id': user})

        self.server.logger.info(f"connect {sid} environ {environ}")
        await self.emit('core_updstates', self.app.core_states)
        await self.send_messages()

    async def on_disconnect(self, sid):
        self.server.logger.info(f'disconnect {sid}')
        del self.clients[sid]

    async def send_users_list(self):
        pass

    async def on_core_updstate(self, sid, name_place):
        self.app.core_states[name_place] = not self.app.core_states[name_place]
        self.server.logger.info(f'sid: {sid}, name_place: {name_place}')
        await self.emit('core_updstates', self.app.core_states)

    async def send_messages(self):
        message = Message(self.app.db)
        messages = await message.get_messages()
        self.server.logger.info(f'send messages: {messages}')
        await self.emit('chat_messages', {'messages': messages})

    async def chat_message(self, sid):
        message = Message(self.app.db)
        messages = await message.get_messages()
        self.server.logger.info(f'send messages: {messages}')
        client = self.clients[sid]
        login = await client.get_login()
        m = {'user': login, 'msg': 'mmmeesaggeee', 'time': str(datetime.now().timestamp())}
        await self.emit('chat_messages', {'messages': [m, m]})

    async def on_messagetoserver(self, sid, msg):
        message = Message(self.app.db)
        login = await self.clients[sid].login
        self.server.logger.info(f'Receive mess: {msg} from user: {login}')
        result, m_dict = await message.save(user=login, msg=msg)
        if result:
            await self.emit('chat_onemessage', m_dict)
        else:
            raise Exception("Message doesnt save: {m_dict}")


sio.register_namespace(NSws('/ws', app=app))

if __name__ == '__main__':
    log.debug('start server')
    web.run_app(app, port=8000)
    log.debug('Stop server end')

