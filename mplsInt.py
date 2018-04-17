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
RsvpTable:
  rpc: get-rsvp-interface-information
  item: rsvp-interface
  key: interface-name
  view: RsvpView

RsvpView:
  fields:
    name: interface-name
    state: rsvp-status

MplsTable:
   rpc: get-mpls-interface-information
   item: mpls-interface
   key: interface-name
   view: MplsView

MplsView:
  fields:
    name: interface-name
    state: mpls-interface-state

OspfTable:
   rpc: get-ospf-interface-information
   item: ospf-interface
   key: interface-name
   view: OspfView

OspfView:
  fields:
    name: interface-name
    state: ospf-interface-state
    count: neighbor-count

PhysTable:
   rpc: get-interface-information
   item:  physical-interface/logical-interface
   key: name
   view: PhysView

PhysView:
  fields:
    name: name
    admin: admin-status
    oper:  oper-status
    
"""

globals().update(FactoryLoader().load(yaml.load(yaml_data)))
username = input("Device username: ")
password = getpass("Device password: ")

file= input ("Device list file:")


mplsInt={}
rsvpInt={}
ospfInt={}
physInt={}

with open(file) as fp:  
         hostip = fp.readline().strip()
#go thru a router
         while hostip:
             mplsInt={}
             rsvpInt={}
             ospfInt={}
             physInt={}
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
             print ( hostname," , ",version," , " , serialnum,",",model)
             if("M" in model ):
                  rsvp = RsvpTable(dev)
                  rsvp.get()
                  mpls = MplsTable(dev)
                  mpls.get()
                  ospf=OspfTable(dev)
                  ospf.get()
                  phys=PhysTable(dev)
                  phys.get()
                
                  for int in mpls:
                      mplsInt[int.name] =int.state
                  for int in rsvp:
                      rsvpInt[int.name]=int.state
                  for int in ospf:
                      ospfInt[int.name]=int.state
                  for int in phys:
                      physInt[int.name]=int.oper
          
                  for int in  physInt.keys():
                      if(int in ospfInt):
                          if("Pt" in ospfInt[int]):
                              if (int in mplsInt and int in rsvpInt):
                                  print (hostname,",",int,"mpls",mplsInt[int],",","rsvp",rsvpInt[int],",","ospf",",",ospfInt[int])
                              else:
                                  if not( "255" in int):
                                      print(hostname,",",int,"OSPF only,no MPLS, RSVP")
                                  
                      else:
                          print(hostname,",",int,"NO OSPF")
 #close the router        
             dev.close()
             hostip = fp.readline().strip()
