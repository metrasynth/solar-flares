from sf.lib.orderedattrdict import OrderedAttrDict


class Controller(object):

    def __init__(self, module, name):
        self.module = module
        self.name = name

    @property
    def ctl(self):
        c = self.module.controllers[self.name]
        if hasattr(self.module, 'user_defined') and c.number >= 6:
            c = self.module.user_defined[c.number - 6]
        return c

    @property
    def value(self):
        return getattr(self.module, self.name)

    @value.setter
    def value(self, value):
        setattr(self.module, self.name, value)

    @staticmethod
    def to_json(python_object):
        if isinstance(python_object, Controller):
            module = python_object.module
            name = python_object.name
            return dict(
                module=module.index,
                controller=module.controllers[name].number,
            )
        raise TypeError(repr(python_object) + ' is not JSON serializable')


class Group(OrderedAttrDict):

    def __init__(self, **kwds):
        super().__init__(default=Group, **kwds)

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

    def all_items(self):
        for key, value in self.items():
            if isinstance(value, Group):
                yield (key, list(value.all_items()))
            else:
                yield (key, value)


__all__ = [
    'Controller',
    'Group',
]
