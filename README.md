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
> 

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
Add single device

ndct device add -n DeviceName -i 192.168.1.1 -u username -p password -o cisco_ios|vyos
***

Add multiple devices from a file

ndct device add-from-file -f example.txt
***

Remove device

ndct device remove -n DeviceName
***

View device

ndct device view -n DeviceName
***

Add deployment

ndct deployment add -n DeploymentName -t Target1 Target2 -a get|deploy_generated|deploy_custom
***

Remove deployment

ndct deployment remove -n DeploymentName
***

View deployment

ndct deployment view -n DeploymentName
***

Run deployment

ndct deployment run -n DeploymentName
***

List stored configuration files

ndct configuration stored
***

Config diff

ndct configuration diff -c1 R1_generated.txt -c2 R2_generated.txt
***

Generate config

ndct configuration generate -n MyDevice 
***
