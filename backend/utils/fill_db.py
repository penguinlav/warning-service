import os
import sys
import json

import asyncio
from sqlalchemy.exc import IntegrityError

dir_file = os.path.dirname(__file__)
sys.path.append(os.path.join(dir_file, '../'))

from config import cfg, BASE_PATH, log
from db.manager import DBManager
from db.models import User


async def fill_db():
    try:
        log.info('Start fill db.')
        conn_string = cfg.db.connection
        mgr = DBManager(conn_string)
        con = await mgr.con
        with open(os.path.join(BASE_PATH, 'db/fixtures.json'), 'r') as file:
            fixtures = json.load(file)
            for user in fixtures['users']:
                u = User(**user)
                try:
                    await u.create(con)
                except IntegrityError:
                    log.info(f'{user} already exists')
    except Exception as e:
        log.error(f'Exception in the process of filling the database: {e}')


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fill_db())


if __name__ == '__main__':
    main()
