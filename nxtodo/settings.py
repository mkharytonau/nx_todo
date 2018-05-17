SECRET_KEY = 'REPLACE_ME123'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nxtodo_test',
        'USER': 'nxtodo',
        'PASSWORD': 'todotodo',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

INSTALLED_APPS = [
    'nxtodo_db'
]
