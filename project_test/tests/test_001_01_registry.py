import pytest

from rstview.registry import RstviewConfigAlreadyRegistered, RstviewConfigNotRegistered, RstConfigSite


def test_registry_empty():
    """Initial empty registry"""
    registry = RstConfigSite()

    assert registry.get_registry() == {}


def test_registry_initial():
    """Registry initially filled"""
    registry = RstConfigSite()
    registry.update({
        'foo': 42,
        'bar': {
            'yep': 'yap',
            'pika': True,
        },
    })

    assert registry.get_registry() == {
        'foo': 42,
        'bar': {
            'yep': 'yap',
            'pika': True,
        },
    }


def test_reset():
    """Reseting registry"""
    registry = RstConfigSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })
    registry.reset()

    assert registry.get_registry() == {}


def test_names():
    """Get registred names"""
    registry = RstConfigSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.get_names() == [
        'bar',
        'foo',
    ]


@pytest.mark.parametrize("name,exists", [
    ('foo', True),
    ('bar', True),
    ('nope', False),
    ('Foo', False),
])
def test_hasname(name, exists):
    """Check if a name exist in registry"""
    registry = RstConfigSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.has_name(name) == exists


def test_getparameters():
    """Check if a title exist in registry"""
    registry = RstConfigSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.get_parameters('foo') == 42

    with pytest.raises(RstviewConfigNotRegistered):
        registry.get_parameters('nope')


def test_register():
    """Register title"""
    registry = RstConfigSite()

    registry.register('foo', True)
    registry.register('bar', 42)

    assert registry.get_names() == [
        'bar',
        'foo',
    ]

    with pytest.raises(RstviewConfigAlreadyRegistered):
        registry.register('foo', True)


def test_unregister():
    """Unregister title"""
    registry = RstConfigSite()

    registry.register('foo', True)
    registry.register('bar', 42)

    assert registry.get_names() == [
        'bar',
        'foo',
    ]

    registry.unregister('foo')
    assert registry.get_names() == [
        'bar',
    ]

    with pytest.raises(RstviewConfigNotRegistered):
        registry.unregister('plip')
