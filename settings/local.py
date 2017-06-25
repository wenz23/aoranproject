from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'aoranprojectdb.csbmq0o4oy2b.us-west-1.rds.amazonaws.com',
        'NAME': 'aoranprojectdb',
        'USER': 'ranaoyang',
        'PASSWORD': '1991627yar'
    }
}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qgd(kc82*#anz6cyz*jg30wx+cdtav51dtoe5*a(30pqkg@%g*'
