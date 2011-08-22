import sys

# following PEP 386, versiontools will pick it up
__version__ = (0, 1, 0, "final", 0)


class AppConfOptions(object):

    def __init__(self, meta, *args, **kwargs):
        self.configured = False

    def prefixed_name(self, name):
        if name.startswith(self.app_label):
            return name
        return "%s_%s" % (self.app_label.upper(), name.upper())


class AppConfMetaClass(type):
    options_class = AppConfOptions

    def __new__(cls, name, bases, attrs):
        super_new = super(AppConfMetaClass, cls).__new__
        parents = [b for b in bases if isinstance(b, AppConfMetaClass)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        try:
            meta = attrs.pop('Meta')
        except KeyError:
            meta = None

        attrs['_meta'] = cls.options_class(meta)
        new_class = super_new(cls, name, bases, attrs)

        if getattr(new_class._meta, 'app_label', None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            model_module = sys.modules[new_class.__module__]
            new_class._meta.app_label = model_module.__name__.split('.')[-2]

        names = []
        defaults = []
        for name in filter(lambda name: name == name.upper(), attrs):
            prefixed_name = new_class._meta.prefixed_name(name)
            names.append((name, prefixed_name))
            defaults.append((prefixed_name, attrs.pop(name)))

        new_class.defaults = dict(defaults)
        new_class.names = dict(names)
        new_class._configure()

    def _configure(cls):
        if not cls._meta.configured:
            # the ad-hoc settings class instance used to configure each value
            obj = cls()
            from django.conf import settings
            for name, prefixed_name in obj.names.items():
                default_value = obj.defaults.get(prefixed_name)
                value = getattr(settings, prefixed_name, default_value)
                callback = getattr(obj, "configure_%s" % name.lower(), None)
                if callable(callback):
                    value = callback(value)
                # Finally, set the setting in the global setting object
                setattr(settings, prefixed_name, value)
            cls._meta.configured = True


class AppConf(object):
    """
    An app setting object to be used for handling app setting defaults
    gracefully and providing a nice API for them.
    """
    __metaclass__ = AppConfMetaClass

    def __init__(self, holder=None, **kwargs):
        for name, value in kwargs.iteritems():
            setattr(self, self._meta.prefixed_name(name), value)
        if holder is None:
            from django.conf import settings as holder
        self.__dict__['_holder'] = holder

    def __dir__(self):
        return sorted(list(set(dir(self.__dict__['_holder']))))

    def __members__(self):
        return self.__dir__()

    def __getattr__(self, name):
        return getattr(self.__dict__['_holder'], name)

    def __setattr__(self, name, value):
        setattr(self.__dict__['_holder'], name, value)
