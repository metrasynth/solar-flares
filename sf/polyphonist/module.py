from enum import Enum

from rv import m, read_sunvox_file, Project, Synth


class ModulePolyphonist(object):

    def __init__(self, module):
        if isinstance(module, str):
            module = read_sunvox_file(module).module
        elif isinstance(module, Synth):
            module = module.module
        elif not isinstance(module, m.Module):
            raise ValueError(
                'Must provide a path, Synth instance, or Module instance')
        self.module = module

    def polyphonized_module(self, voices):
        p = Project()
        poly = m.MetaModule(
            project=p,
            name='{} ({}x)'.format(self.module.name, voices),
        )
        orig = self.module
        clones = []
        for i in range(voices):
            clone = p.attach_module(orig.clone())
            clone.x = p.output.x - 512
            clone.y = p.output.y + i * 256
            clones.append(clone)
        p.output << clones
        mappings = poly.mappings.values
        if isinstance(orig, m.MetaModule):
            p.initial_bpm = orig.bpm
            p.initial_tpl = orig.tpl
            poly.bpm = orig.bpm
            poly.tpl = orig.tpl
            poly.user_defined_controllers = orig.user_defined_controllers
            for ctl_num, orig_ctl, poly_ctl in zip(
                    range(orig.user_defined_controllers),  # acts as a limiter
                    orig.user_defined,
                    poly.user_defined,
            ):
                poly_ctl.label = orig_ctl.label
                poly_ctl.detached = orig_ctl.detached
                ctl_name = 'user_defined_{}'.format(ctl_num + 1)
                ctl_value = getattr(orig, ctl_name)
                multi_ctl = p.new_module(m.MultiCtl, value=ctl_value)
                multi_ctl >> clones
                multi_ctl.x = p.output.x - 1024
                multi_ctl.y = p.output.y + ctl_num * 256
                for i, clone in enumerate(clones):
                    multi_ctl.mappings.values[i].controller = ctl_num + 5
                # mappings[ctl_num].module = multi_ctl.index + 1
                mappings[ctl_num].module = multi_ctl.index
                mappings[ctl_num].controller = 1
                setattr(poly, ctl_name, ctl_value)
        else:
            poly.user_defined_controllers = len(orig.controller_values)
            for ctl_num, (user_ctl, (ctl_name, ctl_value)) in enumerate(zip(
                poly.user_defined,
                orig.controller_values.items(),
            )):
                user_ctl_name = 'user_defined_{}'.format(ctl_num + 1)
                user_ctl.label = ctl_name
                ctl_value = ctl_value.value if isinstance(ctl_value, Enum) else ctl_value
                multi_ctl = p.new_module(m.MultiCtl, value=ctl_value)
                multi_ctl >> clones
                multi_ctl.x = p.output.x - 1024
                multi_ctl.y = p.output.y + ctl_num * 256
                for i, clone in enumerate(clones):
                    multi_ctl.mappings.values[i].controller = ctl_num + 1
                mappings[ctl_num].module = multi_ctl.index
                mappings[ctl_num].controller = 1
                poly.controller_values[user_ctl_name] = ctl_value
        return poly

    def polyphonized_synth(self, voices):
        poly = self.polyphonized_module(voices)
        return Synth(poly)
