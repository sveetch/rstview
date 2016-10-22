
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

#. Finally add these lines in your main ``urls.py``:

    .. sourcecode:: python

        from rstview.discover import autodiscover
        autodiscover()

    You may also try to do discovering yourself from your code, see
    :ref:`discovering-intro`. For details about registry and configuration
    see :ref:`registry-intro`.

Now you can use rstview either from :ref:`templatetags-intro` or :ref:`views-intro`.