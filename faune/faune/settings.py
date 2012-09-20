# Django settings for faune project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASE_ID = 'default'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'appli_faune',                      # Or path to database file if using sqlite3.
        'USER': 'gisuser',                      # Not used with sqlite3.
        'PASSWORD': 'Rivirwaktim9',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2&amp;a^+yahrzn--_7f3-rr#-uu@6%93t)upl(mc0d$puonvj0yq)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'faune.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'faune.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'faune',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False, # this tells logger to send logging message
                                # to its parent (will send if set to True)
        },        
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }        
    }
}


TOKEN = "666"

TABLE_TAXON = 'taxonomie.bib_taxons_faune_pne'
TABLE_FAMILY = 'taxonomie.bib_familles'
TABLE_UNITY = 'layers.l_unites_geo'
TABLE_TAXON_UNITY = 'contactfaune.cor_unite_taxon'
TABLE_CRITERION = 'contactfaune.bib_criteres_cf'
TABLE_USER = 'utilisateurs.t_roles'
TABLE_STATEMENT = 'contactfaune.t_releves_cf'
TABLE_SHEET = 'contactfaune.t_fiches_cf'
TABLE_SHEET_ROLE = 'contactfaune.cor_role_fiche_cf'
TABLE_FAILED_JSON = 'synchronomade.erreurs_cf'

FAUNE_TABLE_INFOS =  {
    TABLE_FAILED_JSON: {
        'id_col': 'id',
        'select_col': 'id,json_date_import'
    },
    TABLE_SHEET_ROLE: {
        #'id_col': 'id_role',
        'select_col': 'id_cf,id_role',
        'json_to_db_columns' : {
            'id_cf' : 'id_cf', 
            'observer_id' : 'id_role'    
        }        
    },    
    TABLE_STATEMENT: {
        'id_col': 'id_releve_cf',
        'select_col': 'id_releve_cf, id_cf, id_taxon, id_critere_cf, am, af, ai, na, sai, jeune, yearling, nom_taxon_saisi, commentaire, supprime, prelevement',
        'json_to_db_columns' : {
            'id_cf' : 'id_cf', 
            'id' : 'id_taxon',
            'criterion' : 'id_critere_cf',
            'adult_male' : 'am',
            'adult_female' : 'af',
            'adult' : 'ai',
            'not_adult' : 'na',
            'sex_age_unspecified' : 'sai',
            'young' : 'jeune',
            'yearling' : 'yearling',
            'name_entered' : 'nom_taxon_saisi',
            'comment' : 'commentaire',
            'supprime' : 'supprime',
            'sample' : 'prelevement'    
        }        
    },
    TABLE_SHEET: {
        'id_col': 'id_cf',
        'select_col': 'id_cf, dateobs, altitude_saisie, supprime, pdop, the_geom_2154, saisie_initiale, id_organisme, id_protocole, id_lot',
        'json_to_db_columns' : {
            'dateobs' : 'dateobs',
            'altitude' : 'altitude_saisie',
            'supprime' : 'supprime',
            'accuracy' : 'pdop',
            'geometry' : 'the_geom_2154',
            'initial_input' : 'saisie_initiale'
        }        
    },
    TABLE_TAXON: {
        'id_col': 'id_taxon',
        'json_name': 'taxa',
        'select_col': 'id_taxon, nom_latin, nom_francais, id_famille',
        'db_to_json_columns' : {
            'id_taxon' : 'id',
            'nom_latin' : 'name',
            'nom_francais' : 'name_fr',
            'id_famille' : 'family_id'
        }
    },
    TABLE_FAMILY: {
        'id_col': 'id_famille',
        'json_name': 'family',
        'select_col': 'id_famille, nom_famille',
        'db_to_json_columns' : {
            'id_famille' : 'id',
            'nom_famille' : 'name'
        }
    },
    TABLE_UNITY: {
        'id_col': 'id_unite_geo',
        'json_name': 'unity',
        'select_col': 'id_unite_geo, code_insee, commune',
        'db_to_json_columns' : {
            'id_unite_geo' : 'id',
            'code_insee' : 'insee',
            'commune' : 'city'
        }        
    },
    TABLE_TAXON_UNITY: {
        'id_col': 'id_unite_geo',
        'json_name': 'taxa_unity',
        'select_col': 'id_unite_geo, id_taxon, derniere_date, couleur, nb_obs',
        'db_to_json_columns' : {
            'id_unite_geo' : 'unite_geo_id',
            'id_taxon' : 'taxon_id',
            'derniere_date' : 'date',
            'couleur' : 'color',
            'nb_obs' : 'nb_obs'
        }        
    },
    TABLE_CRITERION: {
        'id_col': 'id_critere_cf',
        'json_name': 'criterion',
        'select_col': 'id_critere_cf, code_critere_cf, nom_critere_cf, tri_cf, cincomplet',
        'db_to_json_columns' : {
            'id_critere_cf' : 'id',
            'code_critere_cf' : 'code',
            'nom_critere_cf' : 'name',
            'tri_cf' : 'sort',
            'cincomplet' : 'incomplete'
        }        
    },
    TABLE_USER: {
        'id_col': 'id_role',
        'json_name': 'user',
        'select_col': 'id_role, identifiant, nom_role, prenom_role, organisme',
        'db_to_json_columns' : {
            'id_role' : 'id',
            'identifiant' : 'ident',
            'nom_role' : 'last_name',
            'prenom_role' : 'first_name',
            'organisme' : 'organism'
        }        
    }    
}
