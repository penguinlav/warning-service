from chat.views import ChatList
from auth.views import Auth, SignIn, SignOut


routes = [
    ('GET', '/api/messages',        ChatList,  'messages'),
    # ('GET', '/ws',      WebSocket, 'chat'),
    ('*',   '/api/auth',   Auth,     'auth'),
    ('*',   '/api/signin',  SignIn,    'signin'),
    ('*',   '/api/signout', SignOut,   'signout'),
]
