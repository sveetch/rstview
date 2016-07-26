
=========
Changelog
=========

Version 0.3.2 - 2016/07/26
--------------------------

* Fixed tests settings and conftest so tests can run correctly through tox;
* Added Django 1.7, Django 1.8, Django 1.9 support since these versions have passed tests through tox;


Version 0.3.1 - 2016/07/26
--------------------------

* First try to use tox for tests;

Version 0.3.0 - 2016/07/24
--------------------------

* Added unittests with Py.test and a dummy project for tests;
* Added better documentation using Sphinx+Autodoc+Napoleon;
* Now require for Django==1.8;
* **Major changes** in modules and structure:

  * ``rstview.parser`` has been refactored to contain everything in two classes;
  * Improved view ``rstview.views.RSTFileView`` to be more flexible;
  * Default shipped view template now inherits from ``skeleton.html`` instead of ``base.html``;
  * Template filter ``source_render`` has been dropped in profit of template tag ``rst_render`` which has more options;
  * Dropped old sample ``rstview/rst_sample.rst``;
  * ``rstview.views.RSTFileView`` now raise an exception if ``doc_path`` attributed is empty;

Version 0.2.1 - 2014/08/17
--------------------------

Minor update for README.

Version 0.2.0 - 2014/08/16
--------------------------

* Added ``source_render`` template filter;
* Updated README;
