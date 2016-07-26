.. _docutils: http://docutils.sourceforge.net/
.. _Django: https://www.djangoproject.com/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/

rstview
===================================

This is a simple `Django`_ application around `docutils`_ to parse `reStructuredText`_ markup.

.. Warning::
    Version 0.3.0 have major backward changes, see details in documentation changelogs.

Features
********

* Either **Html4 or Htmls5 writers** available;
* **Custom reporter** to validate source;
* **Dedicated view** to make a page from a rst source;
* **Template tag** to parse `reStructuredText`_ markup;
* Comes with **unittests**;

Links
*****

* Read the documentation on `Read the docs <http://rstview.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/rstview>`_;
* Clone it on its `Github repository <https://github.com/sveetch/rstview>`_;

Dependancies
************

* `Django`_ >= 1.7;
* `docutils`_ >= 0.7;
* Optionnaly (but recommended): `Pygments`_ >= 1.2.x to have highlighted syntax in your *sourcecode* blocks;
