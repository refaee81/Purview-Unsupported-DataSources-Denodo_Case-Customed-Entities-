
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:42:00 2023

@author: abdera


This is an example of authentication file used for the work 

"""


tenant_id = "xxxxx-xxx-xxx-xx-xxxxxx"
client_id = "xxxxx-xxx-xxx-xx-xxxxxx"
scope_name = "xxxxx-xxx-xxx-xx-xxxxxx"
client_secret_secret_name = "xxxxx-xxx-xxx-xx-xxxxxx"

 
## Microsoft Purview
data_catalog_name = "xxxxx-xxx-xxx-xx-xxxxxx"  # Purview Account Name

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
import os

Endpoint = f"https://{data_catalog_name}.purview.azure.com"
resource_url = "https://purview.azure.net"
 
client_secret = "xxxxx-xxx-xxx-xx-xxxxxx"

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
import os

clientSecret = "xxxxx-xxx-xxx-xx-xxxxxx"

auth = ServicePrincipalAuthentication(
    client_id="xxxxx-xxx-xxx-xx-xxxxxx", client_secret=clientSecret, tenant_id="xxxxx-xxx-xxx-xx-xxxxxx"
)


client = PurviewClient('pview-dap-dev-001',auth, requests_verify=False)


#################################
import subprocess
import requests

def azuread_auth(tenant_id: str, client_id: str, client_secret: str, resource_url: str):
    """
      Authenticates Service Principal to the provided Resource URL, and returns the OAuth Access Token
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    payload= f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource={resource_url}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_token = json.loads(response.text)['access_token']
    return access_token

    



def purview_auth(tenant_id: str, client_id: str, client_secret: str, data_catalog_name: str):
    """
      Authenticates to Atlas Endpoint and returns a client object
    """
    oauth = ServicePrincipalAuthentication(
        tenant_id = tenant_id,
        client_id = client_id,
        client_secret = client_secret
    )
    client = PurviewClient(
      account_name = data_catalog_name,
      authentication = oauth,
      requests_verify=False
    )
    return client


azuread_access_token = azuread_auth(tenant_id, client_id, clientSecret, resource_url)
purview_client = purview_auth(tenant_id, client_id, clientSecret, data_catalog_name) 


##################################################


from purviewautomation import (ServicePrincipalAuthentication,
                                PurviewCollections)

auth = ServicePrincipalAuthentication(tenant_id=tenant_id,
                                      client_id=client_id,
                                      client_secret=client_secret)

Colclient = PurviewCollections(purview_account_name="pview-dap-dev-001",
                            auth=auth)

###################################################


denodoserver_uid = "xxxxx-xxx-xxx-xx-xxxxxx"
denodoserver_pwd = "xxxxx-xxx-xxx-xx-xxxxxx"

















