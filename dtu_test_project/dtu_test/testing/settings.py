# type: ignore
"""
testing.settings will pull in (probably global) local_settings,
This is a special thanks to David Dyball for helping me understand and build something very familiar to me
in terms of settings and how to set them up
To all who contribute for this, thank you very much.
If you are using windows by default, the permissions to access subfolders for tests are disabled
Activate them using NOSE_INCLUDE_EXE = 1 or an environment variable in your OS with the same name and value
"""
import os

from ..settings import *
from .databases import *

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "x7@y+)ixs_gdewzjw!br7ee#e4ovat7xd3%5&m8i6ws(d=5p#x"
)

#
# Other settings
#
DEBUG = True
TESTING = True

#
# Tells the django environment
#
DJANGOENV = os.environ.get("DJANGOENV", "testing")

REUSE_DB = bool(int(os.environ.get("REUSE_DB", 0)))

if REUSE_DB:
    DATABASE_ROUTERS = []

# Disable the Secure SSL Redirect (special thanks to @DD)
SECURE_SSL_REDIRECT = False

# Use this if you have local_settings.pt file
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = "/media/"
STATIC_ROOT = "/tmp/assets-upload"
STATIC_URL = "/static/"
MEDIA_ROOT = "/tmp/media-root"

# We don't want to run Memcached for tests.
SESSION_ENGINE = "django.contrib.sessions.backends.db"

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "staticfiles": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
}

MIDDLEWARE = list(MIDDLEWARE)
