import os
import shutil
import argparse

from aiohttp import web


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--host", default='127.0.0.1', help="Default host localhost.")
    parser.add_argument("--port", type=int, default=8000, help="Default port 8000.")
    parser.add_argument("--session_secret", default=None, help="Secret of client session.")
    parser.add_argument("command", nargs='+', help=
"""copyconfig\tInit config file.
runserver\tRun server.
migrate <name>\tMake migration with name of migration.
fillfixtures\tFill database with fixtures.""")

    parsed = parser.parse_args()
    command = parsed.command

    run_path = os.path.abspath(os.getcwd())
    if command[0] == 'copyconfig':
        if len(command) != 1:
            parser.error('Invalid command line.')
        file_path = os.path.dirname(os.path.realpath(__file__))
        shutil.copy(os.path.join(file_path, 'config.yml'), run_path)
        return

    if not os.path.exists(os.path.join(run_path, 'config.yml')):
        parser.error("No config file 'config.yml' found")
        return
    from .config import log

    if command[0] == 'runserver':
        if len(command) != 1:
            parser.error('Invalid command line.')
        from .app import make_app

        app = make_app(KEY=parsed.session_secret)
        log.info(f'Starting server at {parsed.host}:{parsed.port}')
        web.run_app(app, host=parsed.host, port=parsed.port, access_log=log)

    elif command[0] == 'migrate':
        if len(command) != 2:
            parser.error('Invalid command. For example: migrate head')
        from .alembic import run_migrations
        run_migrations.run(command[1])

    elif command[0] == 'fillfixtures':
        if len(command) != 1:
            parser.error('Invalid command line.')
        from .utils import fill_db
        fill_db.main()






if __name__ == "__main__":
    main()


