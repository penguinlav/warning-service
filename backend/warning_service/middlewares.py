from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session

from .db.models import User


@middleware
async def authorize(request, handler):
    def check_path(path):
        for r in ['/api/signout', '/api/profile', '/socket.io']:
            if path.startswith(r):
                return False
        return True
    session = await get_session(request)
    if session.get("user"):
        try:
            user_obj = await User.get_user(await request.app.mgr.con, username=session.get("user"))
            request.user = user_obj
        except:
            session.invalidate()
            return web.HTTPUnauthorized()
        return await handler(request)
    elif check_path(request.path):
        return await handler(request)
    else:
          return web.HTTPUnauthorized()
