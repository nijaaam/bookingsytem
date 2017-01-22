from bookingsystem.settings import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'root',
        'PASSWORD': 'Bksysuser_2017',
        'HOST': 'mysql2704.cloudapp.net',
    }
}
