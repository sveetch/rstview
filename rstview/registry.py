# -*- coding: utf-8 -*-
"""

.. _Docutils Configuration: http://docutils.sourceforge.net/docs/user/config.html

.. _registry-intro:

Configuration registry
======================

Registry store configurations by the way of its interface.

Default global registry is available at ``rstview.registry.rstview_registry``
and is global for the whole project and apps, you don't need to fill it again
for a same Django instance.

A configuration is a dictionnary of parameters for reStructuredText parser:

.. sourcecode:: python

    {
        'default': {
            'initial_header_level': 1,
            'language_code': "en",
        },
    }

Configuration name is used to retrieve parameters from the registry interface.

See `Docutils Configuration`_ for a full references of available parser
parameters.

"""


class RstviewConfigAlreadyRegistered(Exception):
    pass


class RstviewConfigNotRegistered(Exception):
    pass


class RstConfigSite(object):
    """
    Rstview configurations registry

    Keyword Arguments:
        initial (dict): Optional initial dictionnary of configuration. Default
        to an empty dict.
    """
    def __init__(self, *args, **kwargs):
        self._registry = kwargs.get('initial', {})

    def reset(self):
        """
        Reset registry to an empty Dict.
        """
        self._registry = {}

    def get_registry(self):
        """
        Return current registry

        Returns:
            dict: Currrent registry.
        """
        return self._registry

    def get_names(self):
        """
        Return registred configuration names.

        Returns:
            list: List of registred names, sorted with default ``sorted()``
            behavior.
        """
        return sorted(self._registry.keys())

    def has_name(self, name):
        """
        Find if given name is a registred configuration name.

        Returns:
            bool: ``True`` if name exists in current registry, else ``False``.
        """
        return name in self._registry

    def get_parameters(self, name):
        """
        Get parameters from given configuration name.

        Arguments:
            name (string): Configuration name.

        Returns:
            string or tuple: Configuration parameters.
        """
        if not self.has_name(name):
            msg = 'Given name "{}" is not registered as a configuration.'
            raise RstviewConfigNotRegistered(msg.format(name))
        return self._registry[name]

    def register(self, name, value):
        """
        Register a configuration for given name.

        Arguments:
            name (string): Configuration name.
            value (string or tuple): Configuration parameters to define.

        Raises:
            ``RstviewConfigAlreadyRegistered`` if name is allready registered in
            configurations.
        """
        if self.has_name(name):
            msg = 'Given name "{}" is already registered as a configuration.'
            raise RstviewConfigAlreadyRegistered(msg.format(name))

        self._registry[name] = value

    def unregister(self, name):
        """
        Unregister a configuration from its name.

        Arguments:
            name (string): Url name.

        Raises:
            ``RstviewConfigNotRegistered`` if given url name is not registred yet.
        """
        if not self.has_name(name):
            msg = 'Given name "{}" is not registered as a configuration.'
            raise RstviewConfigNotRegistered(msg.format(name))
        del self._registry[name]

    def update(self, configs):
        """
        Update many configuration.

        This works like the ``Dict.update({..})`` method.

        Arguments:
            configs (dict): A dict of configurations.
        """
        self._registry.update(configs)


#: Default rstview configurations registry for a Django instance.
rstview_registry = RstConfigSite()
