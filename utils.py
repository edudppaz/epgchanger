import devclass
import requests
import string

def valid_ip(ip_add):
    ip_add_list = ip_add.split(".")
    ## Invalidates IP if it has more than 4 octets ##
    if len(ip_add_list) > 4:
        return False
    ## Invalidates IP ##
    elif int(ip_add_list[0]) > 223:
        return False
    ## Invalidates IP ##
    elif int(ip_add_list[0]) == 127:
        return False
    ## Invalidates IP ##
    elif (int(ip_add_list[0]) == 169) and (int(ip_add_list[1]) == 254):
        return False
    ## Iterates through the last 3 objects and if one if them is invalid, sets flags and breaks ##
    for i in range(1, 4):
        if (int(ip_add_list[i]) < 0) or (int(ip_add_list[i]) > 255):
            return False
    return True

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