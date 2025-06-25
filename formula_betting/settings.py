import os
from pathlib import Path
import dj_database_url
import django_heroku
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta
SECRET_KEY = os.environ.get("SECRET_KEY", "chave-insegura-para-dev-apenas")

# Hosts permitidos
ALLOWED_HOSTS = ['formula-betting-2aa7aceb65d3.herokuapp.com', 'localhost']
DEBUG = True

# Aplicações instaladas
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'core',
    'cloudinary',
    'cloudinary_storage',
]

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhjqox1vm',
    'API_KEY': '991611127697474',
    'API_SECRET': 'A0A-6_pcWcVc9Xa91FzwCATdjLc',
}

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL raiz
ROOT_URLCONF = 'formula_betting.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'formula_betting.wsgi.application'

# Banco de dados
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e mídia
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Chave de auto primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# Esquema OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Formula Betting API',
    'DESCRIPTION': 'API pública para visitantes e usuários autenticados.',
    'VERSION': '1.0.0',
}

# Configurações do Jazzmin (Admin bonito)
JAZZMIN_SETTINGS = {
    "site_title": "Fórmula Betting Admin",
    "site_header": "Fórmula Betting",
    "site_brand": "Fórmula Betting",
    "welcome_sign": "Bem-vindo ao Painel Fórmula Betting",
    "copyright": "Fórmula Betting © 2025",
    "search_model": "core.piloto",

    "show_ui_builder": True,
    "theme": "darkly",

    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"name": "Ranking Pilotos", "url": "public/ranking/pilotos/", "permissions": ["core.view_piloto"]},
        {"name": "Ranking Equipes", "url": "public/ranking/equipes/", "permissions": ["core.view_equipe"]},
        {"model": "core.corrida"},
    ],
    "usermenu_links": [
        {"name": "Sair", "url": "/admin/logout/", "icon": "fas fa-sign-out-alt"},
    ],
    "order_with_respect_to": [
        "core.equipe",
        "core.piloto",
        "core.corrida",
        "core.resultado",
    ],
    "icons": {
        "core.equipe": "fas fa-flag",
        "core.piloto": "fas fa-user",
        "core.corrida": "fas fa-flag-checkered",
        "core.resultado": "fas fa-trophy",
    },
    "navigation_expanded": True,
    "show_sidebar": True,
    "login_logo": None,
    "login_logo_dark": None,
    "icons_pack": "fas",
    "show_navbar": True,
}

# Integração com Heroku (deve ser a última linha!)
django_heroku.settings(locals())

