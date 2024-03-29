from random import randint

import rv.api

from sf.error import SFValueError
from sf.lib.pymodule import forget, from_string, remember
from . import parameters, controllers
from .parameters import Parameters, ParameterValues, ParameterClasses


class Kit(object):
    def __init__(self):
        self.name = "kit"
        self._controllers = None
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
        self.py_module = None
        _ = self.py_module
        self._project = None

    @property
    def py_module(self):
        if self._py_source is None:
            raise SFValueError("set py_source before getting py_module")
        if self._py_module is None:
            self._py_module = remember(
                from_string(
                    name="_mmck_{}_{}_{}".format(
                        self.name, id(self), randint(0, 2 ** 16)
                    ),
                    source=self.py_source,
                )
            )
        return self._py_module

    @py_module.setter
    def py_module(self, value):
        if value is not None:
            raise SFValueError("can only be set to None")
        if self._py_module is not None:
            forget(self._py_module)
            self._py_module = None
            self._project = None

    @property
    def parameters(self):
        p = Parameters()
        self.py_module.set_parameters(p=p, P=ParameterClasses)
        for name, param in p.items():
            if name not in self.parameter_values:
                self.parameter_values[name] = param.default
        return p

    @property
    def controllers(self):
        _ = self.project
        return self._controllers

    @property
    def watch_paths(self):
        if hasattr(self.py_module, "watch_paths"):
            return list(self.py_module.watch_paths(self.parameter_values))
        else:
            return []

    @property
    def project(self):
        if self._project is None:
            p = self.parameter_values.copy()
            c = controllers.Group()
            project = rv.api.Project()
            project = self.py_module.build_project(p=p, c=c, project=project)
            self._controllers = c
            self._project = project
        return self._project

    @project.deleter
    def project(self):
        self._project = None
