import devclass
import requests
import string
import ipaddress
import re

def valid_apic(apic):
    fqdn_re = re.compile('(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)')
    try:
        apic_input = ipaddress.ip_address(apic)
        if apic_input.version == 4:
            return True
        elif apic_input.version == 6:
                return True
    except ValueError:
        if fqdn_re.search(apic):
            return True
        else:
            return False

def valid_ip(ip_add):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

def valid_input(to_check):
    other_string = '-_'
    if len(to_check) >= 64:
        return False
    for character in to_check:
        if character not in (string.ascii_lowercase + string.ascii_uppercase +
                         string.digits + other_string):
            print("Invalid character : " + character)
            return True
        else:
            return False

def GetTenants(apic):
    COOKIES_VAR = {}
    COOKIES_VAR['APIC-Cookie'] = apic.token

    # Get tenants list
    # URL construct
    TENANTS_URL = "https://" + apic.ip_add + "/api/class/fvTenant.json"
    # Gets info from ACI API
    TENANTS_RESPONSE = requests.get(TENANTS_URL, cookies=COOKIES_VAR, verify=False)
    # Extracts text response
    TENANTS_TEXT = TENANTS_RESPONSE.text
    return TENANTS_TEXT

def ChooseTenant(list):
    print("Choose the tenant you want to make your change in: \n")
    tenant_dict = {}
    for value in list:
        tenant_dict[list.index(value)] = value
        print(str(list.index(value)) + " - " + value + "\n\n")
    while True:
        TENANT_CHOICE = int(input("Enter tenant number : "))
        if TENANT_CHOICE in tenant_dict:
            break
        else:
            print("Incorrect choice, please try again")
    return tenant_dict[TENANT_CHOICE]

def GetEPGS(apic, tenant):
    COOKIES_VAR = {}
    COOKIES_VAR['APIC-Cookie'] = apic.token
    EPG_URL = "https://" + apic.ip_add + "/api/mo/uni/tn-" + tenant + ".xml?query-target=subtree&target-subtree-class=fvAEPg"
    EPG_RESPONSE = requests.get(EPG_URL, cookies=COOKIES_VAR, verify=False)
    return EPG_RESPONSE.text

def ChooseEPG(list):
    print("\n\nChoose the EPG you want to rename \n\n")
    epg_dict = {}
    for value in list:
        epg_dict[list.index(value)] = value.split("/")[3].split("epg-")[1]
        print(str(list.index(value)) + "-" + value.split("/")[3].split("epg-")[1] + "\n\n")
    while True:
        EPG_CHOICE = int(input("Enter EPG number : "))
        if EPG_CHOICE in epg_dict:
            break
        else:
            print("Incorrect choice, please try again\n")
    EPG_DN = list[int(EPG_CHOICE)]
    return EPG_DN