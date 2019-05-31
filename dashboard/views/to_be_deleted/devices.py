from dashboard.models import Device
from django.shortcuts import render
from django.views import View
from lib.actions import init_actions
# Use test_napalm driver if debug=True in settings.py
from django.conf import settings
if (settings.DEBUG) and (settings.NAPALM) == False:
    from lib.test.test_napalm import get_network_driver
else:
    from napalm import get_network_driver

class DeviceView(View):

    def hunter(self, action_output):
        if 'nested_dict' in self.actions[self.action]:
            nested_dict = self.actions[self.action]['nested_dict']
            parent = (list(action_output))[0]
            action_output = action_output[parent][nested_dict]
        self.data_fields = self.actions[self.action]['data']
        self.device_output = dict()
        self.row_count = 0
        for interface in action_output:
            print(interface)
            self.device_output[self.row_count] = dict()
            self.device_output[self.row_count]['self'] = interface
            for item in action_output[interface]:
                self.key = None
                if item in self.data_fields:
                    self.key = item
                if type(action_output[interface]) == list:
                    if len(action_output[interface]) > 1:
                        for x in action_output[interface]:
                            if (x) == dict:
                                self.dict_hunter(x)
                    else:
                        item = 0
                    continue
                if type(action_output[interface][item]) == dict:
                    self.dict_hunter(action_output[interface][item])
                else:
                    if item in self.data_fields:
                        self.device_output[self.row_count][item] = action_output[interface][item]
            self.row_count += 1       
        print(self.device_output)
        test = list()
        for column in self.actions[self.action]['columns']:
            test.append(self.actions[self.action]['columns'][column])
            
        for i in self.device_output:
            self.test_me = test
            for key, value in self.device_output[i].items():
                self.test_me = [t.replace(key, str(value)) for t in self.test_me]
                self.context[self.action_context][i] = self.test_me
        print(self.context[self.action_context])  
    def dict_hunter(self, idict):
        for key, value in idict.items():
            print(key)
            if self.key != None:
                print('Looking for this key %s' % (self.key))
                print('Found value %s' % (value))
                self.device_output[self.row_count][self.key] = key
                self.key = None
            if type(value) == dict:
                self.dict_hunter(value)
            else:
                if key in self.data_fields:
                    if key in self.device_output[self.row_count]:
                        key_value = self.device_output[self.row_count][key]
                        if type(key_value) != list:
                            print('KEY VALUE: %s' % (key_value))
                            value_list = list()
                            value_list.append(key_value)
                            value_list.append(value)
                            value = value_list
                        elif type(key_value) == list:
                            print(key_value)
                            key_value.append(value)
                            value = key_value
                    else:
                        self.device_output[self.row_count][key] = value
                    

    def init_context(self):
        self.action_context = self.actions[self.action]['context']
        self.action_template = self.actions[self.action]['template']
        self.context = dict()
        self.context['pk'] = self.device.pk
        self.context['device'] = self.device
        self.context[self.action_context] = dict()

    def init_device_conn(self):
        driver = get_network_driver(self.device.napalm_driver)
        with driver(self.device.host, self.device.username, self.device.password) as self.device_conn:
            self.action_dispatcher()

    def action_dispatcher(self):
        action_function = self.actions[self.action]['function']
        action_output = eval('%s()' % (action_function))
        if 'data' in self.actions[self.action]:
            self.hunter(action_output)
            print(self.context[self.action_context]) 
        else:
            self.context[self.action_context] = action_output

    def get_columns(self):
        columns = list()
        for column in self.actions[self.action]['columns']:
            columns.append(column)
        return columns
                 
    def post(self, request):
        self.action = request.POST.get('action')
        self.actions = init_actions()

        stage = request.POST.get('stage', False)
        if (stage) == 'get':
            pk_list = request.POST.getlist('bulk')
            devices = Device.objects.filter(pk__in=pk_list)
            context = {
                'devices' : devices,
                'action' : self.action,
                'columns' : self.get_columns()
            }
            return render(request, 'multidevice.html', context)   
        
        pk = request.POST.get('pk')
        self.device = Device.objects.get(pk=pk)
        self.init_context()
        self.init_device_conn()
        return render(request, ('actions/%s' % (self.action_template)), self.context)
