#!/usr/local/bin/python3  
import sys
from getpass import getpass
from jnpr.junos import Device
from pprint import pprint
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

yaml_data="""
---
IntTable:
  rpc: get-interface-information
  item: physical-interface
  key: name
  view: IntView
IntView:
  fields:
    name: name
    admin_status: admin-status
    oper_status: oper-status
    description: description
"""
username = input("Device username: ")
password = getpass("Device password: ")

file= input ("Device list file:")


dev = Device(host='10.255.254.1', user=username, passwd=password)
dev.open()
#pprint(dev.facts)
hostname=dev.facts['hostname']
version=dev.facts['version']
serialnum=dev.facts['serialnumber']
print ( hostname," , ",version," , " , serialnum)
globals().update(FactoryLoader().load(yaml.load(yaml_data)))
interfaces = IntTable(dev)
interfaces.get()

for interface in interfaces:
   if(interface.oper_status == "up" and interface.description):
     print
     print ('Name: ', interface.name," , Description:", interface.description)
     print

dev.close()
