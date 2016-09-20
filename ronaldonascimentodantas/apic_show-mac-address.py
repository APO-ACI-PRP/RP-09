#!/usr/bin/env python
#This script is used to show all mac-address inside a fabric.

#Import the required classes and modules
import sys
from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory
from cobra.mit.request import ConfigRequest
from cobra.mit.request import ClassQuery

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: apic_show-mac-address.py <hostname> <username> <password> <mac-address>'
        sys.exit()
    else:
        hostname, username, password, macaddress = sys.argv[1:]
        url = 'https://' + hostname
        print "Logging on APIC..."

        try:
            #
            lls = LoginSession(url, username, password, secure=False)
            md = MoDirectory(lls)
            md.login()
            q = ClassQuery('fvCEp')
            q.subtree = 'children'
            q.subtreeClassFilter = 'fvRsCEpToPathEp'
            mos = md.query(q)

            #Other variables
            hasmacaddress = False
            epglists = {}
            i = -1
        
            ## Verifying all mac address:
            for mo in mos:
                for child in mo.rscEpToPathEp:
                       line = str(child.dn)
                       i = i + 1
                       if (macaddress in line):
                           hasmacaddress = True
                           epglists[i] = line

            if(hasmacaddress):
                print "\n\nThe mac-address %s IS inside the Fabric" % macaddress
                print "\nshowing the mac-address in fabric:"
                for each in epglists:
                    print epglists[each]
            else:
                print "\n\nThe mac-address %s is NOT inside the Fabric" % macaddress

        except:
            #
            print "\nPlease review your input parameters"

    print "\n"
