.. Boussole documentation master file, created by
   sphinx-quickstart on Sun Mar  6 12:12:38 2016.

.. _docutils: http://docutils.sourceforge.net/
.. _Django: https://www.djangoproject.com/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/

Welcome to rstview's documentation!
===================================

This is a simple `Django`_ application around `docutils`_ to parse `reStructuredText`_ markup.

Features
********

* **Html4** and **Html5** writers available;
* **Custom reporter** to validate source;
* **Dedicated view** to make a page from a rst source;
* **Template tag** to directly parse `reStructuredText`_ markup;
* **Parser driven by configuration** so they can be shared without to define them again and again;
* **Configuration registry** to store multiple different parser configurations;
* **Test driven development**;

Links
*****

* Read the documentation on `Read the docs <http://rstview.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/rstview>`_;
* Clone it on its `Github repository <https://github.com/sveetch/rstview>`_;

Dependancies
************

* `Django`_ >= 1.7, <1.10;
* `docutils`_ >= 0.7;
* Optionnaly (but recommended): `Pygments`_ >= 1.2.x to have highlighted syntax in your *sourcecode* blocks;

User’s Guide
************

.. toctree::
   :maxdepth: 2

   install.rst
   library_references/templatetags.rst
   library_references/views.rst

References
**********

.. toctree::
   :maxdepth: 1

   settings.rst
   library_references/registry.rst
   library_references/discover.rst
   library_references/parser.rst
   library_references/html5writer.rst

Developer’s Guide
*****************

.. toctree::
   :maxdepth: 1

   development.rst
   changelog.rst
