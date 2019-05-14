from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


SAModel = declarative_base()

class Base(SAModel):
    __abstract__ = True

    def as_dict(self):
        return dict([(col.name, getattr(self, col.name)) for col in self.__table__.c])

    def __json__(self):
        return self.as_dict()

    async def create(self, conn):
        self.before_save()
        resp = await conn.execute(self.__table__.insert().values(**self.as_dict()))
        setattr(self, self.__mapper__.primary_key[0].name, resp.inserted_primary_key[0])
        return self

    def before_save(self):
        pass

class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(128), unique=True, index=True)
    password = sa.Column(sa.String(128))

    def __json__(self):
        ret = super().__json__()
        del ret['password']
        return ret

    @classmethod
    async def get_user(cls, conn, username):
        result = await conn.execute(cls.__table__.select(cls.__table__.c.username == username))
        user_list = await result.fetchall()
        if not len(user_list):
            raise Exception(f"There is not user {username}")
        return User(**dict(user_list[0].items()))

    @classmethod
    async def check_credentials(cls, conn, username, password):
        result = await conn.execute(cls.__table__.select(
            cls.__table__.c.username == username and cls.__table__.c.password == password))
        user_list = await result.fetchall()
        return len(user_list) == 1

class Message(Base):
    __tablename__ = 'messages'

    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.String(128))
    msg = sa.Column(sa.String(1000))
    time = sa.Column(sa.Float, default=datetime.now().timestamp())

    def before_save(self):
        self.time = datetime.now().timestamp()

    @classmethod
    async def get_messages(cls, conn, time=None, size=20):
        result = await conn.execute(
            cls.__table__.select(
                None if time is None else cls.__table__.c.time >= time).order_by(sa.desc(cls.__table__.c.time))
        )
        messages_list = await result.fetchmany(size=size)
        return list([dict(mess.items()) for mess in messages_list])
