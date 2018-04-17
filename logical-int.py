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
IntTable:
  rpc: get-interface-information
  item: physical-interface/logical-interface
  key: name
  view: IntView
IntView:
  fields:
    name: name
    description: description
    ip_address: address-family/interface-address/ifa-local
"""

username = input("Device username: ")
password = getpass("Device password: ")
file= input ("Device list file:")
suffix=input ("domain suffix:")
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
             interfaces = IntTable(dev)
             interfaces.get()
             for interface in interfaces:
                name=interface.name
                int=name.replace("/","-")
                better=int.replace(".","u")
                host='{}.{}'.format(better,hostname)
                fqdn='{}.{}'.format(host,suffix)

                if(interface.ip_address and type(interface.ip_address)==str):
                   print (ipaddress.ip_address(interface.ip_address).reverse_pointer,"\tPTR\t",fqdn)
                   print
    
                if(interface.ip_address and type(interface.ip_address)==list):
                   print (ipaddress.ip_address(interface.ip_address[1]).reverse_pointer,"\tPTR\t",fqdn)
                   print
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
