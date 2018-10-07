from bson.objectid import ObjectId
from settings import USER_COLLECTION

class User():

    def __init__(self, db, data, **kw):
        self.db = db
        self.collection = self.db[USER_COLLECTION]
        # self.email = data.get('email')
        self.username = data.get('username')
        self.password = data.get('password')
        self.id = data.get('id')
        self.last_name = None
        self.first_name = None
        self.middle_name = None
        self._login = None

    login = property()
    @login.getter
    async def login(self):
        if self._login is None:
            self._login = await self.get_login()
        return self._login

    async def check_user(self, **kw):
        return await self.collection.find_one({'username': self.username})

    async def get_login(self, **kw):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('username')

    async def create_user(self, **kw):
        user = await self.check_user()
        if not user:
            result = await self.collection.insert_one({'username': self.username, 'password': self.password})
            result = result.inserted_id
            print(f'ressssss!!! {result}')
        else:
            result = 'User exists'
        return result

    def __json__(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name
        }
