from settings import USER_COLLECTION
from utils import AliasDict

class Users():
  def __init__(self, db):
    self.db = db
    self.collection = self.db[USER_COLLECTION]

  async def dict_users(self):
    usrs = await self.collection.find(projection={'_id': 0})
    return dict({u['username']: u for u in usrs})


class SidUsers(AliasDict):
  # users = AliasDict()
  def __init__(self, db, *args, **kwargs):
    super(AliasDict, self).__init__(*args, **kwargs)

  async def update(self):
    usrs_db = Users(db)
    usrs_d = await usrs_db.dict_users()
    self.users.update(usrs_d)
