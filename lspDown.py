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
LspTable:
  rpc: get-mpls-lsp-information
  item: rsvp-session-data/rsvp-session/mpls-lsp
  key: destination-address
  view: LspView

LspView:
  fields:
    dest: destination-address 
    state: lsp-state
    count: route-count
    active: active-path
    name: name
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
#             pprint(dev.facts)
             hostname=dev.facts['hostname']
             version=dev.facts['version']
             serialnum=dev.facts['serialnumber']
             model=dev.facts['model']
#             print ( hostname," , ",version," , " , serialnum,",",model)
             if("M" in model ):
                  globals().update(FactoryLoader().load(yaml.load(yaml_data)))
                  downlsp = LspTable(dev)
                  downlsp.get()
 #                 pprint(downlsp)
                  for lsp in downlsp:
                      if (lsp.state =="Dn"):
                          print(hostname,",",hostip,",",lsp.dest, "," ,lsp.name,",",lsp.state)
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
