"""String Utilities."""


import re
from sys import version_info

if version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


__all__: Sequence[str] = 'MAX_CHAR_FLD_LEN', 'snake_case', 'upper_case'


MAX_CHAR_FLD_LEN: int = 255


def _clean(s: str, /) -> str:
    return re.sub('_{2,}', '_', re.sub(r'[^\w]+', '_', s).strip('_'))


def snake_case(s: str, /) -> str:
    """Snake-case a string."""
    return _clean(s).lower()


def upper_case(s: str, /) -> str:
    """Upper-case a string."""
    return _clean(s).upper()
