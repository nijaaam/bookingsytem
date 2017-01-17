from bookingsystem.settings import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'baa0d1902a2abe',
        'PASSWORD': '9be677e6',
        'HOST': 'us-cdbr-azure-southcentral-f.cloudapp.net',
    }
}
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True