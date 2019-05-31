import os, json, inspect
import pickle

class Driver(object):
    def __init__(self, host, username, password):
        self.path = os.getcwd()
        self.pickle = None

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        return False

    def load_json(self):
        caller = inspect.stack()[1].function
        print('Testing for %s' % (caller))
        json_path = os.path.join(self.path, 'lib', 'test', 'test_json', '%s.json' % (caller))
        json_file = open(json_path, 'rb')
        if (self.pickle):
            output = pickle.load(json_file)
            return output
        return json.load(json_file)

    def get_interfaces(self):
        return self.load_json()

    def get_interfaces_ip(self):
        return self.load_json()

    def get_bgp_neighbors(self):
        return self.load_json()

    def get_lldp_neighbors(self):
        return self.load_json()

    def get_mac_address_table(self):
        self.pickle = True
        return self.load_json()

    def get_arp_table(self):
        self.pickle = True
        return self.load_json()

    def cli(self, command):
        print('Command Executor Test Napalm')
        print(command)
        return self.load_json()

    def test(self):
        return self.load_json()

def get_network_driver(napalm_driver):
    print(napalm_driver)
    return Driver
