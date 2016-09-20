#!/usr/bin/env python

#file: show-simple-inventory.py
#This python script is used to show a simple inventory interface from a device
#all fields are printed on CSV format, and could be used to import in Excel
#fields: Interface, Speed, Description, Neighbor Name, Neighbor Interface
#Purpose: Help documentation process like an AS-Built

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
        result_final = '{:<30}'.format( neighbor_name ) + "," + '{:<14}'.format( neighbor_interface )
    except KeyError:
        result_final = ""

    return result_final

def show_interface(sw):

    getdata = sw.show('show interface description')
    show_int_description = xmltodict.parse(getdata[1])
    data_result = {}
    data = show_int_description['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']

    #Print the header
    print "%s,%s,%s,%s,%s" % ( '{:<14}'.format('Interface') , '{:<5}'.format('Speed'), '{:<60}'.format('Description'),'{:<30}'.format('Neighbor Name'),'{:<21}'.format('Neighbor Interface'))

    for each in data:
        interface_speed = " "
        interface_description = " "
        data_result['interface_name'] = each['interface']

        # Geting the interface speed
        try:
            if('speed') in each.keys():
                interface_speed = each['speed']
        except KeyError:
                interface_speed = " "

        # Geting the interface description
        try:
            if('desc') in each.keys():
                interface_description = each['desc']
        except KeyError:
                interface_description = " "

        cdp_information = show_cdp(sw, data_result['interface_name'])
        print "%s,%s,%s,%s" % ( '{0:<14.14}'.format( data_result['interface_name'] ),'{:<5}'.format( interface_speed ),'{0:<60.60}'.format(interface_description), '{0:<51.51}'.format(cdp_information) )

def main():

    args = sys.argv

    if len(args)  == 4:
        switch = Device(ip=args[1], username=args[2], password=args[3])
        
        try:
            switch.open()
            interface = show_interface(switch)
        except:
            print "\nshow-simple-inventory.py: Please review your input parameters."
    else:
        print "\nshow-simple-inventory.py: Invalid Key.\nSyntax: show-simple-inventory.py <switch-name> <username> <password>\n"

if __name__ == "__main__":
    main()
