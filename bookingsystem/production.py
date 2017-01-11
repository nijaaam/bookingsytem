from bookingsystem.settings import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'bdc872f41f048b',
        'PASSWORD': '1c11843c',
        'HOST': 'us-cdbr-azure-southcentral-f.cloudapp.net',
    }
}