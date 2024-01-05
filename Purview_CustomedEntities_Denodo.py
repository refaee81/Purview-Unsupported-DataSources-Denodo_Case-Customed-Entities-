
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:42:00 2023

@author: abdera
"""


############################## Credentials 
"""
I stored my credentials in external file ... you can use whatever authentication method that suits your environment or IDE
for authentication methods, visit: https://learn.microsoft.com/en-us/dotnet/azure/sdk/authentication/local-development-service-principal?tabs=azure-portal%2Cwindows%2Ccommand-line
I used (ClientSecretCredential)
"""


exec(open(r'C:\....... \spn.py').read())


############################ Libraries 
import subprocess
import pandas as pd
import decimal
import numpy as np
import xlsxwriter
import json
import os
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from pyapacheatlas.core import AtlasAttributeDef, EntityTypeDef, RelationshipTypeDef
from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.readers import ExcelReader
from pyapacheatlas.scaffolding import column_lineage_scaffold
from json import loads, dumps
from pyapacheatlas.readers.reader import Reader, ReaderConfiguration
from collections import OrderedDict
import re
from pyapacheatlas.core.util import GuidTracker,AtlasException
from pandas import DataFrame, concat
from openpyxl import Workbook
from openpyxl import load_workbook
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader

############################ 
#                                       Denodo CATALOG_METADATA_VIEWS
###########################


import psycopg2 as dbdriver
from socket import gethostname
denodoserver_name = "xxxxx-xxx-xxx-xx-xxxxxx"
denodoserver_odbc_port = "xxxxx-xxx-xxx-xx-xxxxxx"
denodoserver_database = "xxxxx-xxx-xxx-xx-xxxxxx"
denodoserver_uid = "xxxxx-xxx-xxx-xx-xxxxxx"
denodoserver_pwd = "xxxxx-xxx-xxx-xx-xxxxxx"

## Create the useragent as the concatenation of
## the client hostname and the python library used
client_hostname = gethostname()

useragent = "%s-%s" % (dbdriver.__name__,client_hostname)

## Establishing a connection
cnxn_str = "user=%s password=%s host=%s dbname=%s port=%s" %\
       (denodoserver_uid, denodoserver_pwd, denodoserver_name, denodoserver_database, denodoserver_odbc_port)

cnxn = dbdriver.connect(cnxn_str)

## Query to be sent to the Denodo VDP Server
query = "SELECT database_name, view_name, column_name, column_type_name, column_type_length \
FROM CATALOG_METADATA_VIEWS()"

## Define a cursor and execute the results
cur = cnxn.cursor()

cur.execute(query)

## Finally fetch the results. `results` is a list of lists.
## If you don't want to load all the records in memory, you may
## want to use cur.fetchone() or cur.fetchmany()

results = cur.fetchall()

##### Get the column names from the cursor
columns = [c[0] for c in cur.description]

##### Get the data in 'results' into a Pandas dataframe, sort it, and reindex it 
CATALOG_METADATA_VIEWS = pd.DataFrame.from_records(results,columns = columns)

CATALOG_METADATA_VIEWS_X = CATALOG_METADATA_VIEWS


CATALOG_METADATA_VIEWS20 = CATALOG_METADATA_VIEWS


############################## Query Purview Collections 

Collection_List = Colclient.list_collections(only_names=True, pprint=True)

############################## Create Collection 
# Create a collection hierarchy

#Colclient.create_collections(start_collection="Enterprise", collection_names="Denodo")

##################### Create the template for entities : automate using excel 
"""
Below is a complex udf that does the following: 
1. Reads the unique names of Denodo tables and creates a list for them. 
2. Sets a qualifiedName for each asset of Denodo by concatenating asset name, type and schema. The qualifiedNames are crucial for building up relationships and heirarchies in Purview.
3. Loop the creation of qualifiedName, typeName, and asset type (db2 in this case) for each dataset by creating a data frame and appending eventually all data frames in a list of dataframes. 
4. Storing the data of appended dataframe in a temporary file that has the "upload template" structure, and then uploading the entities individually. The temp file stores and deletes for each step (dataframe) causing no storage or capacity issues.
5. loop the creation of a collection based on the unique denodo data set under the parent collection "Denodo" using the collectionId. 
6. For each collection, upload and dump the entities to build up the right heirarchy. 
7. To avoid the expiration of the access token (3600 / 1 hr), I break down the Catalog dataframe into batches of 200 entities, and run authentication at each batch. 

"""

###### UDF & Upload



def denodo_collections(df):


    tables=df.view_name.unique()  ### break it into multiple dataframes of each table/view
    dfs=[]
    for i, table in enumerate(tables):
    
        df_i= df.loc[df['view_name']==table].copy()
        
        df_i['qualifiedName'] = "pyapacheatlas://"+ df_i.database_name + "#" + df_i.view_name + "#" + df_i.column_name
        d1 = df_i.drop(columns=['view_name', 'column_type_length'], axis=1)
        d1['database_name'] = 'db2_table_column'
        d1.rename(columns={'database_name': 'typeName', 'column_name': 'name', 'column_type_name':'type'}, inplace=True)
        d1['[Relationship] table'] = "pyapacheatlas://"+ df_i.database_name + "#" + df_i.view_name
        d1[['typeName','name', 'qualifiedName','[Relationship] table' , 'type']]
        
        df_i['qualifiedName'] = "pyapacheatlas://"+ df_i.database_name + "#" + df_i.view_name
        d2 = df_i.drop(columns=['column_name', 'column_type_length'], axis=1)
        d2 = d2.drop_duplicates()
        d2['database_name'] = 'db2_table'
        d2['column_type_name']  = ''
        d2.rename(columns={'database_name': 'typeName', 'view_name': 'name', 'column_type_name':'type'}, inplace=True)
        d2['[Relationship] table'] = ""
        d2[['typeName','name', 'qualifiedName','[Relationship] table' , 'type']]
        
        d3 = df_i.drop(columns=['qualifiedName', 'view_name', 'column_name', 'column_type_name', 'column_type_length'], axis=1)
        d3 = d3.drop_duplicates()
        d3['qualifiedName'] = "pyapacheatlas://"+ df_i.database_name 
        d3['typeName'] = 'DataSet'
        d3['type'] =''
        d3.rename(columns={'database_name': 'name'}, inplace=True)
        d3['[Relationship] table'] = ""
        d3[['typeName','name', 'qualifiedName','[Relationship] table' , 'type']]
        
        df_i = pd.concat([d3, d2, d1], ignore_index=True, axis=0)
        df_i = df_i[['typeName','name', 'qualifiedName','[Relationship] table' , 'type']]
    
        
        dfs.append(df_i)
        for i, df_i in enumerate(dfs):
            
            file_path = "C:/Users/..../demo_bulk_entities_upload2.xlsx"
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df_i.to_excel(writer, sheet_name='BulkEntities', index=False)
            writer.close()
            
            
            
            excel_config = ExcelConfiguration()
            excel_reader = ExcelReader(excel_config)
            entities = excel_reader.parse_bulk_entities(file_path)
            results = client.upload_entities(entities)
            print(json.dumps(results, indent=2))
            #create a sub collection for denodo dataset
            Colclient.create_collections(start_collection="Denodo",
                                      collection_names= df_i['name'][0])
            entityGuids = list(results['guidAssignments'].values())
            
            for i in enumerate(entityGuids):
                Collection_List = Colclient.list_collections()
                z = next((item for item in Collection_List if item["friendlyName"] == df_i['name'][0]), None)
                collectionid = z['name']
                url = 'https://{purview catalog name}.purview.azure.com/datamap/api/entity/moveTo?collectionId='+collectionid+'&api-version=2023-09-01'
                headers = {
                            'Authorization': f'Bearer {azuread_access_token}',
                            'Content-Type': 'application/json'
                            }     
                payload=    json.dumps({
                                    "entityGuids": entityGuids
    
                                        }) 
                response = requests.request("POST", url, headers=headers, data=payload, timeout=None, verify=False)  
                
#### Batch   
n = 200 #rows
CATALOG_METADATA_VIEWS30 = [CATALOG_METADATA_VIEWS[i:i+n] for i in range(0,len(CATALOG_METADATA_VIEWS),n)]


x = 0 
for x in range(len(CATALOG_METADATA_VIEWS30)):
    denodo_collections(CATALOG_METADATA_VIEWS30[x])
    exec(open(r'C:\Users\.......\spn.py').read())
    x +=1

    
    




































