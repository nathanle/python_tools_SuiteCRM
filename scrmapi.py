#!/usr/local/bin/python3
import http.client
import requests
import os.path
from urllib.parse import urlencode
import json
import time
import sys
import guid
import secrets

# OAUTH2.0 TOOL
# Evaluates remaining life left on token and rerequests when token as expired
# Designed for SuiteCRM

tm = int(time.time())
host = secrets.host
token_file = "crmtoken.txt"


def get_token(token_file):
    endpoint = "https://" + host + secrets.base + "/Api/access_token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': secrets.client_id,
        'client_secret': secrets.client_secret,
        'scope=standard': 'create standard:read standard:update standard:delete standard:delete standard:relationship:create standard:relationship:read standard:relationship:update standard:relationship:delete'
    }
    json_payload = json.dumps(payload)
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json', }
    r = requests.request("POST", endpoint, data=json_payload, headers=headers)
    data = r.json()
    print(data)
    with open(token_file, 'w') as outfile:
        ts = int(time.time())
        data['issued_at'] = ts
        json.dump(data, outfile, ensure_ascii=False)


def open_token(token_file):
    if (os.path.exists(token_file)):
        with open(token_file) as json_file:
            json_data = json.load(json_file)
            return json_data
    else:
        state = "failed"
        return state


expires_in = 3599
#get_token(token_file)
json_data = open_token(token_file)
#print(json_data)
if (json_data == "failed"):
    get_token(token_file)
    json_data = open_token(token_file)
issued_int = int(json_data["issued_at"])  # epoch time bearer token was issued
print(str(tm-issued_int) + "-" + str(expires_in))
if ((tm-issued_int) > expires_in):
    get_token(token_file)
    json_data = open_token(token_file)
#    print("Token refreshed.")
token = json_data["access_token"]
#print(token)

##############################################
# END OF TOKEN MANAGEMENT                    #
##############################################

def api(method, endpoint, headers, payload):
    print(endpoint)
    if payload == None:
        r = requests.request(method, endpoint, headers=headers)
    else:
        r = requests.request(method, endpoint, headers=headers, data=payload)
    data = r.json()
    return data


def get_data(rqtype, crmid):
    endpoint = "https://" + host + secrets.base + "/Api/V8/module/{0}/{1}".format(rqtype, crmid)
    print(endpoint)
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    method = "GET"
    payload = None
    data = api(method, endpoint, headers, payload)
    return data


def add_data(data):
    endpoint = secrets.base + "/Api/V8/module"
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    method = "POST"
    data = api(method, endpoint, headers, data)
    with open('createproperties.log', 'a') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    return data 

def patch(data):
    endpoint = secrets.base + "/Api/V8/module"
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    method = "PATCH"
    data = api(method, endpoint, headers, data)
    with open('patchproperties.log', 'a') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    return data 

def add_relationship(modulename, parentid, data):
    endpoint = secrets.base + "/Api/V8/module/{0}/{1}/relationships".format(modulename, parentid)
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    method = "POST"
    data = api(method, endpoint, headers, data)
    with open('create_relationships.log', 'a') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    conn.close()
    return data 

if __name__ == "__main__":
    data = (get_data("props_NewEntry", "8e9c2aef-1555-b3a8-d13b-5d488f2f3057"))
    print(json.dumps(data, indent=4))
# create_account(json_data["access_token"])
# create_properties()
