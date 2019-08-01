#!/usr/local/bin/python3
import http.client
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
    conn = http.client.HTTPSConnection(host)
    payload = {
        'grant_type': 'client_credentials',
        'client_id': secrets.client_id,
        'client_secret': secrets.client_secret,
        'scope=standard': 'create standard:read standard:update standard:delete standard:delete standard:relationship:create standard:relationship:read standard:relationship:update standard:relationship:delete'
    }
    json_payload = json.dumps(payload)
    endpoint = secrets.base + "/Api/access_token"
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json', }
    conn.request("POST", endpoint, json_payload, headers)
    conn.set_debuglevel(1)
    res = conn.getresponse()
    data = res.read()
    decode = json.loads((data.decode("utf-8")))
    print(decode)
    with open(token_file, 'w') as outfile:
        ts = int(time.time())
        decode['issued_at'] = ts
        json.dump(decode, outfile, ensure_ascii=False)


def open_token(token_file):
    if (os.path.exists(token_file)):
        with open(token_file) as json_file:
            json_data = json.load(json_file)
            return json_data
    else:
        state = "failed"
        return state


expires_in = 3599
json_data = open_token(token_file)
#print(json_data)
if (json_data == "failed"):
    get_token(token_file)
    json_data = open_token(token_file)
issued_int = int(json_data["issued_at"])  # epoch time bearer token was issued
if ((tm-issued_int) > expires_in):
    get_token(token_file)
    json_data = open_token(token_file)
#    print("Token refreshed.")
token = json_data["access_token"]
#print(token)

##############################################
# END OF TOKEN MANAGEMENT                    #
##############################################


def get_data(rqtype):
    if (rqtype == "Accounts"):
        params = urlencode({'fields[Accounts]': 'name,account_type'})
        name = "Accounts"
    if (rqtype == "Properties"):
        params = urlencode({'fields[props_Properties]': 'name,account_type'})
        name = "props_Properties"
    endpoint = secrets.base + "/Api/V8/module/" + name
    conn = http.client.HTTPSConnection(host)
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    conn.request("GET", endpoint, params, headers)
    res = conn.getresponse()
    data = res.read()
    decode = json.loads((data.decode("utf-8")))
    conn.close()
    return decode


def add_data(data):
    conn = http.client.HTTPSConnection(host)
    payload = json.dumps(data)
    endpoint = secrets.base + "/Api/V8/module"
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    conn.request("POST", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    decode = json.loads((data.decode("utf-8")))
    with open('createproperties.log', 'a') as outfile:
        json.dump(decode, outfile, indent=4, ensure_ascii=False)
    conn.close()
    return decode
def patch(data):
    conn = http.client.HTTPSConnection(host)
    payload = json.dumps(data)
    endpoint = secrets.base + "/Api/V8/module"
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }

    conn.request("PATCH", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    decode = json.loads((data.decode("utf-8")))
    with open('patchproperties.log', 'a') as outfile:
        json.dump(decode, outfile, indent=4, ensure_ascii=False)
    conn.close()
    return decode
def add_relationship(modulename, parentid, data):
    conn = http.client.HTTPSConnection(host)
    payload = json.dumps(data)
    endpoint = secrets.base + "/Api/V8/module/{0}/{1}/relationships".format(modulename, parentid)
    print(json.dumps(data, indent=4))
    headers = {
        'Content-type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': "Bearer " + token
    }
    conn.request("POST", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    decode = json.loads((data.decode("utf-8")))
    with open('create_relationships.log', 'a') as outfile:
        json.dump(decode, outfile, indent=4, ensure_ascii=False)
    conn.close()
    return decode

if __name__ == "__main__":
    print(get_data("Accounts"))
# create_account(json_data["access_token"])
# create_properties()
