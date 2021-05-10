"""
Django settings for quetripproj project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vv=gx&1m_ishf3ajz=d+6v33r=y-&2cndnf^_%)8*=8^f+i+&_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [u'quetrip.pythonanywhere.com']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.smtp2go.com'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'Stephen Apgar'
EMAIL_HOST_PASSWORD = 'developer1'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'quetrip.apps.QuetripConfig',
    'imageagent.apps.ImageagentConfig',
    'rakubaru.apps.RakubaruConfig',
    'fcm_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quetripproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

WSGI_APPLICATION = 'quetripproj.wsgi.application'

DATA_UPLOAD_MAX_MEMORY_SIZE = 115242880


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
         },

        'NAME': 'quetrip$quetrip',
        'USER': 'quetrip',
        'PASSWORD': '!@#$%qwe12345',
        'HOST': 'quetrip.mysql.pythonanywhere-services.com'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = u'/home/quetrip/quetripproj/media'
MEDIA_URL = '/media/'
STATIC_ROOT = u'/home/quetrip/quetripproj/quetrip/static'
STATIC_URL = '/static/'


URL = 'https://quetrip.pythonanywhere.com'

STRIPE_LIVE_SECRET_KEY = 'sk_live_FrETYIQLBZjBTtku3f9qY5gW00BiW8D9am'
STRIPE_LIVE_PUBLISHABLE_KEY = 'pk_live_Q125kVLntw5C7lbdRX6ddieS00h1uiQcrO'

STRIPE_TEST_SECRET_KEY = 'sk_test_u6HA6YZmhTIFARTAeY3uSeTL00jyxWKGx0'
STRIPE_TEST_PUBLISHABLE_KEY = 'pk_test_GnPzL8V8zCUsSMWm1zaXkh8W007SDjHEIm'

FCM_LEGACY_SERVER_KEY = 'AIzaSyAIgCUoyB12xwSvQDE2An35BHOaUgytdmA'

IMAGEAGENT_ADMIN_EMAIL = 'softwaredeveloper19630@gmail.com'

RAKUBARU_ADMIN_EMAIL = 'rakubaru2020@gmail.com'
# RAKUBARU_ADMIN_EMAIL = 'softwaredeveloper19630@gmail.com'




































