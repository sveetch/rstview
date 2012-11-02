.. _docutils: http://docutils.sourceforge.net/
.. _Django: https://www.djangoproject.com/
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/
.. _PyPi package: http://pypi.python.org/pypi/rstview
.. _Github repositor: https://github.com/sveetch/rstview

Introduction
============

This is a simple `Django`_ application to parse content with `ReStructuredText`_ from `docutils`_ to HTML5 or HTML4 (suitable for XHTML).

Links
*****

* Download his `PyPi package`_;
* Clone it on his `Github repositor`_;

Requires
========

* `docutils`_ >= 0.7;

Optionnaly (but recommended) you can install **Pygments** to have highlighted syntax in your *sourcecode* block :

* `Pygments`_ >= 1.2.x;

Installation
============

Just register the app in your project settings like this :

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'rstview',
        ...
    )

If needed you can change some options, see the "local_settings.py" file to find the available option variables and overwrite them in your project settings file.

Usage
=====

Simpliest usage is to display a ReStructuredText file, like a "README.rst" from a project, assuming the file is a path below your Django project, you can add it to your project "urls.py" file like this :
    
.. sourcecode:: python

    ...
    from rstview.views import RSTFileView
    ...
    urlpatterns = patterns('',
        ...
        url(r'^README$', RSTFileView.as_view(doc_file_path="../README.rst", doc_title="Notice"), name='project-readme'),
        ...
    )

Default settings is to render document as HTML5, you can change this behaviour to a HTML4 render that is also suitable to use in XHTML documents, see ``local_settings.RSTVIEW_PARSER_WRITER`` and override it in ``settings.RSTVIEW_PARSER_WRITER``.

RSTFileView
***********

This generic view takes three optional arguments :

* **doc_file_path** : the file path to parse as ReStructuredText file to render;
* **doc_title** : the title for the document;
* **template_name** : a custom template file path, by default this is ``rstview/fileview.html``.
