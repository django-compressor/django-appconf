django-appconf
==============

A helper class for handling configuration defaults of packaged Django
apps gracefully.

Overview
--------

Say you have an app called ``myapp`` with a few defaults, which you want
to refer to in the app's code without repeating yourself all the time.
``appconf`` provides a simple class to implement those defaults. Simply add
something like the following code somewhere in your app files::

    from appconf import AppConf

    class MyAppConf(AppConf):
        SETTING_1 = "one"
        SETTING_2 = (
            "two",
        )

.. note::

    ``AppConf`` classes depend on being imported during startup of the Django
    process. Even though there are multiple modules loaded automatically,
    only the ``models`` modules (usually the ``models.py`` file of your
    app) are guaranteed to be loaded at startup. Therefore it's recommended
    to put your ``AppConf`` subclass(es) there, too.

The settings are initialized with the capitalized app label of where the
setting is located at. E.g. if your ``models.py`` with the ``AppConf`` class
is in the ``myapp`` package, the prefix of the settings will be ``MYAPP``.

You can override the default prefix by specifying a ``prefix`` attribute of
an inner ``Meta`` class::

    from appconf import AppConf

    class AcmeAppConf(AppConf):
        SETTING_1 = "one"
        SETTING_2 = (
            "two",
        )

        class Meta:
            prefix = 'acme'

The ``MyAppConf`` class will automatically look at Django's global settings
to determine if you've overridden it. For example, adding this to your site's
``settings.py`` would override ``SETTING_1`` of the above ``MyAppConf``::

    ACME_SETTING_1 = "uno"

In case you want to use a different settings object instead of the default
``'django.conf.settings'``, set the ``holder`` attribute of the inner
``Meta`` class to a dotted import path::

    from appconf import AppConf

    class MyAppConf(AppConf):
        SETTING_1 = "one"
        SETTING_2 = (
            "two",
        )

        class Meta:
            prefix = 'acme'
            holder = 'acme.conf.settings'
