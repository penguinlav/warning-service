import os
from alembic.config import Config
from alembic import command


def run(revision):
    this_file_directory = os.path.dirname(__file__)
    root_directory      = os.path.join(this_file_directory, '..')
    alembic_directory   = os.path.join(root_directory, 'alembic')
    ini_path            = os.path.join(root_directory, 'alembic.ini')
    print('ini_path: ', ini_path)

    config = Config(ini_path)
    config.set_main_option('script_location', alembic_directory)

    #prepare and run the command
    sql = False
    tag = None
    # command.stamp(config, revision, sql=sql, tag=tag)

    #upgrade command
    command.upgrade(config, revision, sql=sql, tag=tag)