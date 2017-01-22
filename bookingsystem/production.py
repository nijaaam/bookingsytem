from bookingsystem.settings import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'be47f6ef0ac9f4',
        'PASSWORD': 'cf66d796',
        'HOST': 'us-cdbr-azure-southcentral-f.cloudapp.net',
    }
}
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True