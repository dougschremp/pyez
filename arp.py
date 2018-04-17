#!/usr/local/bin/python3  
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

yaml_data="""
---
ArpTable:
  rpc: get-arp-table-information
  item: arp-table-entry
  key: mac-address
  view: ArpView
ArpView:
  fields:
    mac_address: mac-address
    ip_address: ip-address
    interface_name: interface-name
    host: hostname
"""

username = input("Device username: ")
password = getpass("Device password: ")

file= input ("Device list file:")
with open(file) as fp:
	hostip = fp.readline().strip()
#go thru a router                                                                                                     
	while hostip:
		hostip.strip()

		dev = Device(host=hostip, user=username, passwd=password, gather_facts=False)
		try:
			dev.open()
		except ConnectError as err:
			print ("Cannot connect to device: {0}".format(err),file=sys.stderr)
			dev.close()
			hostip = fp.readline().strip()
			continue
		globals().update(FactoryLoader().load(yaml.load(yaml_data)))
		arps = ArpTable(dev)
		arps.get()
		for arp in arps:
			print ('mac_address: ', arp.mac_address,'ip_address: ', arp.ip_address,'interface_name:', arp.interface_name,'hostname:', arp.host)

		dev.close()
		hostip = fp.readline().strip()
