from aiohttp import web

from .views.auth import Auth, SignOut, Profile


routes = [
    web.route('*', '/api/auth',   Auth, name='auth'),
    web.route('*', '/api/signout', SignOut, name='signout'),
    web.route('GET', '/api/profile', Profile, name='profile'),
]
