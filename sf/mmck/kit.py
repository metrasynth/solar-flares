import json

import rv.api
from sf.error import SFValueError
from sf.lib.pymodule import forget, from_string, remember
from . import parameters, controllers
from .parameters import Parameters, ParameterValues


class Kit(object):

    def __init__(self):
        self.name = 'kit'
        self._py_source = None
        self._py_module = None
        self._project = None
        self.parameter_values = ParameterValues()

    @property
    def py_source(self):
        return self._py_source

    @py_source.setter
    def py_source(self, src):
        self._py_source = src
        _ = self.py_module
        self._project = None

    @property
    def py_module(self):
        if self._py_source is None:
            raise SFValueError('set py_source before getting py_module')
        if self._py_module is None:
            self._py_module = remember(from_string(
                name='_mmck_{}_{}'.format(self.name, id(self)),
                source=self.py_source,
            ))
        return self._py_module

    @py_module.setter
    def py_module(self, value):
        if value is None:
            if self._py_module is not None:
                forget(self._py_module)
                self._py_module = None
                self._project = None
        else:
            raise SFValueError('can only be set to None')

    @property
    def parameters(self):
        p = Parameters()
        self.py_module.set_parameters(p=p, P=parameters)
        for name, param in p.items():
            if name not in self.parameter_values:
                self.parameter_values[name] = param.default
        return p

    @property
    def controllers(self):
        self.project
        return self._controllers

    @property
    def project(self):
        if self._project is None:
            p = self.parameter_values.copy()
            c = controllers.Group()
            project = rv.api.Project()
            self.py_module.build_project(p=p, c=c, project=project)
            self._controllers = c
            self._project = project
        return self._project

    @project.deleter
    def project(self):
        self._project = None
