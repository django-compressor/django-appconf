from django.conf import settings
from django.test import TestCase

from testapp.models import (TestConf, PrefixConf, YetAnotherPrefixConf,
                            SeparateConf, ProxyConf, CustomHolderConf,
                            custom_holder)


class TestConfTests(TestCase):

    def test_basic(self):
        self.assertEquals(TestConf._meta.prefix, 'testapp')

    def test_simple(self):
        self.assertTrue(hasattr(settings, 'TESTAPP_SIMPLE_VALUE'))
        self.assertEquals(settings.TESTAPP_SIMPLE_VALUE, True)

    def test_configured(self):
        self.assertTrue(hasattr(settings, 'TESTAPP_CONFIGURED_VALUE'))
        self.assertEquals(settings.TESTAPP_CONFIGURED_VALUE, 'correct')

    def test_configure_method(self):
        self.assertTrue(hasattr(settings, 'TESTAPP_CONFIGURE_METHOD_VALUE'))
        self.assertEquals(settings.TESTAPP_CONFIGURE_METHOD_VALUE, True)

    def test_init_kwargs(self):
        custom_conf = TestConf(CUSTOM_VALUE='custom')
        self.assertEquals(custom_conf.CUSTOM_VALUE, 'custom')
        self.assertEquals(settings.TESTAPP_CUSTOM_VALUE, 'custom')
        self.assertRaises(AttributeError, lambda: custom_conf.TESTAPP_CUSTOM_VALUE)

    def test_init_kwargs_with_prefix(self):
        custom_conf = TestConf(TESTAPP_CUSTOM_VALUE2='custom2')
        self.assertEquals(custom_conf.TESTAPP_CUSTOM_VALUE2, 'custom2')
        self.assertEquals(settings.TESTAPP_CUSTOM_VALUE2, 'custom2')

    def test_proxy(self):
        custom_conf = ProxyConf(CUSTOM_VALUE3='custom3')
        self.assertEquals(custom_conf.CUSTOM_VALUE3, 'custom3')
        self.assertEquals(settings.TESTAPP_CUSTOM_VALUE3, 'custom3')
        self.assertEquals(custom_conf.TESTAPP_CUSTOM_VALUE3, 'custom3')
        self.assertTrue('tests.testapp' in custom_conf.INSTALLED_APPS)

    def test_dir_members(self):
        custom_conf = TestConf()
        self.assertTrue('TESTAPP_SIMPLE_VALUE' in dir(settings))
        self.assertTrue('TESTAPP_SIMPLE_VALUE' in settings.__members__)
        self.assertTrue('SIMPLE_VALUE' in dir(custom_conf))
        self.assertTrue('SIMPLE_VALUE' in custom_conf.__members__)
        self.assertFalse('TESTAPP_SIMPLE_VALUE' in dir(custom_conf))
        self.assertFalse('TESTAPP_SIMPLE_VALUE' in custom_conf.__members__)

    def test_custom_holder(self):
        custom_conf = CustomHolderConf()
        self.assertTrue(hasattr(custom_holder, 'CUSTOM_HOLDER_SIMPLE_VALUE'))
        self.assertEquals(custom_holder.CUSTOM_HOLDER_SIMPLE_VALUE, True)


class PrefixConfTests(TestCase):

    def test_prefix(self):
        self.assertEquals(PrefixConf._meta.prefix, 'prefix')

    def test_simple(self):
        self.assertTrue(hasattr(settings, 'PREFIX_SIMPLE_VALUE'))
        self.assertEquals(settings.PREFIX_SIMPLE_VALUE, True)

    def test_configured(self):
        self.assertTrue(hasattr(settings, 'PREFIX_CONFIGURED_VALUE'))
        self.assertEquals(settings.PREFIX_CONFIGURED_VALUE, 'correct')

    def test_configure_method(self):
        self.assertTrue(hasattr(settings, 'PREFIX_CONFIGURE_METHOD_VALUE'))
        self.assertEquals(settings.PREFIX_CONFIGURE_METHOD_VALUE, True)


class YetAnotherPrefixConfTests(TestCase):

    def test_prefix(self):
        self.assertEquals(YetAnotherPrefixConf._meta.prefix,
                          'yetanother_prefix')

    def test_simple(self):
        self.assertTrue(hasattr(settings,
                                'YETANOTHER_PREFIX_SIMPLE_VALUE'))
        self.assertEquals(settings.YETANOTHER_PREFIX_SIMPLE_VALUE, False)

    def test_configured(self):
        self.assertTrue(hasattr(settings,
                                'YETANOTHER_PREFIX_CONFIGURED_VALUE'))
        self.assertEquals(settings.YETANOTHER_PREFIX_CONFIGURED_VALUE,
                          'correct')

    def test_configure_method(self):
        self.assertTrue(hasattr(settings,
                                'YETANOTHER_PREFIX_CONFIGURE_METHOD_VALUE'))
        self.assertEquals(settings.YETANOTHER_PREFIX_CONFIGURE_METHOD_VALUE,
                          True)


class SeparateConfTests(TestCase):

    def test_prefix(self):
        self.assertEquals(SeparateConf._meta.prefix, 'prefix')

    def test_simple(self):
        self.assertTrue(hasattr(settings, 'PREFIX_SEPARATE_VALUE'))
        self.assertEquals(settings.PREFIX_SEPARATE_VALUE, True)
