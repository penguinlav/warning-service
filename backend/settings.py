from os.path import isfile
# from envparse import env
import logging


log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

# if isfile('.env'):
#     env.read_envfile('.env')

DEBUG = True#env.bool('DEBUG', default=False)

# SITE_HOST = env.str('HOST')
# SITE_PORT = env.int('PORT')
SECRET_KEY = 'azzaz' #  env.str('SECRET_KEY')
MONGO_HOST = 'mongo.dev' # env.str('MONGO_HOST')
MONGO_DB_NAME = 'warning_service' #  env.str('MONGO_DB_NAME')

MESSAGE_COLLECTION = 'messages'
USER_COLLECTION = 'users'
