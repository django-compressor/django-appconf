django-appconf
==============

An app configuration object to be used for handling configuration
defaults of packaged apps gracefully. Say you have an app called ``myapp``
and want to define a few defaults, and refer to the defaults easily in the
apps code. Add a ``settings.py`` to your app's models.py::

    from appconf import AppConf

    class MyAppConf(AppConf):
        SETTING_1 = "one"
        SETTING_2 = (
            "two",
        )

        class Meta:
            app_label = 'myapp'

The settings are initialized with the app label of where the setting is
located at. E.g. if your ``models.py`` is in the ``myapp`` package,
the prefix of the settings will be ``MYAPP``.

The ``MyAppConf`` class will automatically look at Django's
global setting to determine each of the settings. E.g. adding this to
your site's ``settings.py`` will set the ``SETTING_1`` app setting
accordingly::

    MYAPP_SETTING_1 = "uno"

Usage
-----

Instead of using ``from django.conf import settings`` as you would
usually do, you can **optionally** switch to using your apps own
settings module to access the settings::

    from myapp.models import MyAppConf

    myapp_settings = MyAppConf()

    print myapp_settings.MYAPP_SETTING_1

``AppConf`` class automatically work as proxies for the other
settings, which aren't related to the app. For example the following
code is perfectly valid::

    from myapp.models import MyAppConf

    settings = MyAppConf()

    if "myapp" in settings.INSTALLED_APPS:
        print "yay, myapp is installed!"

In case you want to set some settings ad-hoc, you can simply pass
the value when instantiating the ``AppConf`` class::

    from myapp.models import MyAppConf

    settings = MyAppConf(SETTING_1='something completely different')

    if 'different' in settings.MYAPP_SETTINGS_1:
        print 'yay, I'm different!'

Custom handling
---------------

Each of the settings can be individually configured with callbacks.
For example, in case a value of a setting depends on other settings
or other dependencies. The following example sets one setting to a
different value depending on a global setting::

    from django.conf import settings
    from appconf import AppConf

    class MyCustomAppConf(AppConf):
        ENABLED = True

        def configure_enabled(self, value):
            return value and not self.DEBUG

The value of ``MYAPP_ENABLED`` will vary depending on the
value of the global ``DEBUG`` setting.

Each of the app settings can be customized by providing
a method ``configure_<lower_setting_name>`` that takes the default
value as defined in the class attributes as the only parameter.
The method needs to return the value to be use for the setting in
question.

After each of the ``_configure`` method have be called, the ``AppConf``
class will additionally call a main ``configure`` method, which can
be used to do any further custom configuration handling, e.g. if multiple
settings depend on each other. For that a ``configured_data`` dictionary
is provided in the setting instance::


    from django.conf import settings
    from appconf import AppConf

    class MyCustomAppConf(AppConf):
        ENABLED = True
        MODE = 'development'

        def configure_enabled(self, value):
            return value and not self.DEBUG

        def configure(self):
            mode = self.configured_data['MODE']
            enabled = self.configured_data['ENABLED']
            if not enabled and mode != 'development':
                print "WARNING: app not enabled in %s mode!" % mode

Changelog
---------

0.3 (2011-08-23)
^^^^^^^^^^^^^^^^

* Added tests with 100% coverage.

* Added ability to subclass ``Meta`` classes.

* Fixed various bugs with subclassing and configuration in subclasses.

0.2.2 (2011-08-22)
^^^^^^^^^^^^^^^^^^

* Fixed another issue in the ``configure()`` API.

0.2.1 (2011-08-22)
^^^^^^^^^^^^^^^^^^

* Fixed minor issue in ``configure()`` API.

0.2 (2011-08-22)
^^^^^^^^^^^^^^^^

* Added ``configure()`` API to ``AppConf`` class which is called after
  configuring each setting.

0.1 (2011-08-22)
^^^^^^^^^^^^^^^^

* First public release.
