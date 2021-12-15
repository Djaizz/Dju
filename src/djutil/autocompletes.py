"""AutoComplete Utilities."""


from functools import reduce
from operator import __or__
from sys import version_info

from dal.autocomplete import Select2QuerySetView
from django.db.models.base import ModelBase
from django.db.models.query_utils import Q

if version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


__all__: Sequence[str] = ('autocomplete_factory',)


def autocomplete_factory(
        ModelClass: ModelBase, /,   # noqa: N803
        *, search_fields: Sequence[str] = (), min_input_len: int = 0):
    """Create a DAL AutoComplete from a Django object model class."""
    class AutoComplete(Select2QuerySetView):
        # pylint: disable=too-many-ancestors
        """AutoComplete class."""

        __name__ = __qualname__ = name = f'{ModelClass.__name__}AutoComplete'

        data_min_input_len = min_input_len

        autocomplete_search_fields = (
            [f'{search_field}__icontains'
             for search_field in search_fields]
            if search_fields
            else (ModelClass.autocomplete_search_fields()
                  if hasattr(ModelClass, 'autocomplete_search_fields')
                  else [f'{search_field}__icontains'
                        for search_field in ModelClass.search_fields()]))

        def get_queryset(self):
            if self.request.user.is_authenticated:

                if self.q:
                    return ModelClass.objects.filter(
                        reduce(__or__,
                               (Q(**{autocomplete_search_field: self.q})
                                for autocomplete_search_field
                                in self.autocomplete_search_fields)))

                if self.data_min_input_len:
                    return ModelClass.objects.none()

                return ModelClass.objects.all()

            return ModelClass.objects.none()

    return AutoComplete
