from sf.lib.orderedattrdict import OrderedAttrDict


p = None


class Parameters(OrderedAttrDict):
    pass


class ParameterValues(OrderedAttrDict):
    pass


class Parameter(object):

    def __init__(self, default=None, label=None):
        self.default = default
        self.label = label


class Integer(Parameter):

    def __init__(self, default=None, label=None, range=None, step=1):
        super(Integer, self).__init__(default, label)
        self.range = range
        self.step = step


class String(Parameter):

    def __init__(self, default=None, label=None, choices=None):
        super(String, self).__init__(default, label)
        self.choices = choices
