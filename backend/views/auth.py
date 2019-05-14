from time import time

from sqlalchemy.exc import OperationalError
from aiohttp import web
from aiohttp_session import get_session


from db.models import User
from config import cfg, log


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def error(message, status=400):
    log.error(message)
    return web.json_response({'error': message}, status=status)


def success(message, status=200, extra=None):
    log.info(message)
    res = {'success': message}
    res.update(extra or {})
    return web.json_response(res, status=status)


class Auth(web.View):
    def _ldap_check_credentials(self, username, password):
        from ldap3 import Server, Connection, ALL, NTLM
        from ldap3.core.exceptions import LDAPBindError
        server = Server(cfg.app.ldap.hostport, connect_timeout=cfg.app.ldap.connect_timeout, get_info=ALL)
        try:
            Connection(
                server,
                user=f'{cfg.app.ldap.user_prefix}{username}',
                password=password,
                auto_bind=True,
                authentication=NTLM
            )
            return True
        except LDAPBindError:
            return False

    async def post(self):
        data = await self.request.json()
        if cfg.app.ldap.is_ldap:
            try:
                log.info("Ldap check.")
                from ldap3.core.exceptions import LDAPSocketOpenError
                result = self._ldap_check_credentials(username=data.get('username'), password=data.get('password'))
            except LDAPSocketOpenError:
                return error(f'Error connect to ldap')
        else:
            try:
                log.info("DB check.")
                result = await User.check_credentials(
                    await self.request.app.mgr.con,
                    username=data.get('username'),
                    password=data.get('password')
                )
            except OperationalError as e:
                return error(f'Error db: {e}')
        if result:
            session = await get_session(self.request)
            set_session(session, data.get('username'))
            return success(f"{data.get('username')} is authorized")
        else:
            return error(f"Invalid credentials for {data.get('username')}")


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
        user = session.get('user')
        return web.json_response({'username': user})
