# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

NAPALM_MAPPING = {
    'cisco_ios': 'ios',
    'cisco_iosxe': 'ios',
}

NETMIKO_MAPPING = {
    'cisco_ios': 'cisco_ios',
    'cisco_iosxe': 'cisco_ios',
}
class Device(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=70)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=30, choices=(("router", "Router"), ("switch", "Switch"), ("firewall", "Firewall")), blank=True)
    platform = models.CharField(max_length=30, choices=(("cisco_ios", "Cisco IOS"), ("cisco_iosxe", "Cisco IOS XE")), blank=True)
    site = models.CharField(max_length=30, choices=(("Short Hills 101", "Short Hills 101") , ("Short Hills 103", "Short Hills 103") , ("Center Valley", "Center Valley") , ("Austin", "Austin") , ("Waltham", "Waltham") , ("Irvine", "Irvine") , ("Santa_Clara", "Santa Clara") , ("Charlotte", "Charlotte") , ("Chicago", "Chicago") , ("Atlanta", "Atlanta") , ("Naperville", "Naperville") , ("Orange", "Orange") , ("Portland", "Portland") , ("Reston", "Reston") , ("San Francisco", "San Francisco") , ("Dallas", "Dallas") , ("London", "London") , ("Dublin", "Dublin") , ("Marlow", "Marlow") , ("Cardiff", "Cardiff") , ("Shelton", "Shelton") , ("New York City", "New York City") , ("Portland", "Portland") , ("Independence", "Independence") , ("Mississauga", "Mississauga") , ("Calgary", "Calgary") , ("Mumbai", "Mumbai") , ("Ashburn", "Ashburn") , ("Seatle", "Seatle") , ("Sydney", "Sydney") , ("Singapore", "Singapore") , ("London", "London")), blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def napalm_driver(self) -> str:
        return NAPALM_MAPPING[self.platform]

    @property
    def netmiko_device_type(self) -> str:
        return NETMIKO_MAPPING[self.platform]