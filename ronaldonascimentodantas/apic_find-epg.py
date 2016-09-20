#!/usr/bin/env python
"""
file: apic_find-epg.py

This script is used to find a specifi EPG inside the fabric
Based on script aci-show-epgs.py from acitoolkit URL: https://github.com/datacenter/acitoolkit/blob/master/samples/aci-show-epgs.py.
"""

import acitoolkit.acitoolkit as aci
import sys

def main():
    args = sys.argv
    hostname = args[1]
    username = args[2]
    password = args[3]
    findedepg = args[4]

    if (len(sys.argv) == 6) and (args[5] == "-s"):
        lookupsubstring = True
    else:
        lookupsubstring = False

    url = 'https://' + hostname
    print "Logging on APIC..."
    session = aci.Session(url, username, password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        exit()

    # Download all of the tenants, app profiles, and EPGs
    # and store the names as tuples in a list
    data = []
    i = 0       #Number of finded epgs
    tenants = aci.Tenant.get(session)
    for tenant in tenants:
        apps = aci.AppProfile.get(session, tenant)
        for app in apps:
            epgs = aci.EPG.get(session, app, tenant)
            for epg in epgs:
                if (lookupsubstring):
                    if (findedepg in epg.name):
                        i = i + 1
                        data.append((tenant.name, app.name, epg.name))
                else:
                    if (epg.name == findedepg):
                        i = i + 1
                        data.append((tenant.name, app.name, epg.name))

    if (i > 0):
        print "\nThere is %i EPGs '%s' inside the Fabric\n" % (i, findedepg)
        template = "{0:19} {1:20} {2:15}"
        print(template.format("TENANT", "APP_PROFILE", "EPG"))
        print(template.format("------", "-----------", "---"))
        for rec in data:
            print(template.format(*rec))
    else:
        print "\nThe '%s' EPGs IS NOT inside the Fabric\n" % findedepg

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
