import json
import requests
import time

class APIC_CLUSTER():
    def __init__(self, ip_add, username="cisco", password="cisco", token="x", cookie={}):
        self.ip_add = ip_add
        self.username = username
        self.password = password
        self.url = "https://" + ip_add + "/api/"
        self.token = token
        self.cookie = cookie

    def acilogin(self):
        name_pwd = {'aaaUser': {'attributes': {'name': self.username, 'pwd': self.password}}}
        json_cred = json.dumps(name_pwd)
        # log in to API
        login_url = self.url + 'aaaLogin.json'
        post_response = requests.post(login_url, data=json_cred, verify=False)

        # get token from login response structure
        print(post_response)
        auth_push = json.loads(post_response.text)
        login_attributes = auth_push['imdata'][0]['aaaLogin']['attributes']
        auth_token_fetch = login_attributes['token']
        ## Creates cookie array from token ##
        self.token = auth_token_fetch

    def printtoken(self):
        print("The APIC session token is " + self.token)

    def printurl(self):
        print("The APIC login url is " + self.url)

class EPG():
    def __init__(self, apic, tenant, full_dn):
        self.apic = apic
        self.tenant = tenant
        self.full_dn = full_dn
        for value in self.full_dn.split("/"):
            if "ap-" in value:
                self.fullapname = value
                self.ap = value[3:]
            if "epg-" in value:
                self.fullepgname = value
                self.name = value[4:]

    def getConfigAPIC(self, config="x"):
        COOKIES_VAR = {}
        COOKIES_VAR['APIC-Cookie'] = self.apic.token
        url = "https://" + self.apic.ip_add + "/api/mo/" + self.full_dn + ".xml?rsp-subtree=full&rsp-prop-include=config-only"
        config_xml = requests.get(url, cookies=COOKIES_VAR, verify=False).text
        # Strips XML headers from response #
        config = "<fvAEPg" + config_xml.split("fvAEPg")[1] + "fvAEPg>"
        self.config = config
        return self.config
    
    def deleteEPG(self):
        COOKIES_VAR = {}
        COOKIES_VAR['APIC-Cookie'] = self.apic.token
        # Prepares URL for deletion #
        POST_URL = "https://" + self.apic.ip_add + "/api/mo/uni.xml"
        print("Deleting old epg.................")
        DELETE = '<fvTenant name="' + self.tenant + '"><fvAp name="' + self.ap + '"><fvAEPg descr="" dn="' + self.full_dn + '" name="' + self.name + '" status=deleted></fvAEPg></fvAp></fvTenant>'
        POST = requests.post(POST_URL, data=DELETE, cookies=COOKIES_VAR, verify=False)
        time.sleep(1)
    
    def addEPG(self, cfg):
        COOKIES_VAR = {}
        COOKIES_VAR['APIC-Cookie'] = self.apic.token
        # Prepares URL for add #
        POST_URL = "https://" + self.apic.ip_add + "/api/mo/uni.xml"
        print("Adding old epg.................")
        EPG_POST = requests.post(POST_URL, data=cfg, cookies=COOKIES_VAR, verify=False)
        time.sleep(1)
print("\n\n\nNew EPG (Rename) has been pushed. Please verify on APIC GUI or CLI\n\n\n")