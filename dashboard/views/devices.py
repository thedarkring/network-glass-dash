from dashboard.models import Device
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from lib.config import init_actions, init_settings
from lib.hunter import Hunter
import json
# Use test_napalm driver if debug=True in settings.py
from django.conf import settings
if (settings.DEBUG) and (settings.NAPALM) == False:
    from lib.test.test_napalm import get_network_driver
else:
    from napalm import get_network_driver

class DeviceView(View):

    def __init__(self):
        self.settings = init_settings()
                    
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
            action_dict = self.actions[self.action]
            h = Hunter(action_output, action_dict)
            action_output = h.clean_hunt()
        self.context[self.action_context] = action_output

    def command_executor(self):
        command = False
        print('Command Executor')
        if 'command' in self.actions[self.action]:
            command = self.actions[self.action]['command']
        elif self.command:
            command = self.command
        if (command):
            command = json.loads(command)
            return self.device_conn.cli(command)
        else:
            raise NameError('No commands to execute')

    def get_columns(self):
        columns = list()
        for column in self.actions[self.action]['columns']:
            columns.append(column)
        return columns
                 
    def post(self, request):
        self.action = request.POST.get('action')
        self.command = request.POST.get('commands', False)
        self.actions = init_actions()
        stage = request.POST.get('stage', False)

        if (stage) == 'get':
            pk_list = request.POST.getlist('bulk')
            devices = Device.objects.filter(pk__in=pk_list)
            device_count = devices.count()
            self.settings = init_settings()
            device_limit_tuple = self.settings['device_limit'],
            device_limit = int(device_limit_tuple[0])
            
            if device_count > device_limit:
                error = {
                    'device_limit': device_limit,
                    'device_count': device_count,
                    }
                return render(request, 'error.html', error)

            context = {
                'devices': devices,
                'action': self.action,
                'columns': self.get_columns(),
                'commands': self.command,
                'instant_search': self.settings['instant_search']
            }
            return render(request, 'multidevice.html', context)   
        
        pk = request.POST.get('pk')
        self.device = Device.objects.get(pk=pk)
        self.init_context()
        self.init_device_conn()
        return render(request, ('actions/%s' % (self.action_template)), self.context)
