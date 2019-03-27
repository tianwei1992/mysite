import os

from django.http import UnreadablePostError

def info_only(record):
    if record.levelname=="INFO":
        return True
    return False

ADMINS = (
     ('grace', 'tianweigrace@qq.com'),
)

MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'server_infos_only': {
        '()': 'django.utils.log.CallbackFilter',
        'callback': info_only,
    }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'simple'
            
        },
        
        'file_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/infos.log',
            
        },
        'server_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filters': ['server_infos_only'],
            'filename': 'logs/server_infos.log',
            'formatter': 'simple'
        },
        'article_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/article_infos.log',
            'formatter': 'simple'
        },
        'mailapi_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/mailapi_infos.log',
            'formatter': 'simple'
        },
        'image_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/image_infos.log',
            'formatter': 'simple'
        },
        'request_warnings': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/request_warnings.log',
            'formatter': 'simple'
        },
        'request_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/request_errors.log',
            
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_infos'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_warnings'],
            'level': 'WARNING',
            'propagate': False,# info recorded here,and will not be propagated to django logger
        },
        'django.server': {
            'handlers': ['server_infos'],
            'level': 'INFO',
            'propagate': False,# info recorded here,and will not be propagated to django logger
        },
        'mysite.error': {
            'handlers': ['file_errors', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        },
        'mysite.article.info': {
            'handlers': ['article_infos', ],
            'level': 'INFO', 
            'propagate': False
        },
        'mysite.mailapi.info': {
            'handlers': ['mailapi_infos', ],
            'level': 'INFO', 
            'propagate': False
        },
        'mysite.image.info': {
            'handlers': ['image_infos', ],
            'level': 'INFO', 
            'propagate': False
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}
