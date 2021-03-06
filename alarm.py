#!/usr/local/bin/python3  
import sys
import ipaddress
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from pprint import pprint
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

yaml_data="""
---
AlarmTable:
  rpc: get-alarm-information
  item: alarm-detail
  key: alarm-time
  view: AlarmView
AlarmView:
  fields:
    time: alarm-time 
    type: alarm-type
    description: alarm-description
"""

username = input("Device username: ")
password = getpass("Device password: ")

file= input ("Device list file:")

with open(file) as fp:  
         hostip = fp.readline().strip()
#go thru a router
         while hostip:
             hostip.strip()
             dev = Device(host=hostip, user=username, passwd=password)
             try:
                dev.open()
             except ConnectError as err:
                print ("Cannot connect to device: {0}".format(err),file=sys.stderr)
                dev.close()
                hostip = fp.readline().strip()
                continue
             #pprint(dev.facts)
             hostname=dev.facts['hostname']
             version=dev.facts['version']
             serialnum=dev.facts['serialnumber']
             #print ( hostname," , ",version," , " , serialnum)
             globals().update(FactoryLoader().load(yaml.load(yaml_data)))
             alarms = AlarmTable(dev)
             alarms.get()
             for alarm in alarms:
                 print(hostname,",",hostip,",",alarm.time, "," ,alarm.type, ",",alarm.description)
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
