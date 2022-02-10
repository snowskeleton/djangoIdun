from royal.settings import BASE_DIR

PRODDB = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'treasure',
        'USER': 'king',
        'PASSWORD': 'gold',
        'HOST': 'localhost',
        'PORT': '', # leaving PORT blank makes it default, which is port 5432
    }
}
TESTDB = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}