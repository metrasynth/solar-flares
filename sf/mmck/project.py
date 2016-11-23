from sf.lib.orderedattrdict import OrderedAttrDict


c = None
p = None
project = None


class Controller(object):

    def __init__(self, module, name):
        self.module = module
        self.name = name

    @property
    def ctl(self):
        return self.module.controllers[self.name]

    @property
    def value(self):
        return getattr(self.module, self.name)

    @value.setter
    def value(self, value):
        setattr(self.module, self.name, value)


class Group(OrderedAttrDict):

    def __setitem__(self, key, value, **kwargs):
        if isinstance(value, tuple) and len(value) == 2:
            module, name = value
            value = Controller(module, name)
        elif not isinstance(value, (Controller, Group)):
            raise ValueError(
                'Value must be a 2-tuple, Controller instance, '
                'or Group instance'
            )
        super().__setitem__(key, value, **kwargs)


__all__ = [
    'Controller',
    'Group',
    'c',
    'p',
    'project',
]