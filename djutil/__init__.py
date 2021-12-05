__all__ = \
    'default_app_config', \
    'MAX_CHAR_FLD_LEN', \
    'snake_case', 'upper_case'


import re


# Django App Config
default_app_config = 'django_util.apps.UtilConfig'


MAX_CHAR_FLD_LEN = 255


def _clean(s):
    return re.sub('_{2,}', '_', re.sub('[^\w]+', '_', s).strip('_'))


def snake_case(s):
    return _clean(s).lower()


def upper_case(s):
    return _clean(s).upper()
