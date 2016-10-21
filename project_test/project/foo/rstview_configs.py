from rstview.registry import rstview_registry
from django.utils.translation import ugettext_lazy


rstview_registry.update({
    'bar': {
        'initial_header_level': 2,
        'language_code': "fr",
    },
})
