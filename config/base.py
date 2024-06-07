import os
import environ
from pathlib import Path
from datetime import timedelta
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

# DIRECTORY
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = BASE_DIR / "app"

# ENV
# ----------------------------------------------------------------------------
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env.local"))

# APP
DJANGO_APP = env.str("DJANGO_APP", "Django")

# General
# ----------------------------------------------------------------------------
USE_TZ = True
USE_I18N = True
APPEND_SLASH = True
LANGUAGE_CODE = "en-us"
TIME_ZONE = env.str("SITE_TIME_ZONE", "UTC")

# STATIC
# ----------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR / "public/static")

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(BASE_DIR / "public/media")
MEDIA_URL = "media/"

# APPLICATION DEFINITION
# ----------------------------------------------------------------------------
DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "whitenoise",
    "easy_thumbnails",
    "rest_framework",
    "django_rest_passwordreset",
    "corsheaders",
    "drf_spectacular",
    "django_celery_beat",
    "import_export",
    "actstream"
]

LOCAL_APPS = [
    "app.base",
    'app.users',
    'app.games',
    'app.files',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE
# ----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# URLS
# ----------------------------------------------------------------------------
ROOT_URLCONF = "app.urls"

# TEMPLATES
# ----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(APPS_DIR, "unfold/templates"),
        ],
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
# EASY THUMBNAILS
# ----------------------------------------------------------------------------
THUMBNAIL_ALIASES = {
    'app.users': {
        'thumbnail': {'size': (100, 100), 'crop': True},
        'medium_square_crop': {'size': (400, 400), 'crop': True},
        'small_square_crop': {'size': (50, 50), 'crop': True},
    },
}


# SGI
# ----------------------------------------------------------------------------
WSGI_APPLICATION = "app.wsgi.application"

if env.bool("USE_ASGI", True):
    INSTALLED_APPS.insert(0, "daphne")
    ASGI_APPLICATION = 'app.asgi.application'

# DATABASE
# ----------------------------------------------------------------------------
if env.bool("DJANGO_DEBUG", default=False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / 'db.sqlite3'),
        }
    }
else: 
    DATABASES = {
        "default": {
            "ENGINE": env.str("DB_ENGINE"),
            "NAME": env.str("DB_NAME"),
            "USER": env.str("DB_USER"),
            "PASSWORD": env.str("DB_PASSWORD"),
            "HOST": env.str("DB_HOST"),
            "PORT": env.str("DB_PORT"),
            # "OPTIONS": { # ALLOWED FOR MYSQL ONLY TO INSERT EMOJI'S
            #     "charset": "utf8mb4",
            # },
        }
    }

DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# AUTH
# ----------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
AUTHENTICATION_BACKENDS = (
    'app.users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# SITE
# ----------------------------------------------------------------------------
SITE_URL = env.str("SITE_URL", default="http://localhost:8000")

# EMAIL
# ----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 5

# CHANNELS
# ----------------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env.str("REDIS_HOST"), env.str("REDIS_PORT"))],
        },
    },
}


# REQUESTS
# ----------------------------------------------------------------------------
CORS_URLS_REGEX = r"^/api/.*$"

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True

# REST_FRAMEWORK
# -------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ),
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}

# SPECTACULAR_SETTINGS
# ----------------------------------------------------------------------------
SERVE_PERMISSIONS =  {"SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"]} if env.str("SITE_MODE", "local") == "production" else {"":""}
SPECTACULAR_SETTINGS = {
    "TITLE": f"{DJANGO_APP} API",
    "DESCRIPTION": f"Documentation of API endpoints of {DJANGO_APP}",
    "VERSION": "2.0",
    **SERVE_PERMISSIONS
}

# SECURITY
# ----------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "SIGNING_KEY": env.str("APP_JWT_SIGNING_KEY"),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
}

# ADMIN
# ----------------------------------------------------------------------------
ADMINS = [
    (
        f"""{DJANGO_APP}, Inc""",
        env.str("DJANGO_ADMIN_REPORT_EMAIL", f"admin@{DJANGO_APP.lower()}.com"),
    )
]
MANAGERS = ADMINS


# UNFOLD
UNFOLD = {
    "SITE_TITLE": f"{DJANGO_APP}",
    "SITE_HEADER": f"{DJANGO_APP} Administration",
    "SITE_SYMBOL": "settings",
    "SHOW_HISTORY": False,
    "ENVIRONMENT": "config.base.environment_callback",
    "DASHBOARD_CALLBACK": "app.unfold.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
    },
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    "TABS": [
        # {
        #     "models": [
        #         "auth.group", 
        #         "users.user"
        #     ],
        #     "items": [
        #         {
        #             "title": _("Users"),
        #             "icon": "sports_motorsports",
        #             "link": reverse_lazy("admin:users_user_changelist"),
        #         },
        #         {
        #             "title": _("Groups"),
        #             "icon": "precision_manufacturing",
        #             "link": reverse_lazy("admin:auth_group_changelist"),
        #         },
        #     ],
        # },
        {
            "models": [
                "django_celery_beat.clockedschedule",
                "django_celery_beat.crontabschedule",
                "django_celery_beat.intervalschedule",
                "django_celery_beat.periodictask",
                "django_celery_beat.solarschedule",
            ],
            "items": [
                {
                    "title": _("Clocked"),
                    "icon": "hourglass_bottom",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_clockedschedule_changelist"
                    ),
                },
                {
                    "title": _("Crontabs"),
                    "icon": "update",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_crontabschedule_changelist"
                    ),
                },
                {
                    "title": _("Intervals"),
                    "icon": "arrow_range",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_intervalschedule_changelist"
                    ),
                },
                {
                    "title": _("Periodic tasks"),
                    "icon": "task",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_periodictask_changelist"
                    ),
                },
                {
                    "title": _("Solar events"),
                    "icon": "event",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_solarschedule_changelist"
                    ),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "badge": "config.base.user_badge_callback",
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Tasks"),
                        "icon": "task_alt",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}


def environment_callback(request):
    mode =  env.str("SITE_MODE", "local")
    color = "info" if mode == "local" else "success"
    return [mode.capitalize, color]


def user_badge_callback(request):
    from app.users.models import User
    return User.objects.count()

# settings.py
WHITENOISE_AUTOREFRESH = True
