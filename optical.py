#!/usr/local/bin/python3
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.op.intopticdiag import PhyPortDiagTable
from pprint import pprint
from lxml import etree
import json
import xmltodict


hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

dev = Device(host=hostname, user=username, passwd=password)
try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

#pprint (dev.facts)

#pprint (dev.facts['re_info'])

#XML Format default
#data = dev.rpc.get_config('interfaces')
#pprint(etree.tostring(data, encoding='unicode'))

#fout=open("downtown-out.xml", "w")
#pprint(etree.tostring(data, encoding='unicode'),stream=fout)

#for interfaces in data.findall('.//interface'):
#   pprint(etree.tostring(interfaces, encoding='unicode'))
#   print (interfaces.get("<name>"))

#print (type(data))


optic=PhyPortDiagTable(dev)
optic.get()
pprint (json.loads(optic.to_json()),indent=4)


dev.close()
