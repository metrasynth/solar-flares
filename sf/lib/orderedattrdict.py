class OrderedAttrDict(dict):
    def __init__(self, default=None, **kwds):
        self.__dict__["_default"] = default
        super().__init__(**kwds)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError()

    def __getitem__(self, item):
        d = self
        parts = item.split(".")
        for name in parts:
            if not super(OrderedAttrDict, d).__contains__(name) and callable(
                self._default
            ):
                v = self._default()
                super(OrderedAttrDict, d).__setitem__(name, v)
            d = super(OrderedAttrDict, d).__getitem__(name)
        return d

    def __contains__(self, item):
        d = self
        parts = item.split(".")
        for name in parts[:-1]:
            if not super(OrderedAttrDict, d).__contains__(name):
                return False
            d = super(OrderedAttrDict, d).__getitem__(name)
        name = parts[-1]
        return super(OrderedAttrDict, d).__contains__(name)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except KeyError:
            raise AttributeError()

    def copy(self):
        return OrderedAttrDict(**self)
