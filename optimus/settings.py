"""
Django settings for optimus project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE DIR IS :",BASE_DIR)

DEBUG = True

if DEBUG == False:
    STATIC_PATH = "/home/optimus/optimus/static"
else:
    STATIC_PATH = "path/to/static/files"
    #STATIC_PATH = os.path.join(BASE_DIR,'static')

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cjjzz&t3y_izmk_26n@0_4cnbadk$oj!jkgd)(m&7fr4ubf-o='

# SECURITY WARNING: don't run with debug turned on in production!


if DEBUG == False:
    # IP of the server hosting this app
    ALLOWED_HOSTS = ['xxx.xxx.xx.xx']
else:
    print("DEBUG'S TRUE..")
    ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'entrypoint',
    'merchantportal',
    'example',
    'api',
# visitor app was made to create a tracking and analytics platform of deals and cablets. It's advised to use analytics software than creating this from scratch     
    'visitor',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'subdomains.middleware.SubdomainURLRoutingMiddleware'
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optimus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'optimus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',                     

    }
}


# This is required. Configure your gmail to send mails via Django
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@example.com'
EMAIL_HOST_PASSWORD = 'verystrongpass'
EMAIL_PORT = 587


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )    
    
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

if DEBUG == True:
    STATICFILES_DIRS = [
    STATIC_PATH,
]

#Commented out in Production


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     '/home/optimus/optimus/static',
# ]

STATIC_URL = '/static/'

MEDIA_URL = '/media/'



UPLOAD_ROOT = os.path.join(BASE_DIR,'media/merchant_ads/')

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

LOGIN_URL = 'login/'

LOGIN_REDIRECT_URL = '/'



SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 600