import os
import logging

import aumbry
from aumbry import Attr, YamlConfig


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class DatabaseConfig(YamlConfig):
    __mapping__ = {
        'connection': Attr('connection', str),
    }

    connection = ''


class LoggerConfig(YamlConfig):
    __mapping__ = {
        'file': Attr('file', str),
        'format': Attr('format', str),
        'level': Attr('level', str),
    }
    file = None
    level = 'INFO'
    format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'

    @property
    def is_log_file(self):
        return self.file is not None


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
        'logger': Attr('logger', LoggerConfig)
    }
    session_secret = 'yep_secret'
    static_folder = property()
    _static_folder = os.path.join(BASE_PATH, 'public')

    def __init__(self):
        self.logger = LoggerConfig()

    @static_folder.setter
    def static_folder(self, v):
        setattr(self, '_static_folder', v)

    @static_folder.getter
    def static_folder(self):
        return getattr(self, '_static_folder', '')


class ServerConfig(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfig),
        'app': Attr('app', AppConfig),
    }

    def __init__(self):
        self.db = DatabaseConfig()
        self.app = AppConfig()


cfg = aumbry.load(aumbry.FILE,
                  ServerConfig,
                  {'CONFIG_FILE_PATH': os.path.join(os.path.abspath(os.getcwd()), 'config.yml')})


log = logging.getLogger('app')
log.setLevel(cfg.app.logger.level)
f = logging.Formatter(cfg.app.logger.format, datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setFormatter(f)
log.addHandler(ch)
if cfg.app.logger.is_log_file:
    cf = logging.FileHandler(filename=cfg.app.logger.file)
    cf.setFormatter(f)
    log.addHandler(cf)