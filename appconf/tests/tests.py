from __future__ import absolute_import
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from appconf.tests.models import (AppConf, TestConf, PrefixConf,
                                  YetAnotherPrefixConf, SeparateConf, ProxyConf,
                                  CustomHolderConf, custom_holder)


class TestConfTests(TestCase):

    def test_basic(self):
        self.assertEquals(TestConf._meta.prefix, 'tests')

    def test_simple(self):
        self.assertTrue(hasattr(settings, 'TESTS_SIMPLE_VALUE'))
        self.assertEquals(settings.TESTS_SIMPLE_VALUE, True)

    def test_configured(self):
        self.assertTrue(hasattr(settings, 'TESTS_CONFIGURED_VALUE'))
        self.assertEquals(settings.TESTS_CONFIGURED_VALUE, 'correct')

    def test_configure_method(self):
        self.assertTrue(hasattr(settings, 'TESTS_CONFIGURE_METHOD_VALUE'))
        self.assertEquals(settings.TESTS_CONFIGURE_METHOD_VALUE, True)

    def test_init_kwargs(self):
        custom_conf = TestConf(CUSTOM_VALUE='custom')
        self.assertEquals(custom_conf.CUSTOM_VALUE, 'custom')
        self.assertEquals(settings.TESTS_CUSTOM_VALUE, 'custom')
        self.assertRaises(AttributeError, lambda: custom_conf.TESTS_CUSTOM_VALUE)
        custom_conf.CUSTOM_VALUE_SETATTR = 'custom'
        self.assertEquals(settings.TESTS_CUSTOM_VALUE_SETATTR, 'custom')
        custom_conf.custom_value_lowercase = 'custom'
        self.assertRaises(AttributeError, lambda: settings.custom_value_lowercase)

    def test_init_kwargs_with_prefix(self):
        custom_conf = TestConf(TESTS_CUSTOM_VALUE2='custom2')
        self.assertEquals(custom_conf.TESTS_CUSTOM_VALUE2, 'custom2')
        self.assertEquals(settings.TESTS_CUSTOM_VALUE2, 'custom2')

    def test_proxy(self):
        custom_conf = ProxyConf(CUSTOM_VALUE3='custom3')
        self.assertEquals(custom_conf.CUSTOM_VALUE3, 'custom3')
        self.assertEquals(settings.TESTS_CUSTOM_VALUE3, 'custom3')
        self.assertEquals(custom_conf.TESTS_CUSTOM_VALUE3, 'custom3')
        self.assertTrue('appconf.tests' in custom_conf.INSTALLED_APPS)

    def test_dir_members(self):
        custom_conf = TestConf()
        self.assertTrue('TESTS_SIMPLE_VALUE' in dir(settings))
        if hasattr(settings, '__members__'):  # django 1.5 removed __members__
            self.assertTrue('TESTS_SIMPLE_VALUE' in settings.__members__)
        self.assertTrue('SIMPLE_VALUE' in dir(custom_conf))
        self.assertTrue('SIMPLE_VALUE' in custom_conf.__members__)
        self.assertFalse('TESTS_SIMPLE_VALUE' in dir(custom_conf))
        self.assertFalse('TESTS_SIMPLE_VALUE' in custom_conf.__members__)

    def test_custom_holder(self):
        CustomHolderConf()
        self.assertTrue(hasattr(custom_holder, 'CUSTOM_HOLDER_SIMPLE_VALUE'))
        self.assertEquals(custom_holder.CUSTOM_HOLDER_SIMPLE_VALUE, True)

    def test_subclass_configured_data(self):
        self.assertTrue('TESTS_CONFIGURE_METHOD_VALUE2' in dir(settings))
        self.assertEquals(settings.TESTS_CONFIGURE_METHOD_VALUE2, False)


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


class RequiredSettingsTests(TestCase):

    def create_invalid_conf(self):
        class RequirementConf(AppConf):
            class Meta:
                required = ['NOT_PRESENT']

    def test_value_is_defined(self):
        class RequirementConf(AppConf):
            class Meta:
                holder = 'appconf.tests.models.custom_holder'
                prefix = 'holder'
                required = ['VALUE']

    def test_default_is_defined(self):
        class RequirementConf(AppConf):
            SIMPLE_VALUE = True

            class Meta:
                required = ['SIMPLE_VALUE']

    def test_missing(self):
        self.assertRaises(ImproperlyConfigured, self.create_invalid_conf)
