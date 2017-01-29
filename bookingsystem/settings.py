import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AZURE_ACCOUNT_NAME = "dbbackupbksys"
AZURE_ACCOUNT_KEY  = 'CkD5/KNWSF/BV4sM0XcnyrfBgPmZXjQW4i/FR4l2wX2Mn/PMZtZ/5u9D2wP6JUpXHDyJUwDtaiAECnuOYBPmfw=='
AZURE_CONTAINER = 'fullbkup'

DEFAULT_FILE_STORAGE = 'storage.AzureStorage'
DBBACKUP_STORAGE = DEFAULT_FILE_STORAGE

DBBACKUP_STORAGE_OPTIONS = {
    'container': AZURE_ACCOUNT_NAME,
    'account_name': AZURE_ACCOUNT_NAME,
    'account_key': AZURE_ACCOUNT_KEY,
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x3h)318k2awulf%&e@z08!tswh21&tbt!wdya4osy5o797l_7('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
ALLOWED_HOSTS = ['*']
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

STATICFILES_FINDERS = (
    "djangobower.finders.BowerFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

BOWER_INSTALLED_APPS = (
    'eonasdan-bootstrap-datetimepicker#latest',
    'fullcalendar',
    'fullcalendar-scheduler',
)

# Application definition

INSTALLED_APPS = (
    'bksys',
    'djangobower',
    'tablet',
    'widget_tweaks',
    'dbbackup',
    'storages',
    'coverage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'bookingsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookingsystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'root',
        'PASSWORD': '123',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

