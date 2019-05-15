from datetime import datetime

from aiohttp_session import get_session
import socketio

from ..db.models import Message


class ChatWS(socketio.AsyncNamespace):
    clients = {}
    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('app')
        super(ChatWS, self).__init__(*args, **kwargs)

    async def on_connect(self, sid, environ):
        request = environ['aiohttp.request']

        session = await get_session(request)
        user = session.get('user')
        self.server.logger.info(f"User connecting: {user}")
        if user is None:
            self.server.logger.error("User not found")
            raise Exception("User not found")
        if self.clients.get(sid) is not None:
            self.server.logger.error(f"Already have the sid: {sid} for user {user}")
            raise Exception(f'Already have the sid: {sid} for user {user}')

        self.clients[sid] = request.user

        self.server.logger.info(f"Connect {sid} environ {environ}")
        await self.emit('core_updstates', self.app.core_states, room=sid)
        await self.emit('chat_userin', {'user': self.clients[sid].username, 'sid': sid})
        await self.send_users_list(sid)
        await self.send_messages(sid)

    async def on_disconnect(self, sid):
        self.server.logger.info(f'disconnect {sid}')
        await self.emit('chat_userout', {'user': self.clients[sid].username, 'sid': sid})
        del self.clients[sid]

    async def send_users_list(self, room=None):
        await self.emit('chat_userslist', {key: u.__json__() for key, u in self.clients.items()}, room=room)

    async def on_core_updstate(self, sid, name_place):
        self.app.core_states[name_place] = not self.app.core_states[name_place]
        self.server.logger.info(f'Upd state sid: {sid}, name_place: {name_place}')
        await self.emit('core_updstates', self.app.core_states)

        m_dict = {
            'type': 'event',
            'user': self.clients[sid].username,
            'time': datetime.now().timestamp(),
            'place': name_place,
            'state': 'on' if self.app.core_states[name_place] else 'off'
        }
        await self.emit('core_event', m_dict)

    async def on_forcelogout(self, sid, sid_victim):
        self.server.logger.info(f'Try kick: {sid_victim} from {sid}')
        await self.emit('auth_forcelogout', room=str(sid_victim))

    async def send_messages(self, sid=None, time=None):
        messages = await Message.get_messages(await self.app.mgr.con, time=time)
        self.server.logger.info(f'Send messages: {messages}')
        await self.emit('chat_messages', {'messages': messages}, room=sid)

    async def on_messagetoserver(self, sid, msg):
        username = self.clients[sid].username
        self.server.logger.info(f'Receive mess: {msg} from user: {username}')
        message = Message(user=username, msg=msg)
        try:
            await message.create(await self.app.mgr.con)
        except:
            self.server.logger.error("Message doesn't save")
        m_dict = {'type': 'msg', 'user': username, 'msg': msg, 'time': message.time}
        await self.emit('chat_onemessage', m_dict)

    async def on_getmoremessages(self, sid, time):
        self.server.logger.info(f'Receive request older messages then time: {time}')
        try:
            time = float(time)
        except:
            self.server.logger.error("Time isn't float")
            return
        await self.send_messages(sid, time)
