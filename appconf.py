import sys

# following PEP 386, versiontools will pick it up
__version__ = (0, 2, 2, "final", 0)


class AppConfOptions(object):

    def __init__(self, meta, app_label=None):
        self.app_label = app_label

    def prefixed_name(self, name):
        if name.startswith(self.app_label.upper()):
            return name
        return "%s_%s" % (self.app_label.upper(), name.upper())

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.names = {}
        self.defaults = {}


class AppConfMetaClass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(AppConfMetaClass, cls).__new__
        parents = [b for b in bases if isinstance(b, AppConfMetaClass)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        if attr_meta:
            meta = attr_meta
        else:
            attr_meta = type('Meta', (object,), {})
            meta = getattr(new_class, 'Meta', None)

        app_label = getattr(meta, 'app_label', None)
        if app_label is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            model_module = sys.modules[new_class.__module__]
            app_label = model_module.__name__.split('.')[-2]

        new_class.add_to_class('_meta', AppConfOptions(meta, app_label))
        new_class.add_to_class('Meta', attr_meta)

        for parent in parents[::-1]:
            if hasattr(parent, '_meta'):
                new_class._meta.names.update(parent._meta.names)
                new_class._meta.defaults.update(parent._meta.defaults)

        for name in filter(lambda name: name == name.upper(), attrs):
            prefixed_name = new_class._meta.prefixed_name(name)
            new_class._meta.names[name] = prefixed_name
            new_class._meta.defaults[prefixed_name] = attrs.pop(name)

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        return new_class._configure()

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def _configure(cls):
        from django.conf import settings
        # the ad-hoc settings class instance used to configure each value
        obj = cls()
        obj.configured_data = dict()
        for name, prefixed_name in obj._meta.names.iteritems():
            default_value = obj._meta.defaults.get(prefixed_name)
            value = getattr(settings, prefixed_name, default_value)
            callback = getattr(obj, "configure_%s" % name.lower(), None)
            if callable(callback):
                value = callback(value)
            obj.configured_data[name] = value
        obj.configured_data = obj.configure()

        # Finally, set the setting in the global setting object
        for name, value in obj.configured_data.iteritems():
            prefixed_name = obj._meta.prefixed_name(name)
            setattr(settings, prefixed_name, value)

        return cls


class AppConf(object):
    """
    An app setting object to be used for handling app setting defaults
    gracefully and providing a nice API for them.
    """
    __metaclass__ = AppConfMetaClass

    def __init__(self, **kwargs):
        from django.conf import settings
        self._holder = settings
        for name, value in kwargs.iteritems():
            setattr(self, self._meta.prefixed_name(name), value)

    def __dir__(self):
        return sorted(list(set(dir(self._holder))))

    # For Python < 2.6:
    @property
    def __members__(self):
        return self.__dir__()

    def __getattr__(self, name):
        return getattr(self._holder, name)

    def __setattr__(self, name, value):
        if name == name.upper():
            return setattr(self._holder, name, value)
        object.__setattr__(self, name, value)

    def configure(self):
        """
        Hook for doing any extra configuration.
        """
        return self.configured_data
