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
opticTable:
  rpc: get-interface-optics-diagnostics-information
  item: physical-interface
  key: name
  view: opticView
opticView:
  fields:
    name: name
    rx_power: optics-diagnostics/rx-signal-avg-optical-power-dbm
"""

username = input("Device username: ")
#username = sys.argv[1]
password = getpass("Device password: ")
#password = sys.argv[2]

file= input ("Device list file:")
#file = sys.argv[3]
print("hostname",",","interface-name",",","rx-power")

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
             interfaces = opticTable(dev)
             interfaces.get()
             for interface in interfaces:
                name=interface.name
                rx=interface.rx_power
                if(rx != "- Inf" and rx!="None"):
                    print(hostname,",",name,",",rx)
                
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
