Usage:
run main.py on Python3

### WORK IN PROGRESS ###

Python script done  labbing to test changing an EPG name via POST pushes into APIC (cant be done via GUI).

It basically logs into APIC, retrieves an EPG list, asks the user
which EPG would like to change name, retrieves the XML code for the EPG, modifies the code (putting the new name in) and pushes the new XML
into APIC.

Use at your own risk. Needs cleanup, checks, testings, etc. This was done in a couple hours as a labbing excersice and has only been tested on simple ACI deployments with EPGs + Contracts. No service-graphs, intra-tenant or advanced configuration has been tested, but it should work as long as the "contract" or "tag" is the merging point between the objects.

Ideas: Add code to push changes to vCenter as when the EPG name is changed, all VMs are left without port-group (as the port-group is removed if the APIC is integrated with vCenter), we could assign the VMs to the new port-group via the same script ;)

### v0.2 ###
Added input for Hostnames and IP Adresses
Fixed a bug where if the EPG name and APP name was the same, the script would create a new app due to Replace not being properly defined.
