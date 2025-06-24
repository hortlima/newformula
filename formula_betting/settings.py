from pathlib import Path
import django_heroku
import os
import dj_database_url

# Configura banco do Heroku
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Ative as configurações do Heroku
django_heroku.settings(locals())

# Adicione o host do heroku no ALLOWED_HOSTS
ALLOWED_HOSTS = ['formula-betting.herokuapp.com', 'localhost']

# DEBUG geralmente False em produção
DEBUG = False

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# Application definition

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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

ROOT_URLCONF = 'formula_betting.urls'

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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'deploy.wsgi'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Fórmula Betting Admin",
    "site_header": "Fórmula Betting",
    "site_brand": "Fórmula Betting",
    "welcome_sign": "Bem-vindo ao Painel Fórmula Betting",
    "copyright": "Fórmula Betting © 2025",
    "search_model": "core.piloto",  # busca rápida pelo modelo Piloto

    # Tema / cores:
    "show_ui_builder": True,        # interface visual para configurar Jazzmin
    "theme": "darkly",              # tema visual (vários disponíveis)
    
    # Navegação lateral:
    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"name": "Ranking Pilotos", "url": "public/ranking/pilotos/", "permissions": ["core.view_piloto"]},
        {"name": "Ranking Equipes", "url": "public/ranking/equipes/", "permissions": ["core.view_equipe"]},
        {"model": "core.corrida"},
    ],
    "usermenu_links": [
        {"name": "Sair", "url": "/admin/logout/", "icon": "fas fa-sign-out-alt"},
    ],
    
    # Menu lateral customizado:
    "order_with_respect_to": [
        "core.equipe",
        "core.piloto",
        "core.corrida",
        "core.resultado",
    ],

    # Mostrar ou esconder ícones:
    "icons": {
        "core.equipe": "fas fa-flag",
        "core.piloto": "fas fa-user",
        "core.corrida": "fas fa-flag-checkered",
        "core.resultado": "fas fa-trophy",
    },

    # Itens do menu colapsados inicialmente?
    "navigation_expanded": True,

    # Mostrar menu lateral ou não
    "show_sidebar": True,

    # Branding do login page
    "login_logo": None,  # URL para logo customizada na página login (pode ser static url)
    "login_logo_dark": None,
    
    # Usar ícones FontAwesome
    "icons_pack": "fas",

    # Botão para ir para a dashboard depois de login
    "show_navbar": True,
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Formula Betting API',
    'DESCRIPTION': 'API pública para visitantes e usuários autenticados.',
    'VERSION': '1.0.0',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
