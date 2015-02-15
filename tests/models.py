from appconf import AppConf


class CustomHolder(object):
    HOLDER_VALUE = True

custom_holder = CustomHolder()


class TestConf(AppConf):

    SIMPLE_VALUE = True

    CONFIGURED_VALUE = 'wrong'

    def configure_configured_value(self, value):
        return 'correct'

    def configure(self):
        self.configured_data['CONFIGURE_METHOD_VALUE'] = True
        return self.configured_data


class PrefixConf(TestConf):

    class Meta:
        prefix = 'prefix'


class YetAnotherPrefixConf(PrefixConf):

    SIMPLE_VALUE = False

    class Meta:
        prefix = 'yetanother_prefix'


class SeparateConf(AppConf):

    SEPARATE_VALUE = True

    class Meta(PrefixConf.Meta):
        pass


class SubclassConf(TestConf):

    def configure(self):
        self.configured_data['CONFIGURE_METHOD_VALUE2'] = False
        return self.configured_data


class ProxyConf(TestConf):

    class Meta:
        proxy = True


class CustomHolderConf(AppConf):

    SIMPLE_VALUE = True

    class Meta:
        # instead of django.conf.settings
        holder = 'tests.models.custom_holder'
        prefix = 'custom_holder'
