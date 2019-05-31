from django.views import View
from django.shortcuts import render
from dashboard.models import Device
from lib.config import init_actions, init_settings

class DashboardView(View):

    def __init__(self):
        self.settings = init_settings()

    def get(self, request):
        devices = Device.objects.all()
        actions_dict = init_actions()
        actions_context = dict()
        for action in actions_dict:
            actions_context[action] = actions_dict[action]['name']
        context = {
            'devices': devices,
            'actions': actions_context,
            'instant_search': self.settings['instant_search'],
            'device_limit': self.settings['device_limit'],
        }
        return render(request, 'dashboard.html', context)