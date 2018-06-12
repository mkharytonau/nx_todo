SECRET_KEY = 'nxtodo_cli'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nxtodo_cli',
        'USER': 'nxtodo_cli',
        'PASSWORD': 'nxtodo_cli',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

INSTALLED_APPS = [
    'nxtodo.nxtodo_db'
]

TIME_ZONE = 'Europe/Moscow'