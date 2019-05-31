from django.shortcuts import render, redirect
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest
from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from netmiko import ConnectHandler
from dashboard.models import Device
from dashboard.serializers import DeviceSerializer
from django.views.decorators.csrf import csrf_exempt
from functools import reduce
import operator
from lib.debug_tools import debug_post
from lib.config import init_actions

class DeviceApi(APIView):
    # @method_decorator(csrf_exempt)
    def post(self, request):
        data = dict()
        devices = Device.objects.all()
        serialized = DeviceSerializer(devices, many=True)
        data['data'] = serialized.data
        return Response(data)

