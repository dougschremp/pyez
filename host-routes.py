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
RouteTable:
  rpc: get-route-information
  item: route-table/rt
  key: re-destination
  view: RouteView
RouteView:
  fields:
    rt: rt-destination
    proto: rt-entry/protocol-name 
    nh: rt-entery/nh/via
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
             routes = RouteTable(dev)
             routes.get(table="inet.0")
             hostroute= '/32'
             for route in routes:
                 if( hostroute in route.rt):
                     rt=route.rt
                     print(rt.replace('/32',''))
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
