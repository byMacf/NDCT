# NDCT (Network Device Configuration Tool)

A configuration tool for efficient network device management.

## Features

###### Generate network device configuration (Juniper Junos, Cisco IOS, Cisco Nexus, Cisco ASA)
  - Multivendor device configuration generation from a single YAML file
  
###### Deployments
  - Push configuration
    - Pre-checks
    - Post-checks
  - Pull configuration
  - Get device information
  - OS upgrade
  
###### Multiple interfaces
  - CLI
  - Web GUI
  
###### Data file encryption

###### Full operation logging

# Libraries
> argparse | os | difflib | yaml | netmiko | jinja2 | datetime | logging | sys | base64 | hashlib | json | ast | getpass | cryptography | time | uuid | multiprocessing | 

# Installation
```
  $ python3 setup.py install
```

# Commands
```
  $ cd NDCT/ndct/bin/
  $ ./cli.py <command>
```
add-device

add-device -n MyDevice -i 192.168.1.1 -u username -p password -o juniper|cisco_ios|cisco_nxos|cisco_asa
***

add-deployment

add-deployment -n MyDeployment -t MyDevice1 MyDevice2 -a push|pull|get -att bgp|interfaces|ospf|routes|None
***

remove-device

remove-device -n MyDevice
***

remove-deployment

remove-deployment -n MyDeployment
***

view-device

view-device -n MyDevice
***

view-deployment

view-deployment -n MyDeployment
***

list-stored-configuration

list-stored-configuration -a
***

run-deployment

run-deployment -n MyDeployment
***

config-diff

config-diff -c1 MyDevice_cisco_ios_verified.txt -c2 MyDevice_cisco_ios_generated.txt
***

generate-config

generate-config -n MyDevice -o cisco_ios
***

mark-config-verified

mark-config-verified -n MyDevice
***
