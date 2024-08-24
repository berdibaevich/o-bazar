
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# load_dotenv() waziypasi bir jaratqan .env formatda file bar edi usilardin key valuesin oqiw ushin kerek boladi

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
PRODUCTION = int(os.environ.get('PRODUCTION', default=1))
ALLOWED_HOSTS = ['.pythonanywhere.com', '127.0.0.1']




# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mptt",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework",
    "algoliasearch_django",

    

    "inventory.apps.InventoryConfig",
    "basket.apps.BasketConfig",
    "account.apps.AccountConfig",
    "payment.apps.PaymentConfig",
    "orders.apps.OrdersConfig",
    "wishlist.apps.WishlistConfig",
    "checkout.apps.CheckoutConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/ 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "inventory.context_processors.categories",
                "basket.context_processors.basket",
                "wishlist.context_processors.wishlist",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#os.environ.get("ENGINE")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get('ENGINE', default="django.db.backends.sqlite3"),
        "NAME": os.environ.get('NAME', default= BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get('USER', default='user'),
        "PASSWORD": os.environ.get('PASSWORD', default='password'),
        "HOST": os.environ.get('HOST', default='localhost'),
        "PORT": os.environ.get('PORT', default='5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# FLOWERAURA URL
FLOWERAURA_URL = "https://www.floweraura.com"
# END FLOWERAURA URL


# BASKET
BASKET_SESSION_DATA = "basket"
# END BASKET

# WISHLIST
WISHLIST_SESSION_DATA = 'wishlist'
# END WISHLIST

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'account.Customer'

# SET UP LOGIN 
LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = 'account:dashboard'



# SETUP EMAIL GOOGLE 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com' #Bul GMAIL HOST bolip tabiladi
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', default='cool')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', default='cool')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# END SETUP EMAIL GOOGLE 

# PAYMENT KEYS ID
PUBLISHABLE_KEY = os.environ.get('PUBLISHABLE_KEY', default='cool')
PAYMENT_SECRET_KEY = os.environ.get('PAYMENT_SECRET_KEY', default='cool')
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET', default='cool')
# END PAYMENT KEYS ID



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "api.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication"

    ),
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.IsAuthenticated",
    ]
    
}


ALGOLIA = {
    'APPLICATION_ID': os.environ.get('APPLICATION_ID', default='cool'),
    'API_KEY': os.environ.get('API_KEY', default='cool'),
    'INDEX_PREFIX':  os.environ.get('INDEX_PREFIX', default='cool'),
}



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}