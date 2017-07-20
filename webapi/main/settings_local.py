# Django settings for webapi project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
    },
    'fauna': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geonaturedb',
        'USER': 'geonatuser',
        'PASSWORD': 'monpassachanger',
        'HOST': '92.222.107.92',
        'PORT': '5432'
    },
    'inv': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geonaturedb',
        'USER': 'geonatuser',
        'PASSWORD': 'monpassachanger',
        'HOST': '92.222.107.92',
        'PORT': '5432'
    },
    'flora': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geonaturedb',
        'USER': 'geonatuser',
        'PASSWORD': 'monpassachanger',
        'HOST': '92.222.107.92',
        'PORT': '5432'
    }
}

TOKEN = "mon!token#complexe"

# local projection
LOCAL_SRID = 2154

# Fauna meta default values
FAUNA_ID_ORGANISM = 2
FAUNA_ID_PROTOCOL = 1
FAUNA_ID_LOT = 1

# Mortality meta values
MORTALITY_ID_ORGANISM = 2
MORTALITY_ID_PROTOCOL = 2
MORTALITY_ID_LOT = 2

# Invertebrate meta default values
INVERTEBRATE_ID_ORGANISM = 2
INVERTEBRATE_ID_PROTOCOL = 3
INVERTEBRATE_ID_LOT = 3

# Flora meta default values
FLORA_ID_ORGANISM = 2
FLORA_ID_PROTOCOL = 4
FLORA_ID_LOT = 4

MOBILE_SOFT_PATH = "/home/gil/synchronomade/webapi/apk/"
MOBILE_FILE_PATH = "/home/gil/synchronomade/webapi/datas/"

#use to synchronize flora data with a other db via a sript (Talend job for exemple) - Optionnal
SYNC_DB_CMD = ""
