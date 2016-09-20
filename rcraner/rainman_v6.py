#!/user/bin/env python

import xmltodict
import json
import sys
from device import Device
import csv

def vtp_info(sw):

  getstatus = sw.show('show vtp status')
  show_vtp_status_dict = xmltodict.parse(getstatus[1])
  vtpenable = show_vtp_status_dict['ins_api']['outputs']['output']['code']
  if vtpenable == "200":
    statusdata = show_vtp_status_dict['ins_api']['outputs']['output']['body']

    getpass = sw.show('show vtp password')
    show_vtp_pass_dict = xmltodict.parse(getpass[1])
    statuspass = show_vtp_pass_dict['ins_api']['outputs']['output']['body']

    gethostname = sw.show('show hostname')
    show_hostname_dict = xmltodict.parse(gethostname[1])
    statushost = show_hostname_dict['ins_api']['outputs']['output']['body']

    version = statusdata['version']
    mode = statusdata['oper_mode']
    domain = statusdata['domain_name']
    config_rev = statusdata['config_rev']
    num_of_vlans = statusdata['num_current_vlans']
    pruning_mode = statusdata['pruning_mode']
    password = statuspass['passwd']
    hostname = statushost['hostname']

    vtp_info_dict = hostname + ',' + version + ',' + mode + ',' + domain + ',' + config_rev + ',' + num_of_vlans + ',' + pruning_mode + ',' + password

    return vtp_info_dict
  else:
  	vtp_info_dict = "VTP Not Enabled"

  	return vtp_info_dict

def connect_pulldata(ipaddr, uname, pword):

  switch = Device(ip=ipaddr, username=uname, password=pword)
  switch.open()

  vtp_facts = ipaddr + ',' + vtp_info(switch)

  csvwriter = csv.writer(open("vtp.csv", "a"))

  csvwriter.writerow([vtp_facts])

def main():

  switch_input_file = csv.DictReader(open("switch_input_file.csv"))

  for row in switch_input_file:
    ipaddr=str(row["ip_address"])
    uname=str(row["uname"])
    pword=str(row["pword"])
    connect_pulldata(ipaddr, uname, pword)
    

  print "Data Gathered.  Please check vtp.csv"
  
if __name__ == "__main__":
  main()
