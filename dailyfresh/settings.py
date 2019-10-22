#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import tinymce


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0ev2e334&=53s6=8msn%18yj94sru1-9vx7@tth&)7rkbp2o-x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',  # 使用富文本编辑框
    'haystack',  # 注册全文检索框架
    'cart',
    'goods',
    'order',
    'user',

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

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'daily_fresh',
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS': {
            # 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'sql_mode': 'traditional',
        }
    }
}

# django认证系统使用的模型
AUTH_USER_MODEL = 'user.User'

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

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'  # 后台管理改为中文

TIME_ZONE = 'Asia/Shanghai'  # 时区改为上海

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 数据库取为国际时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# 富文本编辑框的使用配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}
# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp的地址
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'zhenheweiwei@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'wei123456'
# 收件人看到的发件人
EMAIL_FROM = '天天生鲜<zhenheweiwei@163.com>'

# Django的缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.6.109:6379/9",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}
# 配置session存储
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# 配置登录url地址
LOGIN_URL = '/user/login'

# 设置Django的文件存储类
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'

# 设置fdfs使用的client.conf文件路径
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置fdfs存储服务器上nginx的IP和port
FDFS_URL = 'http://192.168.6.109:8888'

# 全文检索配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 搜索结果默认显示个数，默认为20
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
