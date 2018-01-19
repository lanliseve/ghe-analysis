import json
import sys
import requests
from requests.auth import HTTPBasicAuth

Admin_Account = "xiao-peng-feng"

Admin_Token_HPE = "a3d66d1301387ada46d1ace68c9a68fc45a9545e"
Admin_Token_DXC = "d8b4a4acc745ad8d5b445747ec88a9069109babd"
Admin_Token_Seattle = "189568fb8fcc952cd9dfc289b575800f5be2fd2c"
Admin_Token_Partner = "5cd855b757fad80a186239a997e61877781597b2"

Hostname_HPE = "github.hpe.com"
Hostname_DXC = "github.houston.entsvcs.net"
Hostname_Seattle = "github.houston.softwaregrp.net"
Hostname_Partner = "partner.github.hpe.com"

Http_Proxy  = "http://proxy.houston.hpecorp.net:8080"
Https_Proxy = "http://proxy.houston.hpecorp.net:8080"
proxyDict = { 
              "http"  : Http_Proxy, 
              "https" : Https_Proxy
            }

def get_github_url(instance, relativeurl):
    hostname = ""
    if instance == "hpe":
        hostname = Hostname_HPE
    elif instance == "seattle":
        hostname = Hostname_Seattle
    elif instance == "dxc":
        hostname = Hostname_DXC
    elif instance == "partner":
        hostname = Hostname_Partner

    url = "https://" + hostname + "/api/v3/" + relativeurl
    return url

def get_instance_by_hostname(hostname):
    instance = ""
    if hostname == Hostname_HPE:
        instance = "hpe"
    elif hostname == Hostname_Seattle:
        instance = "seattle"
    elif hostname == Hostname_DXC:
        instance = "dxc"
    elif hostname == Hostname_Partner:
        instance = "partner"
    elif hostname == "github-is-p.ghe.hos.hpecorp.net":
    	#the old instance was retired, so try hpe to see if we're lucky
    	instance = "hpe"

    return instance

def get_github_admin_token(instance):
    #HTTPDigestAuth(raw_input("username: "), raw_input("Password: "))
    admintoken = ""
    if instance == "hpe":
        admintoken = Admin_Token_HPE
    elif instance == "seattle":
        admintoken = Admin_Token_Seattle
    elif instance == "dxc":
        admintoken = Admin_Token_DXC
    elif instance == "partner":
        admintoken = Admin_Token_Partner
   
    return admintoken

def github_restservice(instance, data, authuser, token, operation, relativeurl):
    url = get_github_url(instance, relativeurl)
    headers = {'Content-type': 'application/json'}
   
    print("Making github rest call url: " + url + " authuser: " + authuser + " token: " + token + " operation: " + operation + " data: " + data)

    response = None
    if operation == "post":
        response = requests.post(url, auth=(authuser, token), data=data, headers=headers, proxies=proxyDict)
    elif operation == "delete":
        response = requests.delete(url, auth=(authuser, token), data=data, headers=headers, proxies=proxyDict)
    elif operation == "put":
        response = requests.put(url, auth=(authuser, token), data=data, headers=headers, proxies=proxyDict)

    #print (response.headers)
    #print (response.text)

    # For successful API call, response code will be 200 (OK)
    if response.ok:
   	    return response
    else:
        # If response code is not ok (200), print the resulting http error code with description
        response.raise_for_status()
        return None

def create_impersonation_github(instance, username):
    data =  {"scopes" : ["user"]}
    data_json = json.dumps(data)
    relativeurl = "admin/users/%s/authorizations" %(username)
    token = get_github_admin_token(instance)
    response = github_restservice(instance, data_json, Admin_Account, token, "post", relativeurl)
    jsonres = response.json()
    return jsonres["token"]

def delete_impersonation_github(instance, username):
    relativeurl = "admin/users/%s/authorizations" %(username)
    token = get_github_admin_token(instance)
    return github_restservice(instance, "", Admin_Account, token, "delete", relativeurl)

def remove_emails_github(instance, username, imptoken, emails):
    data =  emails
    data_json = json.dumps(data)
    relativeurl = "user/emails"
    return github_restservice(instance, data_json, username, imptoken, "delete", relativeurl)

def add_emails_github(instance, username, imptoken, emails):
    data =  emails
    data_json = json.dumps(data)
    relativeurl = "user/emails"
    return github_restservice(instance, data_json, username, imptoken, "post", relativeurl)