# mywebsite/settings/production.py
from .base import *
import os
from decouple import config

# 强制 HTTPS (PA 其实已经在 Nginx 层做了，但 Djano 层也实现一下)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 2. 防止浏览器猜测内容类型 (X-Content-Type-Options: nosniff)
SECURE_CONTENT_TYPE_NOSNIFF = True

# 3. 防止点击劫持 (X-Frame-Options: DENY) - 禁止别人用 iframe 嵌入你的网站
X_FRAME_OPTIONS = 'DENY'

# 4. HSTS (告诉浏览器未来一年只用 HTTPS 访问，防降级攻击)
SECURE_HSTS_SECONDS = 31536000 # 1年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True



# 回退两级，找到 my_portfolio_django 根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 使用 / 操作符拼接路径，这回肯定没问题了
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = False

ALLOWED_HOSTS = [
    'xiqiao.pythonanywhere.com',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'django.log',
            'formatter': 'verbose',
            'level': 'INFO',
        },
    },

    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

# 生产环境使用数据库缓存 (因为 PA 免费版不支持 Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table', # 记得在线上运行 createcachetable
    }
}

GITHUB_CLIENT_ID = config('GITHUB_CLIENT_ID')

# 接收报错邮件的人
ADMINS = [
    ('XiQiao', '2377392781@qq.com'), 
]

SERVER_EMAIL = EMAIL_HOST_USER

# 开启邮件通知 (默认 DEBUG=False 时会自动开启，但显式写出来更好)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True, # 邮件里包含详细的 HTML 报错堆栈
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

CORS_ALLOW_ALL_ORIGINS = False