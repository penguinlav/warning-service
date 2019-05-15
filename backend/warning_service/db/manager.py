import sqlalchemy
from sqlalchemy_aio import ASYNCIO_STRATEGY


class DBManager(object):
    def __init__(self, connection=None):
        self.connection = connection

        self.engine = sqlalchemy.create_engine(self.connection, strategy=ASYNCIO_STRATEGY)
        self._con = None

    @property
    async def con(self):
        if self._con is None:
            self._con = await self.engine.connect()
        return self._con