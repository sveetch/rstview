import pytest
"""
WARNING: There is an issue with the way registry is feeded.

Imports are cached, so if we try to reset the registry between
tests, configurations modules won't feed them again during discovering, even
trying to import them manually (without importlib).

Tampering ``sys.modules`` would seem a solution:

    http://stackoverflow.com/questions/2918898/prevent-python-from-caching-the-imported-modules
"""


def test_autodiscover():
    """Check registred crumb names after autodiscover"""
    from rstview.registry import rstview_registry

    # Autodiscovering is disabled since it allready have be executed
    # previously, see previous warning
    #from rstview.discover import autodiscover
    #print autodiscover()

    assert rstview_registry.get_names() == [
        'bar',
        'default',
        'full_page',
    ]
