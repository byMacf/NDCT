# NDCT (Network Device Configuration Tool)

A configuration tool for efficient network device management.

## Features

###### Generate network device configuration (Juniper Junos, Cisco IOS, Cisco Nexus, Cisco ASA)
  - Multivendor device configuration generation from a single YAML file
  
###### Deployments
  - Push configuration
  - Pull configuration
  - Get device information
  
###### Interface
  - CLI
  
###### File encryption
  - AES 128-bit

###### Full operation logging

# Libraries
> click | os | difflib | yaml | netmiko | jinja2 | datetime | logging | sys | base64 | hashlib | json | ast | getpass | cryptography | time | uuid | multiprocessing | pythonping

# Installation
```
  $ cd NDCT
  $ python3 setup.py install
```

# Commands
```
  $ ndct _____
  
  configuration  Configuration actions
  crypt          Crypt actions
  deployment     Deployment actions
  device         Device actions
```
Add device

ndct device add -n MyDevice -i 192.168.1.1 -u username -p password -o juniper|cisco_ios|cisco_nxos|cisco_asa
***

Add deployment

ndct deployment add -n MyDeployment -t MyDevice1 MyDevice2 -a push|pull|get -att bgp|interfaces|ospf|routes|config
***

Remove device

ndct device remove -n MyDevice
***

Remove deployment

ndct deployment remove -n MyDeployment
***

View device

ndct device view -n MyDevice
***

View deployment

ndct deployment view -n MyDeployment
***

List stored configuration

ndct configuration display
***

Run deployment

ndct deployment run -n MyDeployment
***

Config diff

ndct configuration diff -c1 MyDevice_cisco_ios_verified.txt -c2 MyDevice_cisco_ios_generated.txt
***

Generate config

ndct configuration generate -n MyDevice 
***

Verify config

ndct configuration verify -n MyDevice  -n MyDevice
***
