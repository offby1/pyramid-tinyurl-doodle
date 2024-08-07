import ipaddress
import logging
import os
from pathlib import Path

import dotenv
import platformdirs

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "info.teensy.teensy-django"

dotenv_path = platformdirs.user_config_dir(appname=APP_NAME) + "/.env"
dotenv.load_dotenv(
    dotenv_path=dotenv_path,
)
del dotenv_path

if (skf := os.environ.get("DJANGO_SECRET_FILE")) is not None:
    with open(skf) as inf:
        SECRET_KEY = inf.read()
else:
    # This won't be available when we're running `manage.py makemigrations` (when building the Docker image) but that's OK.
    SECRET_KEY = os.environ.get("SECRET_KEY")

if SECRET_KEY is None:
    del SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "offby1.info",
    "teensy.info",
]


# Application definition

INSTALLED_APPS = [
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "app",
]

MIDDLEWARE = [
    "app.middleware.NoIndexMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static_root"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

HASH_LENGTH = 10


GIT_INFO = None

try:
    with open(BASE_DIR / ".git-post-checkout-info") as inf:
        for index, line in enumerate(inf):
            if index == 1:
                GIT_INFO = line.rstrip()
                break
except OSError as e:
    logger.warning("%s -- ignoring", e)

# I don't really understand this, but it shaddaps a warning
# (and replaces it with a deprecation warning :-( )
FORMS_URLFIELD_ASSUME_HTTPS = True

# False means "really check recaptchas with google"
# True means "we're running unit tests or something so just pretend all recaptcha responses are valid"
RECAPTCHA_BACKDOOR = False

RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET")
if RECAPTCHA_SECRET is None:
    del RECAPTCHA_SECRET

RUDYBOT_IP_ADDRESSES = {
    ipaddress.IPv4Address("144.217.82.212"),  # solaria.tethera.net, rudybot's new home.
}

# This is needed for dev when we run via docker, which is why it's here and not in prod_settings.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
