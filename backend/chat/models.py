from datetime import datetime
from settings import MESSAGE_COLLECTION


class Message():

    def __init__(self, db, **kwargs):
        self.collection = db[MESSAGE_COLLECTION]

    async def save(self, user, msg, **kw):
        m_dict = {'user': user, 'msg': msg, 'time': datetime.now().timestamp()}
        result = await self.collection.insert_one(m_dict)
        del m_dict['_id']
        return result.acknowledged, m_dict

    async def get_messages(self):
        messages = self.collection.find(projection={'_id':0}).sort([('time', -1)]).limit(20)
        return await messages.to_list(length=None)
