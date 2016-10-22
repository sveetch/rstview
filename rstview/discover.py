# -*- coding: utf-8 -*-
"""

.. _discovering-intro:

Configuration discovering
=========================

Configurations are registred through files (called **configuration file**) that
are loaded as Python modules where some code can register needed
configurations.

Discovering will find these configuration files through project and its
enabled applications.

Usually you will want to use automatic discovering with the ``autodiscover``
function, so you just have to initiate it once from your project (like in your
root ``urls.py``) to load every configuration files.

In some uncommon cases you may need to do discovering yourself from your code,
use the ``discover`` function to do so.

.. Note:
    Once discovered, configurations from a configuration file are stored in
    registry for your Django instance and trying to discover it again won't do
    anything more.
"""
import copy
from django.conf import settings
from importlib import import_module
from django.utils.module_loading import module_has_submodule

from rstview.registry import rstview_registry


def discover(module_path, filename=None):
    """
    Try to discover and load a configuration file from given Python path.

    Example:

        Supposing you made a configuration file at
        ``myproject/myapp/rstview_configs.py``.

        .. sourcecode:: python
            :linenos:

            from rstview.discover import discover

            discover("myproject.myapp", "rstview_configs")

    Arguments:
        module_path (string): Python path to scan for ``filename`` module.

    Keyword Arguments:
        filename (string): Optional module filename to search for, default to
            ``None``.

    Raises:
        Exception: Raise any occuring exception from loaded Python path.

    Returns:
        string or None: Python path (``module.filename``) for discovered
        configuration module. If ``filename`` does not exists in module,
        return ``None``.
    """
    mod = import_module(module_path)
    name = module_path
    if filename:
        name = '{path}.{filename}'.format(path=module_path, filename=filename)

    # Attempt to import the app's admin module.
    try:
        # Keep registry safe in case of error
        before_import_registry = copy.copy(rstview_registry._registry)
        # Import configurations module
        import_module(name)
    except:
        # Reset the model registry to the state before exception occured
        rstview_registry._registry = before_import_registry

        # Only bubble up error if app have a configurations file, dont raise anything
        # if it lacks of if (unobtrusive way)
        if module_has_submodule(mod, filename):
            raise
        else:
            return None
    else:
        return name


def autodiscover(filename='rstview_configs'):
    """
    Automatic discovering for available configurations

    Before looking at configurations files, registry start from
    ``settings.RSTVIEW_PARSER_FILTER_SETTINGS`` items if setted, else an empty
    Dict.

    Then it try to load possible root configurations file defined in
    ``settings.RSTVIEW_PARSER_ROOT_CONFIGS`` (as a Python path).

    And finally load each configurations files finded in
    ``settings.INSTALLED_APPS``.

    Example:

        .. sourcecode:: python
            :linenos:

            from rstview.discover import autodiscover
            autodiscover()

        This is something you want to be executed early in your project,
        usually the ``urls.py`` of your project is the best choice.

    Keyword Arguments:
        filename (string): Module filename to search for. Default to
            ``rstview_configs``, so it will search for a ``rstview_configs.py``
            file at root of every enabled module from
            ``settings.INSTALLED_APPS``.

    Returns:
        list: List of successfully loaded Python paths.
    """
    paths = []

    # Directly fill registry from initial configurations setting
    rstview_registry.update(getattr(settings, 'RSTVIEW_PARSER_FILTER_SETTINGS',
                                        {}))

    # Fill path to discover from project level if any
    root_configurations = getattr(settings, 'RSTVIEW_PARSER_ROOT_CONFIGS', None)
    if root_configurations:
        paths.append(discover(root_configurations))

    # Fill paths to discover from installed apps
    apps = list(settings.INSTALLED_APPS)

    paths = paths + [discover(app, filename=filename) for app in apps]

    return filter(None, paths)
