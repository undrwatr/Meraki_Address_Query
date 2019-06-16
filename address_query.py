#!/usr/bin/python

#main varaiables to be anonymized later before upload to github:
organization = cred.org
key = cred.key

#imports
import requests
import json
import os
import time
import difflib
import sys

#Import the CRED module from a separate directory
sys.path.insert(0,'../CRED')
import cred

#Main URL for the Meraki Platform
dashboard = "https://dashboard.meraki.com"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

# open files for writing
address = open("address.txt", "w", 0)
error = open("error.txt", "w", 0)

#pull back all of the networks for the organization
get_network_url = dashboard + '/api/v0/organizations/%s/networks' % organization

#request the network data
get_network_response = requests.get(get_network_url, headers=headers)

#puts the data into a json format
get_network_json = get_network_response.json()

for network in get_network_json:
    get_device_url = dashboard + '/api/v0/networks/%s/devices' % network["id"]
    get_device_response = requests.get(get_device_url, headers=headers)
    time.sleep(4)
    get_device_json = get_device_response.json()
    for device in get_device_json:
        get_uplink_url = dashboard + '/api/v0/networks/%s/devices' % network["id"]
        get_uplink_response = requests.get(get_uplink_url, headers=headers)
        get_uplink_json = get_uplink_response.json()
        for uplink in get_uplink_json:
            try:
                address.write(network["name"] + " " + uplink["address"] + "\n")
            except TypeError:
                error.write(network["name"] + "\n")

        
#close the files when done so that they can be used for the next section.
address.close
error.close
