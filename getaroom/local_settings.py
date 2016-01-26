from settings import *
import os

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "devdatabase",
        "USER": "postgres",
        "PASSWORD": "WILLjohn831!",
        "HOST": "127.0.0.1",
        "PORT": "5433",
    }
}