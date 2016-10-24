#encoding:utf-8
import sys
import os
from datetime import timedelta
import pymongo
from mongoengine import connect
import redis
import socket
from apps.base import xinge

reload(sys)
sys.setdefaultencoding('utf-8')

VERSION = '0.1.1'

   
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}
'''

#-----------  celery ----------
import celery
CELERYD_CONCURRENCY           = 1
CELERY_TIMEZONE               = 'Asia/Shanghai'
BROKER_TRANSPORT              = "redis"
BROKER_URL                    = 'redis://127.0.0.1:6379/2'
CELERY_RESULT_BACKEND         = "redis://127.0.0.1:6379/3"
CELERY_REDIS_BACKEND_SETTINGS = {
                                    'host':'127.0.0.1',
                                    'port':6379,
                                }
celery_app = celery.Celery()
celery_app.config_from_object(locals())

# ---------- session ----------

SESSION_ENGINE       = 'redis_sessions.session'
SESSION_REDIS_HOST   = 'localhost'
SESSION_REDIS_PORT   = 6379
SESSION_REDIS_DB     = 0
SESSION_REDIS_PREFIX = 'session'


# ---------- cache ----------

CACHE_BACKEND = 'redis_cache.cache://127.0.0.1:6379'
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    },
}

ROOT_PATH   = os.path.abspath(os.path.dirname(__file__))

DB_NAME = None
DB_HOST = None


ENV_NAME = 'tlmq'

ENV = os.getenv('ENV', 'TEST').upper()
HOST_NAME = socket.gethostname()

if ENV == 'TEST':
    DEBUG   = True
    DB_HOST, DB_NAME = 'localhost', '51quickfix'
else:
    DEBUG   = True
    DB_HOST, DB_NAME = 'localhost', '51quickfix'


ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = 'Asia/Shanghai'

DATETIME_FORMAT = 'Y-m-d H:i:s'

LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

LOCALE_PATHS  = ('.', 'locale')

USE_TZ = True

APPEND_SLASH = False

MEDIA_ROOT  = os.path.join(ROOT_PATH, 'media')
MEDIA_ROOT  = ''
MEDIA_URL   = ''

BACKEND_ROOT = os.path.join(ROOT_PATH, 'apps', 'backend')

STATIC_ROOT = os.path.join(ROOT_PATH, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
        os.path.join(BACKEND_ROOT),
        os.path.join(STATIC_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
)

SECRET_KEY = '-genfexc=&amp;ss$)##ddg6)(6n^g1vbn0stszdr%wcmy78$(1h)k'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.base.middlewares.BaseMiddleware', 
)


SESSION_COOKIE_AGE = 1209600

AUTHENTICATION_BACKENDS = ['mongoengine.django.auth.MongoEngineBackend']
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
MONGOENGINE_USER_DOCUMENT = 'apps.base.models.User'

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
        os.path.join(ROOT_PATH,'templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'apps.base.context.settings_processor',    
    'django.contrib.messages.context_processors.messages'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'mongoengine.django.mongo_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'apps',
    'redis_cache',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ['*',]


TEMPLATE_DEBUG = DEBUG

COMPRESS_ENABLED = not DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

connect(host=DB_HOST,db=DB_NAME)
DB    = getattr(pymongo.MongoClient(host=DB_HOST),DB_NAME)
REDIS = redis.Redis(host='localhost', port=6379, db=1)


ANDROID_XG_ACCESS_ID   = '2100167016'
ANDROID_XG_SECRET_KEY  = '2a3f33ce8f00dc0783f0fed99fb435c8'
MANDROID_XG_ACCESS_ID  = '2100167011'
MANDROID_XG_SECRET_KEY = '0c5005e1fa3255def0b616e8c0dd92d2'

MIOSID_XG_ACCESS_ID  = '2200167018'
MIOSID_XG_SECRET_KEY = 'fcd454baa41bfe7590d0b7e13be8e341'
IOSID_XG_ACCESS_ID   = '2200167021'
IOSID_XG_SECRET_KEY  = 'cfdc742e6010a82ac8562a5023ee3585'


'''
_xinge_app_android = xinge.XingeApp(ANDROID_XG_ACCESS_ID, ANDROID_XG_SECRET_KEY)
m_xinge_app_android = xinge.XingeApp(MANDROID_XG_ACCESS_ID, MANDROID_XG_SECRET_KEY)
m_xinge_app_ios = xinge.XingeApp(MIOSID_XG_ACCESS_ID, MIOSID_XG_SECRET_KEY)
_xinge_app_ios = xinge.XingeApp(IOSID_XG_ACCESS_ID, IOSID_XG_SECRET_KEY)
'''
 
PUSH_ANDROID = xinge.XingeApp(ANDROID_XG_ACCESS_ID, ANDROID_XG_SECRET_KEY)
M_PUSH_ANDROID = xinge.XingeApp(MANDROID_XG_ACCESS_ID, MANDROID_XG_SECRET_KEY)
M_PUSH_IOS = xinge.XingeApp(MIOSID_XG_ACCESS_ID, MIOSID_XG_SECRET_KEY)
PUSH_IOS = xinge.XingeApp(IOSID_XG_ACCESS_ID, IOSID_XG_SECRET_KEY)


USER_CATEGORY_TUPLE = [[u'男', u'男'],[u'女', u'女']]
DEVICE_TYPE = {u'设备':'EQ', u'IT':'IT', u'工程':'EN'}
DEVICE_CATEGORY = [u'制冷',u'制热',u'不锈钢',u'其他']
SERVICE_COMPANY = {1:u'',2:u'汉堡王',3:u'达美乐'}
CALL_STATUS     = {-1:u'取消', 0:u'新维修单', 1:u'已接单', 2:u'已经完成', 3:u'到店', 4:u'维修失败', 5:u'填写修单未确认', 6:u'暂停'}
AREA    = {
            2:[u'华东区',u'华南区',u'华北区',u'加盟区'],
            3:[u'华东区',u'华南区',u'华北区',u'加盟区']
          }
COMPANY = {
            2:[u'汉堡王(中国)投资有限公司',u'汉堡王(北京)餐饮管理有限公司',u'汉堡王(上海)餐饮管理有限公司',u'汉堡王(广州)餐饮有限公司',u'汉堡王(沈阳)餐饮管理公司',u'汉堡王食品(深圳)有限公司'],
            3:[u'上海达美乐比萨有限公司']
            }
COMPANYS = {
            2:{u'汉堡王(中国)投资有限公司':u'华北区',u'汉堡王(北京)餐饮管理有限公司':u'华北区',u'汉堡王(上海)餐饮管理有限公司':u'华东区',u'汉堡王(广州)餐饮有限公司':u'华南区',u'汉堡王(沈阳)餐饮管理公司':u'华北区',u'汉堡王食品(深圳)有限公司':u'华南区'},
            3:{u'上海达美乐比萨有限公司':u'华东区'}
            }

FIX_TIME = {1:[4, 2], 2:[72,2], 3:[72,2]}
if ENV in ['TEST', 'TEST2']:
    AREA_CONNECTOR = {
        2:{u'华东区':[u'潘远1','15017935316'], u'华北区':[u'潘远2','15017935316'], u'华南区':[u'潘远3','15017935316'], u'加盟区':[u'潘远4','15017935316']},
        3:{u'华东区':[u'潘远1','15017935316'], u'华北区':[u'潘远2','15017935316'], u'华南区':[u'潘远3','15017935316'], u'加盟区':[u'潘远4','15017935316']}
    } 
else:
    AREA_CONNECTOR = {
        2:{u'华东区':[u'陈波','13818670832'], u'华北区':[u'刘勇','13910023841'], u'华南区':[u'王建斌','13713983988'], u'加盟区':[u'周文辉','13585753381']},
        3:{u'华东区':[u'Ted','13564437395'], u'华北区':[u'Ted','13564437395'], u'华南区':[u'Ted','13564437395'], u'加盟区':[u'Ted','13564437395']}
    }

USER_CATEGORY = {'0':u'维修员','1':u'餐厅负责人','2':u'维修主管','3':u'餐厅区域经理','4':u'OC', '5':u'后台管理员'}

SMSAPIKEY = '26235daf2cdee5c1e931205e0a939767'

#人工费收费标准
CHARGE = 80
#上门费
HOME_FEE = 30




