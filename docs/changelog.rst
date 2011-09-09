Changelog
=========

0.4.1 (2011-09-09)
------------------

* Fixed minor issue in installation documentation.

0.4 (2011-08-24)
----------------

* Renamed ``app_label`` attribute of the inner ``Meta`` class to ``prefix``.
  The old form ``app_label`` will work in the meantime.

* Added ``holder`` attribute to the inner ``Meta`` class to be able to
  specify a custom "global" setting holder. Default: "'django.conf.settings'"

* Added ``proxy`` attribute to the inner ``Meta`` class to enable proxying
  of ``AppConf`` instances to the settings holder, e.g. the global Django
  settings.

* Fixed issues with ``configured_data`` dictionary available in the
  ``configure`` method of ``AppConf`` classes with regard to subclassing.

0.3 (2011-08-23)
----------------

* Added tests with 100% coverage.

* Added ability to subclass ``Meta`` classes.

* Fixed various bugs with subclassing and configuration in subclasses.

0.2.2 (2011-08-22)
------------------

* Fixed another issue in the ``configure()`` API.

0.2.1 (2011-08-22)
------------------

* Fixed minor issue in ``configure()`` API.

0.2 (2011-08-22)
----------------

* Added ``configure()`` API to ``AppConf`` class which is called after
  configuring each setting.

0.1 (2011-08-22)
----------------

* First public release.
