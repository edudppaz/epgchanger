#!/usr/bin/python3

import getpass
import urllib3
import utils
import devclass


""" 
Current: v0.2

Script made to do renaming of EPGs on the APIC fabric, this script is NOT safe for use on
production environments without proper testing first this was tested only on a lab environments
and with basic EPG relations (Contracts, Domains, Attachments), other tests are needed:
- Service Graphs on EPG
- Static Leafs
- Fiber Channel Paths
- L3 Out EPGs
- L2 Out EPGs
- L4-L7 services"""

# Disables the insecure SSL requests warning as ACI uses a self-originated CERT in my lab#
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # Sets validation flag to enter the loop
    VALIDATION = False
    # Validation loop for IP address #
    while VALIDATION is False:
    # Asks user for the APIC management ip address #
        ACI_INPUT = input("\nPlease enter your APIC management ip address : ")
        VALIDATION = utils.valid_apic(ACI_INPUT)
        if VALIDATION is False:
            print("You have entered an invalid APIC, please check and re-enter")

    # create credentials structure
    while True:
        try:
            ACI_USER = input("\nPlease enter your APIC management username : ")
            ACI_PWD = getpass.getpass("\nPlease enter your APIC management password : ")
            APIC = devclass.APIC_CLUSTER(ACI_INPUT, ACI_USER, ACI_PWD)
            APIC.acilogin()
            break
        except KeyError:
            print("\n\nInvalid username/password, please try again\n\n")

    # Get the tenants from the APIC #
    APIC_TENANTS = utils.GetTenants(APIC)

    # Converts tenants into a list #
    TENANTS_LIST = []
    for value in APIC_TENANTS.split(","):
        if "name" in value:
            ADD_TENANT = value.split('"')[3]
            if ADD_TENANT:
                TENANTS_LIST.append(ADD_TENANT)

    # Chooses tenant from APIC #
    TENANT = utils.ChooseTenant(TENANTS_LIST)

    # Gets the EPGs for the tenant #
    TENANT_EPGS = utils.GetEPGS(APIC, TENANT)
    # Converts epgs into a list #
    EPG_LIST = []
    for value in TENANT_EPGS.split(" "):
        if "dn=" in value:
            EPG_LIST.append(value.split('"')[1])

    # Chooses EPG from tenant, returns Full DN #
    EPG_DN = utils.ChooseEPG(EPG_LIST)

    # Creates an object for the old EPG #
    OLD_EPG = devclass.EPG(APIC, TENANT, EPG_DN)
    # Gets the config from the EPG #
    OLD_EPG_CFG = OLD_EPG.getConfigAPIC()
    # Prints warning showing the config to be modified #
    print("""\n The following XML configuration on the chosen EPG will be modified,
    	save this for backup purposes\n""")
    print("\n \n " + OLD_EPG_CFG + "\n \n")

    # Warning to proceed #

    print("\n\n The process of deletion and re adding the EPG carries risk and downtime, are you sure to continue? \n \n")
    print(" 1 - YES ")
    print(" 2 - NO, EXIT SCRIPT \n\n")
    WARNING_EXIT = input("Enter your choice: ")
    if WARNING_EXIT == 2:
        print("Bye")
        exit()

    # Defines new EPG data #
    print("Enter the new EPG name \n")
    # Fetches input and validates the new EPG name #
    while True:
        NEW_EPG_NAME = input("Name : ")
        VALIDATOR_EPG = utils.valid_input(NEW_EPG_NAME)
        if VALIDATOR_EPG is False:
            break
        else:
            print("You have entered an invalid char, valid chars are a-z,A-Z,-,_\n")
            print("Please enter a new EPG name\n")
    
    print("New epg name is " + NEW_EPG_NAME)
    NEW_EPG_FULLNAME = "epg-" + NEW_EPG_NAME

    # Replaces EPG name on the old DN to get the new one #
    NEW_DN = EPG_DN.replace(OLD_EPG.fullepgname, NEW_EPG_FULLNAME)

    # Creates object for the new EPG #
    NEW_EPG = devclass.EPG(APIC, TENANT, NEW_DN)

    # Creates new config replacing name from old one #
    NEW_EPG_CFG = OLD_EPG_CFG.replace(OLD_EPG.fullepgname, NEW_EPG.fullepgname)
    # Fix for when AP name == EPG name #
    NEW_EPG_CFG = NEW_EPG_CFG.replace('name="'+ OLD_EPG.name + '"', 'name="'+ NEW_EPG.name + '"')

    # Final Validation input #
    FINAL_VAL = input("The old EPG is going to be deleted now, press ENTER to continue or CTRL+C to cancel  ")

    # Add headers to full config before push ##
    EPG_FULL_NEW = '<fvTenant name="' + NEW_EPG.tenant + '"><fvAp name="' + NEW_EPG.ap + '">' + NEW_EPG_CFG + '</fvAp></fvTenant>'
    #Deletes Old EPG#
    OLD_EPG.deleteEPG()
    #Adds new EPG#
    NEW_EPG.addEPG(EPG_FULL_NEW)
    print("\n\n\nNew EPG (Rename) has been pushed. Please verify on APIC GUI or CLI\n\n\n")

if __name__ == "__main__":
    main()
