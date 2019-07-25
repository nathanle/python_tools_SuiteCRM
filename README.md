# python_tools_SuiteCRM

**guid.py** - This creates Id numbers in the SuiteCRM format. I based this on the guid.php file that comes with SuiteCRM

**scrmapi.py** - This is the module for interfacing with the SuiteCRM API. I have used this to add over 50K records without any issues, but it does not do token refresh handling and I plan to add that. Instead, it requests a new token when the old one expires, and this is not the best way to do this as you wind up with a lot of old tokens in your records. 

Also, get_data function is not mature as I really only used it to prove it worked. I have been doing all my searches directly against the database.

It requires a secrets.py file with the following:
```
#!/usr/local/bin/python3 #Or whatever your python3 path is.

host = "hostname"
client_secret = "client secret password"
client_id = "token"
token_endpoint = "/<SuiteCRM_Install_Directory>/Api/access_token"
get_endpoint = "/<SuiteCRM_Install_Directory>/Api/V8/module/"
post_endpoint = "/<SuiteCRM_Install_Directory>/Api/V8/module"
```

**I will be adding my CSV parser for importing SF data into SCRM in a few days**
