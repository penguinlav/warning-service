import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context


parent_dir = os.path.abspath(os.getcwd())
sys.path.append(parent_dir)


from db.models import SAModel
from config import cfg


config = context.config
fileConfig(config.config_file_name)

target_metadata = SAModel.metadata
connectable = create_engine(cfg.db.connection)

with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()
