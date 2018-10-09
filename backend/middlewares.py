from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session
from settings import *


@middleware
async def authorize(request, handler):
    print('middleware ', request)
    def check_path(path):
        result = True
        for r in ['/auth', '/static/', '/signin', '/signout', '/_debugtoolbar/']:
            if path.startswith('/api' + r):
                result = False
        return result
    session = await get_session(request)
    if session.get("user"):
        return await handler(request)
    elif check_path(request.path):
        url = request.app.router['auth'].url_for()
        session.invalidate()
        return web.HTTPUnauthorized()
    else:
          return await handler(request)
