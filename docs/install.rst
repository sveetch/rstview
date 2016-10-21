
=======
Install
=======

::

    pip install rstview


#. In your *settings* file add **rstview** to your installed apps:

    .. sourcecode:: python

        INSTALLED_APPS = (
            ...
            'rstview',
            ...
        )

#. Import default settings:

    .. sourcecode:: python

        from rstview.settings import *

#. Finally add these two lines in your main ``urls.py``:

    .. sourcecode:: python

        import rstview
        from rstview.discover import autodiscover
        autodiscover()

    This is optional but if you don't do this, all ``rstview_configs.py`` file will be
    ignored and only ``default`` parser configuration will be available.
