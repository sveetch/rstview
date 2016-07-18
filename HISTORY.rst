
=========
Changelog
=========

Version 0.3.0 - Unreleased
--------------------------

* Added unittests with Py.test and a dummy project for tests;
* Now require for Django==1.8;
* Major changes in modules and structure:

  * ``rstview.parser.SilentReporter`` has moved to ``rstview.reporter.SilentReporter``;
  * ``rstview.parser.SourceReporter`` has moved to ``rstview.reporter.SourceReporter``;
  * ``rstview.parser.map_parsing_errors`` has moved to ``rstview.reporter.format_parsing_errors``;
  * Improved view ``rstview.views.RSTFileView`` to be more flexible;
  * Default shipped view template now inherits from ``skeleton.html`` instead of ``base.html``;

Version 0.2.1 - 2014/08/17
--------------------------

Minor update for README.

Version 0.2.0 - 2014/08/16
--------------------------

* Added ``source_render`` template filter;
* Updated README;
