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

def get_secret(secret_name: str) -> str | None:
    secret_name = secret_name.upper()
    secret_file_env_var = f"{secret_name}_FILE"
    if (secret_file_name := os.environ.get(secret_file_env_var)) is not None:
        try:
            with open(secret_file_name) as inf:
                logger.info("%s", f"read {secret_file_name=}")
                return inf.read()
        except Exception as e:
            logger.info("%s", f"{secret_file_name=}: {e}")

    logger.info("%s", f"Couldn't read file {secret_file_name=}; continuing")
    got = os.environ.get(secret_name)
    logger.info("%s", f"from environment: {'found' if got else 'did not find'} {secret_name=}")
    return got

if (SECRET_KEY := get_secret("DJANGO_SECRET_KEY")) is None:
    del SECRET_KEY

# False means "really check recaptchas with google"
# True means "we're running unit tests or something so just pretend all recaptcha responses are valid"
RECAPTCHA_BACKDOOR = False

if (RECAPTCHA_SECRET := get_secret("RECAPTCHA_SECRET")) is None:
    del RECAPTCHA_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    ".offby1.info",
    ".orb.local",
    ".teensy.info",
    "127.0.0.1",
    "localhost",
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

ASGI_APPLICATION = "project.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

SQLITE_DATA_DIR = Path(os.environ.get("SQLITE_DATA_DIR", BASE_DIR))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": SQLITE_DATA_DIR / "db.sqlite3",
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

RUDYBOT_IP_ADDRESSES = {
    ipaddress.IPv4Address("144.217.82.212"),  # solaria.tethera.net, rudybot's new home.
}

# This is needed for dev when we run via docker, which is why it's here and not in prod_settings.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

for basename in ("aws_access_key_id", "aws_secret_access_key"):
    fullname = Path("/run/secrets") / basename
    try:
        with open(fullname) as inf:
            os.environ[basename.upper()] = inf.read()
    except FileNotFoundError as e:
        pass
    else:
        logger.info("%s", f"Read {len(os.environ[basename.upper()])} bytes from {fullname} into env var {basename.upper()}")

del basename
