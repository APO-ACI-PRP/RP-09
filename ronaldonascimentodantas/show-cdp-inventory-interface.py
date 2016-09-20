#!/usr/bin/env python

#file: show-cdp-inventory-interface.py
#this python script is used to return the neighbor name and interface using CDP

import xmltodict
import json
import sys
from device import Device

def show_cdp(sw, interface):

    result_final = ""
    command = 'show cdp neighbor interface ' + interface
    
    getdata = sw.show(command)
    result  = xmltodict.parse(getdata[1])

    try:
        data = result['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']
        neighbor_name = data['device_id']
        neighbor_interface = data['port_id']
        result_final = '{:<30}'.format( neighbor_name ) + '{:<14}'.format( neighbor_interface )
    except KeyError:
        result_final = ""

    return result_final

def main():

    args = sys.argv

    if len(args)  == 5:
        switch = Device(ip=args[1], username=args[2], password=args[3])
        interface_name = args[4]   # Get the interface name
        
        try:
            switch.open()
            cdp = show_cdp(switch, interface_name)
            print cdp
        except:
            print "\nshow-cdp-inventory-interface.py: Please review your input parameters.\n\nSyntax: show-cdp-inventory-interface.py <switch-name> <username> <password> <interface_name>\n"
    else:
        print "\nshow-cdp-inventory-interface.py: Invalid Key.\nSyntax: show-cdp-inventory-interface.py <switch-name> <username> <password> <interface_name>\n"

if __name__ == "__main__":
    main()
