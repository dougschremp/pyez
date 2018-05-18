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


username = input("Device username: ")
password = getpass("Device password: ")
file= input ("Device list file:")
with open(file) as fp:  
    hostip = fp.readline().strip()
    while hostip:
        hostip.strip()
        dev = Device(host=hostip, user=username, passwd=password)
        try:
            dev.open()
        except ConnectError as err:
            print ("Cannot connect to device: {0}".format(err))
            sys.exit(1)
            dev.close()
            hostip = fp.readline().strip()
            continue
                 
        hostname=dev.facts['hostname']
        version=dev.facts['version']
        serialnum=dev.facts['serialnumber']
        print ( hostname," , ",version," , " , serialnum)
        optic=PhyPortDiagTable(dev)
        optic.get()
        print (optic.rx_optic_power)
        dev.close()
        hostip = fp.readline().strip()
        
