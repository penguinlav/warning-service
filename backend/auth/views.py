import json
from time import time
from bson.objectid import ObjectId

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from auth.models import User


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def error(message, status=400):
    return web.json_response({'error': message}, status=status)

def success(message, status=200, extra={}):
    res = {'success': message}
    res.update(extra)
    return web.json_response(res, status=status)

class Auth(web.View):

    async def post(self):
        data = await self.request.json()
        try:
            user = User(self.request.app.db, data)
        except KeyError as e:
            return error(f'Missed {e}')
        result = await user.check_user()
        if isinstance(result, dict):
            session = await get_session(self.request)
            set_session(session, str(result['_id']), self.request)
            return success('Authorized', extra=user.__json__())
        else:
            return error(f'User {user.username} with password {user.password} dont not found')


class SignIn(web.View):

    async def post(self, **kw):
        data = await self.request.json()
        try:
            user = User(self.request.app.db, data)
        except KeyError as e:
            return error(e)
        result = await user.create_user()
        if isinstance(result, ObjectId):
            return success(f'User {user.username} created')
        else:
            return error(f'User {user.username} doesnt created')


class SignOut(web.View):

    async def get(self, **kw):
        session = await get_session(self.request)
        session.invalidate()
        if session.get('user'):
            return success('User sign out')
        else:
            return success('User is already sign out')


class Profile(web.View):
    async def get(self, **kwargs):
        session = await get_session(self.request)
        user = User(self.request.app.db, {'id': session.get('user')})
        username = await user.get_login()
        return web.json_response({'username': username})
