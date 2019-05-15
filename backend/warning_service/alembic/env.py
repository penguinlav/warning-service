import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from db.models import SAModel
from config import cfg, log


config = context.config
fileConfig(config.config_file_name)

target_metadata = SAModel.metadata
log.info(f'Start miration for connection: {cfg.db.connection}.')
print(f'Start miration for connection: {cfg.db.connection}.')
connectable = create_engine(cfg.db.connection)

with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()
