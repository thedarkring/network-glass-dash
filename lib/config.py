def init_settings():
    settings = {
        'device_limit': 10,
        'instant_search': False,
    }
    return settings

def init_actions():
    actions = {
        'get_lldp_neighbors': {
            'name': 'LLDP Neighbors',
            'function': 'self.device_conn.get_lldp_neighbors',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'data': ['self', 'hostname', 'port'],
            'columns': {
                'Interface':  'self',
                'Hostname': 'hostname',
                'Port': 'port',
            }
        },
        'get_mac_address_table': {
            'name': 'Mac Address Table',
            'function': 'self.device_conn.get_mac_address_table',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'data': ['mac', 'interface', 'vlan', 'static', 'active'],
            'columns': {
                'MAC':  'mac',
                'Interface': 'interface',
                'VLAN': 'vlan',
                'Static': 'static',
                'Active': 'active'
            },
            'replace': {
                'static': {
                    True: {
                        "value": "Up",
                        "element": "span",
                        "class": "badge badge-pill badge-success"
                    },
                    False: {
                        "value": "Down",
                        "element": "span",
                        "class": "badge badge-pill badge-danger"
                    }
                },
            }
        },
        'get_interfaces': {
            'name': 'Get Interfaces',
            'function': 'self.device_conn.get_interfaces',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'data': ['self', 'description', 'is_up', 'is_enabled', 'speed'],
            'columns': {
                'Interface Name': 'self',
                'Description': 'description',
                'UP/Down': 'is_up',
                'Enabled/Disabled': 'is_enabled',
                'Speed': 'speed',
            },
            'replace': {
                'is_up': {
                    True: {
                        "value": "Up",
                        "element": "span",
                        "class": "badge badge-pill badge-success"
                    },
                    False: {
                        "value": "Down",
                        "element": "span",
                        "class": "badge badge-pill badge-danger"
                    }
                },
                'is_enabled': {
                    True: {
                        "value": "Enabled",
                        "element": "span",
                        "class": "badge badge-pill badge-success"
                    },
                    False: {
                        "value": "Disabled",
                        "element": "span",
                        "class": "badge badge-pill badge-danger"
                    }
                },
                'speed': {
                    '*': {
                        "value": "selfMB/s",
                        "element": "i",
                        "class": "fa fa-tachometer"
                    },
                }
            }
        },
        'get_arp_table': {
            'name': 'Get Arp Table',
            'function': 'self.device_conn.get_arp_table',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'data': ['interface', 'mac', 'ip', 'age'],
            'columns': {
                'Interface': 'interface',
                'Mac Address': 'mac',
                'IP': 'ip',
                'Age': 'age',
            }
        },
        'get_ips': {
            'name': 'IP Addresses',
            'function': 'self.device_conn.get_interfaces_ip',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'data': ['self', 'ipv4', 'prefix_length'],
            'columns': {
                'Interface':  'self',
                'IP': 'ipv4/prefix_length'
            }
        },
        'get_bgp': {
            'name': 'BGP Peers',
            'function': 'self.device_conn.get_bgp_neighbors',
            'context': 'hunter',
            'template': 'hunter_template.html',
            'nested_dict': 'peers',
            'data': ['self', 'description', 'is_up', 'uptime', 'is_enabled', 'address_family', 'sent_prefixes', 'received_prefixes'],
            'columns': {
                'Peer IP': 'self',
                'Peer Description': 'description',
                'UP/Down': 'is_up (uptime)',
                'Enabled/Disabled': 'is_enabled',
                'Address Family': 'address_family',
                'Received': 'received_prefixes',
                'Sent': 'sent_prefixes'
            },
            'render_func': {
                'uptime': 'up_hours("uptime")'
            },
            'replace': {
                'is_up': {
                    True: {
                        "value": "Up",
                        "element": "span",
                        "class": "badge badge-pill badge-success"
                    },
                    False: {
                        "value": "Down",
                        "element": "span",
                        "class": "badge badge-pill badge-danger"
                    }
                },
                'is_enabled': {
                    True: {
                        "value": "Enabled",
                        "element": "span",
                        "class": "badge badge-pill badge-success"
                    },
                    False: {
                        "value": "Disabled",
                        "element": "span",
                        "class": "badge badge-pill badge-danger"
                    }
                }
            }
        },  
        'get_command': {
            'name': 'Command',
            'function': 'self.command_executor',
            'context': 'command',
            'template': 'command.html',
            'columns': {
                'Command': 'key',
                'Output': 'value'
            }
        }, 
        'get_commands': {
            'name': 'Test',
            'function': 'self.command_executor',
            'context': 'command',
            'template': 'command.html',
            'columns': {
                'Command': 'key',
                'Output': 'value'
            }
        },      
    }
    return actions