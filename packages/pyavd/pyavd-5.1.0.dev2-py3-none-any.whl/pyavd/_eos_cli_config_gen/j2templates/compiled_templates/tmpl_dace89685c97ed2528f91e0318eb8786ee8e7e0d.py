from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/port-channel-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['arista.avd.range_expand']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.range_expand' found.")
    try:
        t_5 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_6 = environment.filters['replace']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'replace' found.")
    try:
        t_7 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
        l_1_encapsulation_dot1q_cli = resolve('encapsulation_dot1q_cli')
        l_1_encapsulation_cli = resolve('encapsulation_cli')
        l_1_client_encapsulation = resolve('client_encapsulation')
        l_1_network_flag = resolve('network_flag')
        l_1_network_encapsulation = resolve('network_encapsulation')
        l_1_dfe_algo_cli = resolve('dfe_algo_cli')
        l_1_dfe_hold_time_cli = resolve('dfe_hold_time_cli')
        l_1_host_proxy_cli = resolve('host_proxy_cli')
        l_1_interface_ip_nat = resolve('interface_ip_nat')
        l_1_hide_passwords = resolve('hide_passwords')
        l_1_sorted_vlans_cli = resolve('sorted_vlans_cli')
        l_1_backup_link_cli = resolve('backup_link_cli')
        _loop_vars = {}
        pass
        yield '!\ninterface '
        yield str(environment.getattr(l_1_port_channel_interface, 'name'))
        yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'profile')):
            pass
            yield '   profile '
            yield str(environment.getattr(l_1_port_channel_interface, 'profile'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'input')):
            pass
            yield '   traffic-policy input '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'input'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'output')):
            pass
            yield '   traffic-policy output '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'traffic_policy'), 'output'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'description')):
            pass
            yield '   description '
            yield str(environment.getattr(l_1_port_channel_interface, 'description'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'shutdown'), True):
            pass
            yield '   shutdown\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'mtu')):
            pass
            yield '   mtu '
            yield str(environment.getattr(l_1_port_channel_interface, 'mtu'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'logging'), 'event'), 'link_status'), True):
            pass
            yield '   logging event link-status\n'
        elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'logging'), 'event'), 'link_status'), False):
            pass
            yield '   no logging event link-status\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bgp'), 'session_tracker')):
            pass
            yield '   bgp session tracker '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bgp'), 'session_tracker'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'l2_protocol'), 'forwarding_profile')):
            pass
            yield '   l2-protocol forwarding profile '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'l2_protocol'), 'forwarding_profile'))
            yield '\n'
        if ((t_7(environment.getattr(l_1_port_channel_interface, 'vlans')) and t_7(environment.getattr(l_1_port_channel_interface, 'mode'))) and (environment.getattr(l_1_port_channel_interface, 'mode') in ['access', 'dot1q-tunnel'])):
            pass
            yield '   switchport access vlan '
            yield str(environment.getattr(l_1_port_channel_interface, 'vlans'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan')):
            pass
            yield '   switchport access vlan '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan'))
            yield '\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'mode')) and (environment.getattr(l_1_port_channel_interface, 'mode') in ['trunk', 'trunk phone'])):
            pass
            if t_7(environment.getattr(l_1_port_channel_interface, 'native_vlan_tag'), True):
                pass
                yield '   switchport trunk native vlan tag\n'
            elif t_7(environment.getattr(l_1_port_channel_interface, 'native_vlan')):
                pass
                yield '   switchport trunk native vlan '
                yield str(environment.getattr(l_1_port_channel_interface, 'native_vlan'))
                yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True):
            pass
            yield '   switchport trunk native vlan tag\n'
        elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan')):
            pass
            yield '   switchport trunk native vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'phone'), 'vlan')):
            pass
            yield '   switchport phone vlan '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'phone'), 'vlan'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'phone'), 'vlan')):
            pass
            yield '   switchport phone vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'phone'), 'vlan'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'phone'), 'trunk')):
            pass
            yield '   switchport phone trunk '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'phone'), 'trunk'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'phone'), 'trunk')):
            pass
            yield '   switchport phone trunk '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'phone'), 'trunk'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'in_required'), True):
            pass
            yield '   switchport vlan translation in required\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'out_required'), True):
            pass
            yield '   switchport vlan translation out required\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'dot1q'), 'vlan_tag')):
            pass
            yield '   switchport dot1q vlan tag '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'dot1q'), 'vlan_tag'))
            yield '\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'vlans')) and t_7(environment.getattr(l_1_port_channel_interface, 'mode'), 'trunk')):
            pass
            yield '   switchport trunk allowed vlan '
            yield str(environment.getattr(l_1_port_channel_interface, 'vlans'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan')):
            pass
            yield '   switchport trunk allowed vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan'))
            yield '\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'mode')) and (environment.getattr(l_1_port_channel_interface, 'mode') != 'access')):
            pass
            yield '   switchport mode '
            yield str(environment.getattr(l_1_port_channel_interface, 'mode'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'mode')):
            pass
            yield '   switchport mode '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'mode'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'dot1q'), 'ethertype')):
            pass
            yield '   switchport dot1q ethertype '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'dot1q'), 'ethertype'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_forwarding_accept_all'), True):
            pass
            yield '   switchport vlan forwarding accept all\n'
        for l_2_trunk_group in t_3(environment.getattr(l_1_port_channel_interface, 'trunk_groups')):
            _loop_vars = {}
            pass
            yield '   switchport trunk group '
            yield str(l_2_trunk_group)
            yield '\n'
        l_2_trunk_group = missing
        for l_2_trunk_group in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'groups')):
            _loop_vars = {}
            pass
            yield '   switchport trunk group '
            yield str(l_2_trunk_group)
            yield '\n'
        l_2_trunk_group = missing
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'enabled'), True):
            pass
            yield '   switchport\n'
        elif t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'enabled'), False):
            pass
            yield '   no switchport\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'type'), 'switched'):
            pass
            yield '   switchport\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'type'), 'routed'):
            pass
            yield '   no switchport\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q'), 'vlan')):
            pass
            l_1_encapsulation_dot1q_cli = str_join(('encapsulation dot1q vlan ', environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q'), 'vlan'), ))
            _loop_vars['encapsulation_dot1q_cli'] = l_1_encapsulation_dot1q_cli
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q'), 'inner_vlan')):
                pass
                l_1_encapsulation_dot1q_cli = str_join(((undefined(name='encapsulation_dot1q_cli') if l_1_encapsulation_dot1q_cli is missing else l_1_encapsulation_dot1q_cli), ' inner ', environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q'), 'inner_vlan'), ))
                _loop_vars['encapsulation_dot1q_cli'] = l_1_encapsulation_dot1q_cli
            yield '   '
            yield str((undefined(name='encapsulation_dot1q_cli') if l_1_encapsulation_dot1q_cli is missing else l_1_encapsulation_dot1q_cli))
            yield '\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'vlan_id')) and (t_1(environment.getattr(l_1_port_channel_interface, 'type')) != 'l2dot1q')):
            pass
            yield '   vlan id '
            yield str(environment.getattr(l_1_port_channel_interface, 'vlan_id'))
            yield '\n'
        if (t_1(environment.getattr(l_1_port_channel_interface, 'type')) in ['l3dot1q', 'l2dot1q']):
            pass
            if t_7(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan')):
                pass
                yield '   encapsulation dot1q vlan '
                yield str(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan'))
                yield '\n'
            if (t_7(environment.getattr(l_1_port_channel_interface, 'vlan_id')) and (environment.getattr(l_1_port_channel_interface, 'type') == 'l2dot1q')):
                pass
                yield '   vlan id '
                yield str(environment.getattr(l_1_port_channel_interface, 'vlan_id'))
                yield '\n'
            if (t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan')) and (not t_7(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan')))):
                pass
                l_1_encapsulation_cli = str_join(('client dot1q ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan')):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network dot1q ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'client'), True):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif (t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner')) and t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'))):
                pass
                l_1_encapsulation_cli = str_join(('client dot1q outer ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'), ' inner ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                if (t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner')) and t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'))):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network dot1q outer ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'), ' inner ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'client'), True):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'unmatched'), True):
                pass
                l_1_encapsulation_cli = 'client unmatched'
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            if t_7((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli)):
                pass
                yield '   !\n   encapsulation vlan\n      '
                yield str((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli))
                yield '\n'
        if (t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'encapsulation')) and (not t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q'), 'vlan')))):
            pass
            l_1_client_encapsulation = environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'encapsulation')
            _loop_vars['client_encapsulation'] = l_1_client_encapsulation
            l_1_network_flag = False
            _loop_vars['network_flag'] = l_1_network_flag
            if ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['dot1q', 'dot1ad']):
                pass
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'vlan')):
                    pass
                    l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'vlan'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif (t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan')) and t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'))):
                    pass
                    if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'inner_encapsulation')):
                        pass
                        l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'inner_encapsulation'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    else:
                        pass
                        l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    if (t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'encapsulation')) == 'client inner'):
                        pass
                        l_1_network_flag = True
                        _loop_vars['network_flag'] = l_1_network_flag
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'encapsulation'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['untagged', 'unmatched']):
                pass
                l_1_encapsulation_cli = str_join(('client ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'encapsulation'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            if t_7((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli)):
                pass
                if ((((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['dot1q', 'dot1ad', 'untagged']) and t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'encapsulation'))) and (not (undefined(name='network_flag') if l_1_network_flag is missing else l_1_network_flag))):
                    pass
                    l_1_network_encapsulation = environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'encapsulation')
                    _loop_vars['network_encapsulation'] = l_1_network_encapsulation
                    if ((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) in ['dot1q', 'dot1ad']):
                        pass
                        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'vlan')):
                            pass
                            l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'vlan'), ))
                            _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                        elif (t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan')) and t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'))):
                            pass
                            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'inner_encapsulation')):
                                pass
                                l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'inner_encapsulation'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'), ))
                                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                            else:
                                pass
                                l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'), ))
                                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    elif (((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) == 'untagged') and ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) == 'untagged')):
                        pass
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network untagged', ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    elif (((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) == 'client') and ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) != 'untagged')):
                        pass
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                yield '   !\n   encapsulation vlan\n      '
                yield str((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli))
                yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'source_interface')):
            pass
            yield '   switchport source-interface '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'source_interface'))
            yield '\n'
        for l_2_vlan_translation in t_3(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
            l_2_vlan_translation_cli = resolve('vlan_translation_cli')
            _loop_vars = {}
            pass
            if (t_7(environment.getattr(l_2_vlan_translation, 'from')) and t_7(environment.getattr(l_2_vlan_translation, 'to'))):
                pass
                l_2_vlan_translation_cli = 'switchport vlan translation'
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                if (t_1(environment.getattr(l_2_vlan_translation, 'direction')) in ['in', 'out']):
                    pass
                    l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'direction'), ))
                    _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'from'), ))
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                yield '   '
                yield str((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli))
                yield '\n'
        l_2_vlan_translation = l_2_vlan_translation_cli = missing
        for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_both'), 'from'):
            l_2_vlan_translation_both_cli = missing
            _loop_vars = {}
            pass
            l_2_vlan_translation_both_cli = str_join(('switchport vlan translation ', environment.getattr(l_2_vlan_translation, 'from'), ))
            _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            if t_7(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), True):
                pass
                l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' dot1q-tunnel', ))
                _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            elif t_7(environment.getattr(l_2_vlan_translation, 'inner_vlan_from')):
                pass
                l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), ))
                _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
                if t_7(environment.getattr(l_2_vlan_translation, 'network'), True):
                    pass
                    l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' network', ))
                    _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
            _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            yield '   '
            yield str((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli))
            yield '\n'
        l_2_vlan_translation = l_2_vlan_translation_both_cli = missing
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_in')):
            pass
            for l_2_vlan_translation in environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_in'):
                l_2_vlan_translation_in_cli = missing
                _loop_vars = {}
                pass
                l_2_vlan_translation_in_cli = str_join(('switchport vlan translation in ', environment.getattr(l_2_vlan_translation, 'from'), ))
                _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                if t_7(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), True):
                    pass
                    l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' dot1q-tunnel', ))
                    _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                elif t_7(environment.getattr(l_2_vlan_translation, 'inner_vlan_from')):
                    pass
                    l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), ))
                    _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                yield '   '
                yield str((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli))
                yield '\n'
            l_2_vlan_translation = l_2_vlan_translation_in_cli = missing
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_out')):
            pass
            for l_2_vlan_translation in environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_out'):
                l_2_vlan_translation_out_cli = resolve('vlan_translation_out_cli')
                _loop_vars = {}
                pass
                if t_7(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')):
                    pass
                    l_2_vlan_translation_out_cli = str_join(('switchport vlan translation out ', environment.getattr(l_2_vlan_translation, 'from'), ' dot1q-tunnel ', environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to'), ))
                    _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                elif t_7(environment.getattr(l_2_vlan_translation, 'to')):
                    pass
                    l_2_vlan_translation_out_cli = str_join(('switchport vlan translation out ', environment.getattr(l_2_vlan_translation, 'from'), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                    _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                    if t_7(environment.getattr(l_2_vlan_translation, 'inner_vlan_to')):
                        pass
                        l_2_vlan_translation_out_cli = str_join(((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_to'), ))
                        _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                if t_7((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli)):
                    pass
                    yield '   '
                    yield str((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli))
                    yield '\n'
            l_2_vlan_translation = l_2_vlan_translation_out_cli = missing
        if t_7(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'), True):
            pass
            yield '   switchport trunk private-vlan secondary\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'), False):
            pass
            yield '   no switchport trunk private-vlan secondary\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'), True):
            pass
            yield '   switchport trunk private-vlan secondary\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping')):
            pass
            yield '   switchport pvlan mapping '
            yield str(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'pvlan_mapping')):
            pass
            yield '   switchport pvlan mapping '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'pvlan_mapping'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'l2_protocol'), 'encapsulation_dot1q_vlan')):
            pass
            yield '   l2-protocol encapsulation dot1q vlan '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'l2_protocol'), 'encapsulation_dot1q_vlan'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment')):
            pass
            yield '   !\n   evpn ethernet-segment\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'identifier')):
                pass
                yield '      identifier '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'identifier'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'redundancy')):
                pass
                yield '      redundancy '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'redundancy'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')):
                pass
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'algorithm'), 'modulus'):
                    pass
                    yield '      designated-forwarder election algorithm modulus\n'
                elif (t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'algorithm'), 'preference') and t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'preference_value'))):
                    pass
                    l_1_dfe_algo_cli = str_join(('designated-forwarder election algorithm preference ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'preference_value'), ))
                    _loop_vars['dfe_algo_cli'] = l_1_dfe_algo_cli
                    if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'dont_preempt'), True):
                        pass
                        l_1_dfe_algo_cli = str_join(((undefined(name='dfe_algo_cli') if l_1_dfe_algo_cli is missing else l_1_dfe_algo_cli), ' dont-preempt', ))
                        _loop_vars['dfe_algo_cli'] = l_1_dfe_algo_cli
                    yield '      '
                    yield str((undefined(name='dfe_algo_cli') if l_1_dfe_algo_cli is missing else l_1_dfe_algo_cli))
                    yield '\n'
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'hold_time')):
                    pass
                    l_1_dfe_hold_time_cli = str_join(('designated-forwarder election hold-time ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'hold_time'), ))
                    _loop_vars['dfe_hold_time_cli'] = l_1_dfe_hold_time_cli
                    if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'subsequent_hold_time')):
                        pass
                        l_1_dfe_hold_time_cli = str_join(((undefined(name='dfe_hold_time_cli') if l_1_dfe_hold_time_cli is missing else l_1_dfe_hold_time_cli), ' subsequent-hold-time ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'subsequent_hold_time'), ))
                        _loop_vars['dfe_hold_time_cli'] = l_1_dfe_hold_time_cli
                    yield '      '
                    yield str((undefined(name='dfe_hold_time_cli') if l_1_dfe_hold_time_cli is missing else l_1_dfe_hold_time_cli))
                    yield '\n'
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'candidate_reachability_required'), True):
                    pass
                    yield '      designated-forwarder election candidate reachability required\n'
                elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'candidate_reachability_required'), False):
                    pass
                    yield '      no designated-forwarder election candidate reachability required\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time')):
                pass
                yield '      mpls tunnel flood filter time '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index')):
                pass
                yield '      mpls shared index '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'route_target')):
                pass
                yield '      route-target import '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'route_target'))
                yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'flow_tracker'), 'hardware')):
            pass
            yield '   flow tracker hardware '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'flow_tracker'), 'hardware'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'flow_tracker'), 'sampled')):
            pass
            yield '   flow tracker sampled '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'flow_tracker'), 'sampled'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'snmp_trap_link_change'), False):
            pass
            yield '   no snmp trap link-change\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'snmp_trap_link_change'), True):
            pass
            yield '   snmp trap link-change\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'vrf')):
            pass
            yield '   vrf '
            yield str(environment.getattr(l_1_port_channel_interface, 'vrf'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ip_proxy_arp'), True):
            pass
            yield '   ip proxy-arp\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ip_address')):
            pass
            yield '   ip address '
            yield str(environment.getattr(l_1_port_channel_interface, 'ip_address'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ip_verify_unicast_source_reachable_via')):
            pass
            yield '   ip verify unicast source reachable-via '
            yield str(environment.getattr(l_1_port_channel_interface, 'ip_verify_unicast_source_reachable_via'))
            yield '\n'
        if ((t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'interval')) and t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'min_rx'))) and t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'multiplier'))):
            pass
            yield '   bfd interval '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'interval'))
            yield ' min-rx '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'min_rx'))
            yield ' multiplier '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'multiplier'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'echo'), True):
            pass
            yield '   bfd echo\n'
        elif t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'echo'), False):
            pass
            yield '   no bfd echo\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'neighbor')):
            pass
            yield '   bfd neighbor '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'neighbor'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'per_link'), 'enabled'), True):
            pass
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'bfd'), 'per_link'), 'rfc_7130'), True):
                pass
                yield '   bfd per-link rfc-7130\n'
            else:
                pass
                yield '   bfd per-link\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'enabled'), True):
            pass
            l_1_host_proxy_cli = 'ip igmp host-proxy'
            _loop_vars['host_proxy_cli'] = l_1_host_proxy_cli
            yield '   '
            yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
            yield '\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'groups')):
                pass
                for l_2_proxy_group in environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'groups'):
                    _loop_vars = {}
                    pass
                    if (t_7(environment.getattr(l_2_proxy_group, 'exclude')) or t_7(environment.getattr(l_2_proxy_group, 'include'))):
                        pass
                        if t_7(environment.getattr(l_2_proxy_group, 'include')):
                            pass
                            for l_3_include_source in environment.getattr(l_2_proxy_group, 'include'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' include '
                                yield str(environment.getattr(l_3_include_source, 'source'))
                                yield '\n'
                            l_3_include_source = missing
                        if t_7(environment.getattr(l_2_proxy_group, 'exclude')):
                            pass
                            for l_3_exclude_source in environment.getattr(l_2_proxy_group, 'exclude'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' exclude '
                                yield str(environment.getattr(l_3_exclude_source, 'source'))
                                yield '\n'
                            l_3_exclude_source = missing
                    elif t_7(environment.getattr(l_2_proxy_group, 'group')):
                        pass
                        yield '   '
                        yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                        yield ' '
                        yield str(environment.getattr(l_2_proxy_group, 'group'))
                        yield '\n'
                l_2_proxy_group = missing
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'access_lists')):
                pass
                for l_2_access_list in environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'access_lists'):
                    _loop_vars = {}
                    pass
                    yield '   '
                    yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                    yield ' access-list '
                    yield str(environment.getattr(l_2_access_list, 'name'))
                    yield '\n'
                l_2_access_list = missing
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'report_interval')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' report-interval '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'report_interval'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'version')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' version '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ip_igmp_host_proxy'), 'version'))
                yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_enable'), True):
            pass
            yield '   ipv6 enable\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_address')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_port_channel_interface, 'ipv6_address'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_address_link_local')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_port_channel_interface, 'ipv6_address_link_local'))
            yield ' link-local\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_ra_disabled'), True):
            pass
            yield '   ipv6 nd ra disabled\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_managed_config_flag'), True):
            pass
            yield '   ipv6 nd managed-config-flag\n'
        for l_2_ipv6_nd_prefix in t_3(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_prefixes'), 'ipv6_prefix'):
            l_2_ipv6_nd_prefix_cli = missing
            _loop_vars = {}
            pass
            l_2_ipv6_nd_prefix_cli = str_join(('ipv6 nd prefix ', environment.getattr(l_2_ipv6_nd_prefix, 'ipv6_prefix'), ))
            _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
            if t_7(environment.getattr(l_2_ipv6_nd_prefix, 'valid_lifetime')):
                pass
                l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_ipv6_nd_prefix, 'valid_lifetime'), ))
                _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
            if t_7(environment.getattr(l_2_ipv6_nd_prefix, 'preferred_lifetime')):
                pass
                l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_ipv6_nd_prefix, 'preferred_lifetime'), ))
                _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
            if t_7(environment.getattr(l_2_ipv6_nd_prefix, 'no_autoconfig_flag'), True):
                pass
                l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' no-autoconfig', ))
                _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
            yield '   '
            yield str((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli))
            yield '\n'
        l_2_ipv6_nd_prefix = l_2_ipv6_nd_prefix_cli = missing
        if t_7(environment.getattr(l_1_port_channel_interface, 'access_group_in')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'access_group_in'))
            yield ' in\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'access_group_out')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'access_group_out'))
            yield ' out\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_in')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_in'))
            yield ' in\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_out')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_out'))
            yield ' out\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'mac_access_group_in')):
            pass
            yield '   mac access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'mac_access_group_in'))
            yield ' in\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'mac_access_group_out')):
            pass
            yield '   mac access-group '
            yield str(environment.getattr(l_1_port_channel_interface, 'mac_access_group_out'))
            yield ' out\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_mode')):
            pass
            yield '   port-channel lacp fallback '
            yield str(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_mode'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_timeout')):
            pass
            yield '   port-channel lacp fallback timeout '
            yield str(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_timeout'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'l2_mtu')):
            pass
            yield '   l2 mtu '
            yield str(environment.getattr(l_1_port_channel_interface, 'l2_mtu'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'l2_mru')):
            pass
            yield '   l2 mru '
            yield str(environment.getattr(l_1_port_channel_interface, 'l2_mru'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'lacp_id')):
            pass
            yield '   lacp system-id '
            yield str(environment.getattr(l_1_port_channel_interface, 'lacp_id'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'mpls'), 'ldp'), 'igp_sync'), True):
            pass
            yield '   mpls ldp igp sync\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'mpls'), 'ldp'), 'interface'), True):
            pass
            yield '   mpls ldp interface\n'
        elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'mpls'), 'ldp'), 'interface'), False):
            pass
            yield '   no mpls ldp interface\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'mlag')):
            pass
            yield '   mlag '
            yield str(environment.getattr(l_1_port_channel_interface, 'mlag'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'mpls'), 'ip'), True):
            pass
            yield '   mpls ip\n'
        elif t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'mpls'), 'ip'), False):
            pass
            yield '   no mpls ip\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ip_nat')):
            pass
            l_1_interface_ip_nat = environment.getattr(l_1_port_channel_interface, 'ip_nat')
            _loop_vars['interface_ip_nat'] = l_1_interface_ip_nat
            template = environment.get_template('eos/interface-ip-nat.j2', 'eos/port-channel-interfaces.j2')
            for event in template.root_render_func(template.new_context(context.get_all(), True, {'backup_link_cli': l_1_backup_link_cli, 'client_encapsulation': l_1_client_encapsulation, 'dfe_algo_cli': l_1_dfe_algo_cli, 'dfe_hold_time_cli': l_1_dfe_hold_time_cli, 'encapsulation_cli': l_1_encapsulation_cli, 'encapsulation_dot1q_cli': l_1_encapsulation_dot1q_cli, 'host_proxy_cli': l_1_host_proxy_cli, 'interface_ip_nat': l_1_interface_ip_nat, 'network_encapsulation': l_1_network_encapsulation, 'network_flag': l_1_network_flag, 'port_channel_interface': l_1_port_channel_interface, 'sorted_vlans_cli': l_1_sorted_vlans_cli})):
                yield event
        if t_7(environment.getattr(l_1_port_channel_interface, 'ospf_cost')):
            pass
            yield '   ip ospf cost '
            yield str(environment.getattr(l_1_port_channel_interface, 'ospf_cost'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ospf_network_point_to_point'), True):
            pass
            yield '   ip ospf network point-to-point\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ospf_authentication'), 'simple'):
            pass
            yield '   ip ospf authentication\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'ospf_authentication'), 'message-digest'):
            pass
            yield '   ip ospf authentication message-digest\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ospf_authentication_key')):
            pass
            yield '   ip ospf authentication-key 7 '
            yield str(t_2(environment.getattr(l_1_port_channel_interface, 'ospf_authentication_key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'ospf_area')):
            pass
            yield '   ip ospf area '
            yield str(environment.getattr(l_1_port_channel_interface, 'ospf_area'))
            yield '\n'
        for l_2_ospf_message_digest_key in t_3(environment.getattr(l_1_port_channel_interface, 'ospf_message_digest_keys'), 'id'):
            _loop_vars = {}
            pass
            if (t_7(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm')) and t_7(environment.getattr(l_2_ospf_message_digest_key, 'key'))):
                pass
                yield '   ip ospf message-digest-key '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'id'))
                yield ' '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm'))
                yield ' 7 '
                yield str(t_2(environment.getattr(l_2_ospf_message_digest_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
        l_2_ospf_message_digest_key = missing
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'service_policy'), 'pbr'), 'input')):
            pass
            yield '   service-policy type pbr input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'service_policy'), 'pbr'), 'input'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'sparse_mode'), True):
            pass
            yield '   pim ipv4 sparse-mode\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'bidirectional'), True):
            pass
            yield '   pim ipv4 bidirectional\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'border_router'), True):
            pass
            yield '   pim ipv4 border-router\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'hello'), 'interval')):
            pass
            yield '   pim ipv4 hello interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'hello'), 'interval'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'hello'), 'count')):
            pass
            yield '   pim ipv4 hello count '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'hello'), 'count'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'dr_priority')):
            pass
            yield '   pim ipv4 dr-priority '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'dr_priority'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'pim'), 'ipv4'), 'bfd'), True):
            pass
            yield '   pim ipv4 bfd\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security')):
            pass
            if (t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'enabled'), True) or t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'shutdown')):
                pass
                yield '   switchport port-security\n'
            elif t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'protect'):
                pass
                if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'violation'), 'protect_log'), True):
                    pass
                    yield '   switchport port-security violation protect log\n'
                else:
                    pass
                    yield '   switchport port-security violation protect\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'disabled'), True):
                pass
                yield '   switchport port-security mac-address maximum disabled\n'
            elif t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'disabled'), False):
                pass
                yield '   no switchport port-security mac-address maximum disabled\n'
            elif t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'limit')):
                pass
                yield '   switchport port-security mac-address maximum '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'limit'))
                yield '\n'
            if (not t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'protect')):
                pass
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'vlans')):
                    pass
                    l_1_sorted_vlans_cli = []
                    _loop_vars['sorted_vlans_cli'] = l_1_sorted_vlans_cli
                    for l_2_vlan in environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'vlans'):
                        _loop_vars = {}
                        pass
                        if (t_7(environment.getattr(l_2_vlan, 'range')) and t_7(environment.getattr(l_2_vlan, 'mac_address_maximum'))):
                            pass
                            for l_3_id in t_4(environment.getattr(l_2_vlan, 'range')):
                                l_3_port_sec_cli = missing
                                _loop_vars = {}
                                pass
                                l_3_port_sec_cli = str_join(('switchport port-security vlan ', l_3_id, ' mac-address maximum ', environment.getattr(l_2_vlan, 'mac_address_maximum'), ))
                                _loop_vars['port_sec_cli'] = l_3_port_sec_cli
                                context.call(environment.getattr((undefined(name='sorted_vlans_cli') if l_1_sorted_vlans_cli is missing else l_1_sorted_vlans_cli), 'append'), (undefined(name='port_sec_cli') if l_3_port_sec_cli is missing else l_3_port_sec_cli), _loop_vars=_loop_vars)
                            l_3_id = l_3_port_sec_cli = missing
                    l_2_vlan = missing
                    for l_2_cli in t_3((undefined(name='sorted_vlans_cli') if l_1_sorted_vlans_cli is missing else l_1_sorted_vlans_cli)):
                        _loop_vars = {}
                        pass
                        yield '   '
                        yield str(l_2_cli)
                        yield '\n'
                    l_2_cli = missing
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'vlan_default_mac_address_maximum')):
                    pass
                    yield '   switchport port-security vlan default mac-address maximum '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'port_security'), 'vlan_default_mac_address_maximum'))
                    yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'enable'), True):
            pass
            yield '   ptp enable\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'mpass'), True):
            pass
            yield '   ptp mpass\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'announce'), 'interval')):
            pass
            yield '   ptp announce interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'announce'), 'interval'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'announce'), 'timeout')):
            pass
            yield '   ptp announce timeout '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'announce'), 'timeout'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'delay_mechanism')):
            pass
            yield '   ptp delay-mechanism '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'delay_mechanism'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'delay_req')):
            pass
            yield '   ptp delay-req interval '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'delay_req'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'profile'), 'g8275_1'), 'destination_mac_address')):
            pass
            yield '   ptp profile g8275.1 destination mac-address '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'profile'), 'g8275_1'), 'destination_mac_address'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'role')):
            pass
            yield '   ptp role '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'role'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'sync_message'), 'interval')):
            pass
            yield '   ptp sync-message interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'sync_message'), 'interval'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'transport')):
            pass
            yield '   ptp transport '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'transport'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'vlan')):
            pass
            yield '   ptp vlan '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'ptp'), 'vlan'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'service_policy'), 'qos'), 'input')):
            pass
            yield '   service-policy type qos input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'service_policy'), 'qos'), 'input'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'service_profile')):
            pass
            yield '   service-profile '
            yield str(environment.getattr(l_1_port_channel_interface, 'service_profile'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'trust')):
            pass
            if (environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'trust') == 'disabled'):
                pass
                yield '   no qos trust\n'
            else:
                pass
                yield '   qos trust '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'trust'))
                yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'cos')):
            pass
            yield '   qos cos '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'cos'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'dscp')):
            pass
            yield '   qos dscp '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'qos'), 'dscp'))
            yield '\n'
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'shape'), 'rate')):
            pass
            yield '   shape rate '
            yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'shape'), 'rate'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'sflow')):
            pass
            if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'enable'), True):
                pass
                yield '   sflow enable\n'
            elif t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'enable'), False):
                pass
                yield '   no sflow enable\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'egress'), 'enable'), True):
                pass
                yield '   sflow egress enable\n'
            elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'egress'), 'enable'), False):
                pass
                yield '   no sflow egress enable\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'egress'), 'unmodified_enable'), True):
                pass
                yield '   sflow egress unmodified enable\n'
            elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'sflow'), 'egress'), 'unmodified_enable'), False):
                pass
                yield '   no sflow egress unmodified enable\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_enable')):
            pass
            yield '   isis enable '
            yield str(environment.getattr(l_1_port_channel_interface, 'isis_enable'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_bfd'), True):
            pass
            yield '   isis bfd\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type')):
            pass
            yield '   isis circuit-type '
            yield str(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_metric')):
            pass
            yield '   isis metric '
            yield str(environment.getattr(l_1_port_channel_interface, 'isis_metric'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_passive'), True):
            pass
            yield '   isis passive\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'), False):
            pass
            yield '   no isis hello padding\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'), True):
            pass
            yield '   isis hello padding\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'), True):
            pass
            yield '   isis network point-to-point\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode')) and (environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode') in ['text', 'md5'])):
            pass
            yield '   isis authentication mode '
            yield str(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'))
            yield '\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'isis_authentication_key')):
            pass
            yield '   isis authentication key 7 '
            yield str(t_2(environment.getattr(l_1_port_channel_interface, 'isis_authentication_key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
            yield '\n'
        for l_2_section in t_3(environment.getattr(l_1_port_channel_interface, 'storm_control')):
            _loop_vars = {}
            pass
            if (l_2_section != 'all'):
                pass
                if t_7(environment.getattr(environment.getitem(environment.getattr(l_1_port_channel_interface, 'storm_control'), l_2_section), 'level')):
                    pass
                    if t_7(environment.getattr(environment.getitem(environment.getattr(l_1_port_channel_interface, 'storm_control'), l_2_section), 'unit'), 'pps'):
                        pass
                        yield '   storm-control '
                        yield str(t_6(context.eval_ctx, l_2_section, '_', '-'))
                        yield ' level pps '
                        yield str(environment.getattr(environment.getitem(environment.getattr(l_1_port_channel_interface, 'storm_control'), l_2_section), 'level'))
                        yield '\n'
                    else:
                        pass
                        yield '   storm-control '
                        yield str(t_6(context.eval_ctx, l_2_section, '_', '-'))
                        yield ' level '
                        yield str(environment.getattr(environment.getitem(environment.getattr(l_1_port_channel_interface, 'storm_control'), l_2_section), 'level'))
                        yield '\n'
        l_2_section = missing
        if t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'storm_control'), 'all')):
            pass
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'storm_control'), 'all'), 'level')):
                pass
                if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'storm_control'), 'all'), 'unit'), 'pps'):
                    pass
                    yield '   storm-control all level pps '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'storm_control'), 'all'), 'level'))
                    yield '\n'
                else:
                    pass
                    yield '   storm-control all level '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'storm_control'), 'all'), 'level'))
                    yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'logging'), 'event'), 'storm_control_discards'), True):
            pass
            yield '   logging event storm-control discards\n'
        elif t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'logging'), 'event'), 'storm_control_discards'), False):
            pass
            yield '   no logging event storm-control discards\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_portfast'), 'edge'):
            pass
            yield '   spanning-tree portfast\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_portfast'), 'network'):
            pass
            yield '   spanning-tree portfast network\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpduguard')) and (environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpduguard') in [True, 'True', 'enabled'])):
            pass
            yield '   spanning-tree bpduguard enable\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpduguard'), 'disabled'):
            pass
            yield '   spanning-tree bpduguard disable\n'
        if (t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpdufilter')) and (environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpdufilter') in [True, 'True', 'enabled'])):
            pass
            yield '   spanning-tree bpdufilter enable\n'
        elif t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_bpdufilter'), 'disabled'):
            pass
            yield '   spanning-tree bpdufilter disable\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'spanning_tree_guard')):
            pass
            if (environment.getattr(l_1_port_channel_interface, 'spanning_tree_guard') == 'disabled'):
                pass
                yield '   spanning-tree guard none\n'
            else:
                pass
                yield '   spanning-tree guard '
                yield str(environment.getattr(l_1_port_channel_interface, 'spanning_tree_guard'))
                yield '\n'
        if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup_link'), 'interface')):
            pass
            l_1_backup_link_cli = str_join(('switchport backup-link ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup_link'), 'interface'), ))
            _loop_vars['backup_link_cli'] = l_1_backup_link_cli
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup_link'), 'prefer_vlan')):
                pass
                l_1_backup_link_cli = str_join(((undefined(name='backup_link_cli') if l_1_backup_link_cli is missing else l_1_backup_link_cli), ' prefer vlan ', environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup_link'), 'prefer_vlan'), ))
                _loop_vars['backup_link_cli'] = l_1_backup_link_cli
            yield '   '
            yield str((undefined(name='backup_link_cli') if l_1_backup_link_cli is missing else l_1_backup_link_cli))
            yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'preemption_delay')):
                pass
                yield '   switchport backup preemption-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'preemption_delay'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'mac_move_burst')):
                pass
                yield '   switchport backup mac-move-burst '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'mac_move_burst'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'mac_move_burst_interval')):
                pass
                yield '   switchport backup mac-move-burst-interval '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'mac_move_burst_interval'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'initial_mac_move_delay')):
                pass
                yield '   switchport backup initial-mac-move-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'initial_mac_move_delay'))
                yield '\n'
            if t_7(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'dest_macaddr')):
                pass
                yield '   switchport backup dest-macaddr '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'backup'), 'dest_macaddr'))
                yield '\n'
        for l_2_link_tracking_group in t_3(environment.getattr(l_1_port_channel_interface, 'link_tracking_groups'), 'name'):
            _loop_vars = {}
            pass
            if (t_7(environment.getattr(l_2_link_tracking_group, 'name')) and t_7(environment.getattr(l_2_link_tracking_group, 'direction'))):
                pass
                yield '   link tracking group '
                yield str(environment.getattr(l_2_link_tracking_group, 'name'))
                yield ' '
                yield str(environment.getattr(l_2_link_tracking_group, 'direction'))
                yield '\n'
        l_2_link_tracking_group = missing
        if (t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'link_tracking'), 'direction')) and t_7(environment.getattr(environment.getattr(l_1_port_channel_interface, 'link_tracking'), 'groups'))):
            pass
            for l_2_group_name in environment.getattr(environment.getattr(l_1_port_channel_interface, 'link_tracking'), 'groups'):
                _loop_vars = {}
                pass
                yield '   link tracking group '
                yield str(l_2_group_name)
                yield ' '
                yield str(environment.getattr(environment.getattr(l_1_port_channel_interface, 'link_tracking'), 'direction'))
                yield '\n'
            l_2_group_name = missing
        if t_7(environment.getattr(l_1_port_channel_interface, 'vmtracer'), True):
            pass
            yield '   vmtracer vmware-esx\n'
        if t_7(environment.getattr(l_1_port_channel_interface, 'eos_cli')):
            pass
            yield '   '
            yield str(t_5(environment.getattr(l_1_port_channel_interface, 'eos_cli'), 3, False))
            yield '\n'
    l_1_port_channel_interface = l_1_encapsulation_dot1q_cli = l_1_encapsulation_cli = l_1_client_encapsulation = l_1_network_flag = l_1_network_encapsulation = l_1_dfe_algo_cli = l_1_dfe_hold_time_cli = l_1_host_proxy_cli = l_1_interface_ip_nat = l_1_hide_passwords = l_1_sorted_vlans_cli = l_1_backup_link_cli = missing

blocks = {}
debug_info = '7=54&9=70&10=72&11=75&13=77&14=80&16=82&17=85&19=87&20=90&22=92&24=95&27=98&28=101&30=103&32=106&35=109&36=112&38=114&39=117&41=119&42=122&44=124&45=127&47=129&48=131&50=134&51=137&54=139&56=142&57=145&59=147&60=150&62=152&63=155&65=157&66=160&68=162&69=165&71=167&74=170&77=173&78=176&80=178&81=181&83=183&84=186&86=188&87=191&89=193&90=196&92=198&93=201&95=203&98=206&99=210&101=213&102=217&104=220&106=223&109=226&112=229&115=232&116=234&117=236&118=238&120=241&122=243&123=246&125=248&126=250&127=253&129=255&131=258&133=260&134=262&135=264&136=266&137=268&138=270&140=272&141=274&142=276&143=278&144=280&145=282&147=284&148=286&150=288&153=291&156=293&157=295&158=297&159=299&160=301&161=303&162=305&163=307&164=309&166=313&168=315&169=317&170=319&173=321&174=323&176=325&177=327&178=329&179=331&180=333&181=335&182=337&183=339&184=341&186=345&189=347&190=349&191=351&192=353&197=356&200=358&201=361&203=363&204=367&205=369&206=371&207=373&209=375&210=377&211=380&214=383&215=387&216=389&217=391&218=393&219=395&220=397&221=399&224=401&225=404&227=407&228=409&229=413&230=415&231=417&232=419&233=421&235=423&236=426&239=429&240=431&241=435&242=437&243=439&244=441&245=443&246=445&249=447&250=450&254=453&256=456&259=459&262=462&263=465&265=467&266=470&268=472&269=475&271=477&274=480&275=483&277=485&278=488&280=490&281=492&283=495&284=497&285=499&286=501&288=504&290=506&291=508&292=510&293=512&295=515&297=517&299=520&303=523&304=526&306=528&307=531&309=533&310=536&313=538&314=541&316=543&317=546&319=548&321=551&324=554&325=557&327=559&330=562&331=565&333=567&334=570&336=572&339=575&341=581&343=584&346=587&347=590&349=592&350=594&356=600&357=602&358=605&359=607&360=609&361=612&362=614&363=616&364=620&367=627&368=629&369=633&372=640&373=643&377=648&378=650&379=654&382=659&383=662&385=666&386=669&389=673&392=676&393=679&395=681&396=684&398=686&401=689&404=692&405=696&406=698&407=700&409=702&410=704&412=706&413=708&415=711&417=714&418=717&420=719&421=722&423=724&424=727&426=729&427=732&429=734&430=737&432=739&433=742&435=744&436=747&438=749&439=752&441=754&442=757&444=759&445=762&447=764&448=767&450=769&453=772&455=775&458=778&459=781&461=783&463=786&466=789&467=791&468=793&470=796&471=799&473=801&476=804&478=807&481=810&482=813&484=815&485=818&487=820&488=823&489=826&492=833&493=836&495=838&498=841&501=844&504=847&505=850&507=852&508=855&510=857&511=860&513=862&516=865&517=867&519=870&520=872&526=878&528=881&530=884&531=887&533=889&534=891&535=893&536=895&537=898&538=900&539=904&540=906&544=909&545=913&548=916&549=919&553=921&556=924&559=927&560=930&562=932&563=935&565=937&566=940&568=942&569=945&571=947&572=950&574=952&575=955&577=957&578=960&580=962&581=965&583=967&584=970&586=972&587=975&589=977&590=980&592=982&593=984&596=990&599=992&600=995&602=997&603=1000&605=1002&606=1005&608=1007&609=1009&611=1012&614=1015&616=1018&619=1021&621=1024&625=1027&626=1030&628=1032&631=1035&632=1038&634=1040&635=1043&637=1045&640=1048&642=1051&645=1054&648=1057&650=1060&652=1062&653=1065&655=1067&656=1070&657=1072&658=1074&659=1077&661=1084&666=1089&667=1091&668=1093&669=1096&671=1101&675=1103&677=1106&680=1109&682=1112&685=1115&687=1118&690=1121&692=1124&695=1127&696=1129&699=1135&702=1137&703=1139&704=1141&705=1143&707=1146&708=1148&709=1151&711=1153&712=1156&714=1158&715=1161&717=1163&718=1166&720=1168&721=1171&724=1173&725=1176&726=1179&729=1184&730=1186&731=1190&734=1195&737=1198&738=1201'