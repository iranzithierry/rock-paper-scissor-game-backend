import subprocess

def update_package(package):
    subprocess.run(['pip', 'install', package])

packages = [
    "pytz",
    "Django",
    "gunicorn",
    "newrelic",
    "django-dotenv",
    "django-3-jet",
    "celery",
    "psycopg2",
    "redis",
    "django-model-utils",
    "django_unique_upload",
    "django-summernote",
    "django-celery-beat",
    "django-activity-stream",
    "django-money",
    "djangorestframework",
    "djangorestframework-simplejwt",
    "Markdown",
    "drf-yasg",
    "django-filter",
    "django-cors-headers",
    "django-rest-passwordreset",
    "django-rest-swagger",
    "easy-thumbnails",
    "django-auto-prefetching",
    "social-auth-core",
    "social-auth-app-django",
    "ipython",
    "sentry-sdk",
    "django-inlinecss",
    "django-storages",
    "boto3",
    "django-health-check"
]

for package in packages:
    update_package(package)

# Freeze the current environment to requirements.txt
with open('requirements.txt', 'w') as f:
    subprocess.run(['pip', 'freeze'], stdout=f)



# jet/models.py
# from django.utils.translation import ugettext_lazy as _