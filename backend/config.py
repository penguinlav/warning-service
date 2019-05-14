import os
import logging

import aumbry
from aumbry import Attr, YamlConfig


BASE_PATH = os.path.dirname(__file__)


class DatabaseConfig(YamlConfig):
    __mapping__ = {
        'connection': Attr('connection', str),
    }

    connection = ''


class LDAPConfig(YamlConfig):
    __mapping__ = {
        'hostport': Attr('hostport', str),
        'user_prefix': Attr('user_prefix', str),
        'connect_timeout': Attr('connect_timeout', int),
    }
    hostport = None
    port = None
    user_prefix = ''
    connect_timeout = 10

    @property
    def is_ldap(self):
        return self.hostport is not None


class AppConfig(YamlConfig):
    __mapping__ = {
        'static_folder': Attr('static_folder', str),
        'session_secret': Attr('session_secret', str),
        'ldap': Attr('ldap', LDAPConfig),
        'logger_format': Attr('logger_format', str),
    }
    logger_format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
    session_secret = 'yep_secret'
    static_folder = property()

    @static_folder.setter
    def static_folder(self, v):
        setattr(self, '_static_folder', v)

    @static_folder.getter
    def static_folder(self):
        return os.path.join(BASE_PATH, getattr(self, '_static_folder', ''))


class ServerConfig(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfig),
        'app': Attr('app', AppConfig),
    }

    def __init__(self):
        self.db = DatabaseConfig()
        self.app = AppConfig()



cfg = aumbry.load(aumbry.FILE, ServerConfig, {'CONFIG_FILE_PATH': os.path.join(BASE_PATH, 'config.yml')})


log = logging.getLogger('app')
log.setLevel('DEBUG')
f = logging.Formatter(cfg.app.logger_format, datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
ch.setFormatter(f)
log.addHandler(ch)