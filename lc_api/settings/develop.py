"""
Django settings for lc_api project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 修改默认子应用的目录 将apps目录设置为全局的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-&)=8ceglcmk8lf-am60#b0h8p0jkk^u^d!#qs*6jv=u(tipgr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'xadmin',
    'crispy_forms',
    'reversion',
    'django_filters',
    # 富文本编辑器配置
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器的上传模块

    'home',
    'user',
    'course',
    'cart',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lc_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lc_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "api_lc",
        'HOST': "127.0.0.1",
        'PORT': 3306,
        'USER': "root",
        'PASSWORD': "123456",
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 允许跨域请求
CORS_ORIGIN_ALLOW_ALL = True

# 富文本编辑器
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 展示哪些工具栏
        'height': 300,  # 编辑器的高度
    },
}

CKEDITOR_UPLOAD_PATH = ''

JWT_AUTH = {
    # jwt 登录视图返回的数据的格式
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'user.utils.jwt_response_payload_handler',
    # token的过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),
}

# 自定义多条件登录方式
AUTHENTICATION_BACKENDS = [
    'user.utils.UserAuthBackend'
]

REST_FRAMEWORK = {
    # 全局异常配置
    "EXCEPTION_HANDLER": "lc_api.utils.exceptions.exception_handler",
}

# 注册自定义用户模型
AUTH_USER_MODEL = "user.UserInfo"

# redis连接配置
CACHES = {
    "default": {
        # 连接的客户端
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis的库
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码储存位置
    "sms_code": {
        # 连接的客户端
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis的库
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 购物车储存位置
    "cart": {
        # 连接的客户端
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis的库
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# 日志配置
LOGGING = {
    # 日志版本 唯一即可
    'version': 1,
    # 是否禁用项目中的已存在的日志器
    'disable_existing_loggers': False,
    # 格式化日志信息
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 日志的过滤信息
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理日志的方法
    'handlers': {
        # 打印到控制台的日志格式
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 记录到文件中的日志格式
        'file': {
            # 记录到文件中的日志级别
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的保存的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/lesson_api.log"),
            # 日志文件的大小  100M
            'maxBytes': 100 * 1024 * 1024,
            # 日志文件最大的数量
            'backupCount': 10,
            # 保存的日志格式
            'formatter': 'verbose'
        },
    },
    # Django日志对象
    'loggers': {
        'django': {
            # 生效的内容  打印控制台+日志文件的生成
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}
