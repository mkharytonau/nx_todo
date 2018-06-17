SECRET_KEY = 'nxtodo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nxtodo',
        'USER': 'nxtodo',
        'PASSWORD': 'todotodo',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

INSTALLED_APPS = [
    'nxtodo.db'
]

TIME_ZONE = 'Europe/Moscow'
