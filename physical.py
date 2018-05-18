#!/usr/local/bin/python3  
import sys
from getpass import getpass
from jnpr.junos import Device
from pprint import pprint
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.exception import ConnectError
import yaml

yaml_dataPhys="""
---
physTable:
  rpc: get-interface-information
  item: physical-interface
  key: name
  view: physView
physView:
  fields:
    name: name
    admin_status: admin-status
    oper_status: oper-status
    description: description
"""

yaml_dataInt="""
---
intTable:
    rpc: get-interface-information
    item: physical-interface/logical-interface 
    key: name                                                                                                        
    view: intView
intView:
   fields:
    name: name
    description: description
    ip_address: address-family/interface-address/ifa-local
"""

username = input("Device username: ")
password = getpass("Device password: ")
file= input ("Device list file:")

globals().update(FactoryLoader().load(yaml.load(yaml_dataPhys)))
globals().update(FactoryLoader().load(yaml.load(yaml_dataInt)))

with open(file) as fp:  
    hostip = fp.readline().strip()
#go thru a router
    while hostip:
        hostip.strip()
        dev = Device(host=hostip, user=username, passwd=password)
        try:
            dev.open()
            print ("starting",hostip)
            
        except ConnectError as err:
            print ("Cannot connect to device: {0}".format(err),file=sys.stderr)
            dev.close()
            hostip = fp.readline().strip()
            continue
        
#gather some facts        
        hostname=dev.facts['hostname']
        print (hostname)
        version=dev.facts['version']
        serialnum=dev.facts['serialnumber']
        f1=open( '%s.csv' %hostname, 'w')
        print( hostname," , ",version," , " , serialnum, file=f1)

#get the physical interface information
        physinterfaces = physTable(dev)
        physinterfaces.get()
        for pinterface in physinterfaces:
            if(pinterface.oper_status == "up" and pinterface.description):
                print(pinterface.name,",", pinterface.description, file=f1)
                    
#get the logical interface inforation                
        intinterfaces = intTable(dev)
        intinterfaces.get()
        for linterface in intinterfaces:
            if(linterface.description or linterface.ip_address):
                print(linterface.name,",",linterface.description,",",linterface.ip_address,file=f1)
                        
#close the router        
        f1.close()
        dev.close()
#loop
        hostip = fp.readline().strip()
