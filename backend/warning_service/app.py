import hashlib

import socketio
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .config import cfg, log
from .views.chat import ChatWS
from .middlewares import authorize
from .routes import routes
from .db.manager import DBManager


async def make_app(*args, **kwargs):
    KEY = kwargs.pop('KEY')
    KEY = KEY or cfg.app.session_secret
    sio = socketio.AsyncServer(logger=log, engineio_logger=log)
    app = web.Application(middlewares=[
        session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(KEY, 'utf-8')).digest(), httponly=False)),
        authorize
    ])

    app.mgr = DBManager(cfg.db.connection)

    app.core_states = {
        'cp': False,
        'lab1': False,
        'lab2': False,
        'lab3': False,
        'lec1': False,
        'lec2': False,
        'lec3': False,
        'tea': False,
        'afk': False
    }
    sio.attach(app)
    sio.register_namespace(ChatWS('/ws', app=app))

    app.router.add_routes(routes)
    static_resource = web.StaticResource('', cfg.app.static_folder, name="resources")

    async def index(request):
        request.match_info['filename'] = 'index.html'
        return await static_resource._handle(request)

    app.router.add_route('GET', '/{path:(?!static/?).*$}', index)
    app.router.register_resource(static_resource)

    return app