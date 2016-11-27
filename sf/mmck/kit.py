import json

import rv.api
from sf.lib.pymodule import forget, from_string, remember
from . import parameters, project
from .parameters import Parameters, ParameterValues


class Kit(object):

    def __init__(self):
        self._parameter_factory_source = ''
        self._parameter_module = None
        self._project_factory_source = ''
        self._project_module = None
        self.parameter_values = ParameterValues()
        self.parameter_values_dirty = False

    @property
    def parameters(self):
        return self.parameter_module.p

    @property
    def parameter_factory_source(self):
        return self._parameter_factory_source

    @parameter_factory_source.setter
    def parameter_factory_source(self, value):
        self._parameter_factory_source = value
        self.parameter_module = None
        self.project_module = None

    @property
    def parameter_factory_source_clean(self):
        return self._parameter_module is not None

    @property
    def parameter_module(self):
        if self._parameter_module is None:
            parameters.p = Parameters()
            try:
                self._parameter_module = remember(from_string(
                    name='_kit_{}.parameter'.format(id(self)),
                    source=self._parameter_factory_source,
                ))
                for name, param in self._parameter_module.p.items():
                    if name not in self.parameter_values:
                        self.parameter_values[name] = param.default
            finally:
                parameters.p = None
        return self._parameter_module

    @parameter_module.setter
    def parameter_module(self, value):
        if value is None:
            forget(self._parameter_module)
            self._parameter_module = None
        else:
            raise ValueError('can only set to None')

    @property
    def project(self):
        return self.project_module.project

    @property
    def project_factory_source(self):
        return self._project_factory_source

    @project_factory_source.setter
    def project_factory_source(self, value):
        self._project_factory_source = value
        self.project_module = None

    @property
    def project_factory_source_clean(self):
        return (
            self._project_module is not None
            and not self.parameter_values_dirty
        )

    @property
    def project_module(self):
        if not self.project_factory_source_clean:
            project.c = project.Group()
            project.p = self.parameter_values.copy()
            project.project = rv.api.Project()
            try:
                forget(self._project_module)
                self._project_module = remember(from_string(
                    name='_kit_{}.project'.format(id(self)),
                    source=self._project_factory_source,
                ))
            finally:
                project.c = None
                project.p = None
                project.project = None
        return self._project_module

    @project_module.setter
    def project_module(self, value):
        if value is None:
            forget(self._project_module)
            self._project_module = None
        else:
            raise ValueError('can only set to None')

    def to_json(self):
        return json.dumps({
            'mmck_version': 1,
            'parameter_factory_source': self.parameter_factory_source,
            'parameter_values': list(self.parameter_values.items()),
            'project_factory_source': self.project_factory_source,
        }, indent=2)

    def load_json(self, src):
        data = json.loads(src)
        if data['mmck_version'] == 1:
            self.parameter_factory_source = data['parameter_factory_source']
            self.parameter_values.update(data['parameter_values'])
            self.project_factory_source = data['project_factory_source']
