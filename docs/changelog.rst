
=========
Changelog
=========

Version 0.4.0 - 2016/10/23
--------------------------

* Added a configuration registry and use it instead of directly getting/setting configurations from ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``;
* Now configurations can be added/updated/removed per application through registry interface;
* Now ``settings.RSTVIEW_PARSER_FILTER_SETTINGS`` is only used as a startup configuration sets that are not needed to be tampered anymore;
* Added discovering methods to discover configuration files from enabled applications;
* Added tests for registry and discovering;
* Updated documentation to include configuration registry and all;
* Removed some unused settings:

  * ``RSTVIEW_PARSER_ENABLE_FILE_INSERTION``;
  * ``RSTVIEW_PARSER_ENABLE_RAW_INSERTION``;
  * ``RSTVIEW_PARSER_LANGUAGE_CODE``.

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
