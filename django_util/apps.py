__all__ = 'UtilConfig',


from django.apps import AppConfig

import os


# # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig
class UtilConfig(AppConfig):
    # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.name
    name = 'django_util'

    # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.label
    label = 'DjangoUtil'

    # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.verbose_name
    verbose_name = 'Django Utilities'

    # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.path
    path = os.path.dirname(__file__)
