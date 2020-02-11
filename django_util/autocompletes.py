__all__ = 'autocomplete_factory',


from dal.autocomplete import Select2QuerySetView
from django.db.models.query_utils import Q
from functools import reduce
from operator import or_, __or__


def autocomplete_factory(
        ModelClass,   # TODO Py3.8: positional-only
        *, search_fields=(), min_input_len=0):
    class AutoComplete(Select2QuerySetView):
        __name__ = __qualname__ = name = \
            '{}AutoComplete'.format(ModelClass.__name__)

        data_min_input_len = min_input_len

        autocomplete_search_fields = \
            ['{}__icontains'.format(search_field)
             for search_field in search_fields] \
            if search_fields \
            else (ModelClass.autocomplete_search_fields()
                  if hasattr(ModelClass, 'autocomplete_search_fields')
                  else ['{}__icontains'.format(search_field)
                        for search_field in ModelClass.search_fields()])

        def get_queryset(self):
            return (ModelClass.objects.filter(
                        reduce(__or__,
                               (Q(**{autocomplete_search_field: self.q})
                                for autocomplete_search_field in self.autocomplete_search_fields)))
                    if self.q
                    else (ModelClass.objects.none()
                          if self.data_min_input_len
                          else ModelClass.objects.all())) \
                if self.request.user.is_authenticated \
              else ModelClass.objects.none()

    return AutoComplete
