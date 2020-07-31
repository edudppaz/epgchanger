### WORK IN PROGRESS ###
### v0.1 ###
Python script done  labbing to test changing an EPG name via POST pushes into APIC (cant be done in any other way).

I dont know if this still works as i did it on an old APIC version, it basically logs into APIC, retrieves an EPG list, asks the user
which EPG would like to change name, retrieves the XML code for the EPG, modifies the code (putting the new name in) and pushes the new XML
into APIC.

Use at your own risk. Needs cleanup, checks, testings, etc. This was done in a couple hours as a labbing excersice :)

Ideas: Add code to push changes to vCenter as when the EPG name is changed, all VMs are left without port-group (as the port-group is removed if the APIC is integrated with vCenter), we could assign the VMs to the new port-group via the same script ;)
