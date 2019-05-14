import argparse

from aiohttp import web
from app import make_app

from config import log

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='127.0.0.1')
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--session_secret", default=None)
    parser.add_argument("command", nargs='+')

    parsed = parser.parse_args()

    command = parsed.command

    if command[0] == 'runserver':
        if len(command) != 1:
            parser.error('Invalid command line.')
        app = make_app(KEY=parsed.session_secret)
        log.info(f'Starting server at {parsed.host}:{parsed.port}')
        web.run_app(app, host=parsed.host, port=parsed.port)

    elif command[0] == 'migrate':
        if len(command) != 2:
            parser.error('Invalid command. For example: migrate head')
        import alembic.config
        alembicArgs = [
            '--raiseerr',
            'upgrade', command[1],
        ]
        alembic.config.main(argv=alembicArgs)
    elif command[0] == 'fillfixtures':
        if len(command) != 1:
            parser.error('Invalid command line.')
        import utils.fill_db
        utils.fill_db.main()


if __name__ == "__main__":
    main()


