#!/usr/bin/env python

#file: show-command.py
#this python script is used to execute ANY show command from NXAPI
#without necessary to login on Sandbox to check show command availability NXAPI

import xmltodict
import json
import sys
from device import Device

def show_command(sw, command):

    command = 'show ' + command
    getdata = sw.show(command)
    return json.dumps( xmltodict.parse(getdata[1]), indent=2 )

def main():

    args = sys.argv

    if len(args)  == 5:
        switch = Device(ip=args[1], username=args[2], password=args[3])
        
        try:
            switch.open()
            showcommand = show_command(switch, args[4] )
            print showcommand

        except:
            print "\nshow-command_v2.py: Please review you input parameters.\n\nSyntax: show-command.py <switch-name> <username> <password> <show-command>\n"
    else:
        print "\nshow-command_v2.py: Invalid Key.\nSyntax: show-command.py <switch-name> <username> <password> <show-command>\n"

if __name__ == "__main__":
    main()
