# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:56:57 2023

@author: abdera
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:42:00 2023

@author: abdera
"""
#Ref: https://github.com/Ludwinic1/purviewautomation
#pip install purviewautomation


tenant_id = "d4167d58-713e-4e8f-8ba2-869b5491fb80"
client_id = "29a0dcca-e5c6-4dfd-9bac-740e5c0fcf14"
scope_name = "kv-001-secrets"
client_secret_secret_name = "app-dap-purview-dev"
# tenant_id_secret_name = "..."
# client_id_secret_name = "..."
 
## Microsoft Purview
data_catalog_name = "pview-dap-dev-001"  # Purview Account Name

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
import os

Endpoint = f"https://{data_catalog_name}.purview.azure.com"
resource_url = "https://purview.azure.net"
 
client_secret = "c345828a-0bae-4973-b9dc-372398abe3ae"

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json
import os

clientSecret = "Utd8Q~-zg0f2g3qVSCQK.SVhktn1kKLdXmqkhaZy"

auth = ServicePrincipalAuthentication(
    client_id='29a0dcca-e5c6-4dfd-9bac-740e5c0fcf14', client_secret=clientSecret, tenant_id='d4167d58-713e-4e8f-8ba2-869b5491fb80'
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
client_id = '29a0dcca-e5c6-4dfd-9bac-740e5c0fcf14'
client_secret = "Utd8Q~-zg0f2g3qVSCQK.SVhktn1kKLdXmqkhaZy"
tenant_id = 'd4167d58-713e-4e8f-8ba2-869b5491fb80'

from purviewautomation import (ServicePrincipalAuthentication,
                                PurviewCollections)

auth = ServicePrincipalAuthentication(tenant_id=tenant_id,
                                      client_id=client_id,
                                      client_secret=client_secret)

Colclient = PurviewCollections(purview_account_name="pview-dap-dev-001",
                            auth=auth)

###################################################


denodoserver_uid = "abdera"
denodoserver_pwd = "991090Ramzi!!"

















