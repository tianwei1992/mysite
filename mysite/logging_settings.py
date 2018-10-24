import os

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
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
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
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'verbose'
        },
        
        'file_infos': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/infos.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_infos'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'mysite.error': {
            'handlers': ['file_errors', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': True
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}
