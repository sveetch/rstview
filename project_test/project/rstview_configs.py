from rstview.registry import rstview_registry
from django.utils.translation import ugettext_lazy


rstview_registry.update({
    'full_page': {
        'initial_header_level': 1,
        'file_insertion_enabled': False,
        'raw_enabled': True,
        'language_code': "fr",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
    },
})
