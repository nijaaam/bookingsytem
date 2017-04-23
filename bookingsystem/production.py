from bookingsystem.settings import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksys',
        'USER': 'root',
        'PASSWORD': 'Bksysuser_2017',
        'HOST': 'mysql2704.cloudapp.net',
    }
}
