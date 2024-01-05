# Purview_ScanUnsupportedDataSource-Denodo_Case-
This solution is designed and implemented for the purpose of enabling purview scanning unregistered/unsupported data sources. The process is built using different REST API requests as well as python loops to read external sources, and replicate exisiting assets by building customed entities. This case is for Denodo as purview unsupported platform.

# The solution entails three main processes: 
1. Query Denodo Catalog and building up Catalog Views DataFrame.
2. Building a Denodo Customed Data Source and/or a Denodo Collection in Purivew using REST API.
3. Buidling up Denodo Entities, Schemas, and Heirarchies in Purview using REST API.  


![image](https://github.com/refaee81/Purview_ScanUnsupportedDataSource-Denodo_Case-/assets/48224520/7f083d96-3fb9-41f9-ae35-2ac66e39731c)


![image](https://github.com/refaee81/Purview_ScanUnsupportedDataSource-Denodo_Case-/assets/48224520/8d70249f-55e7-45f6-8cb4-cf4c5de5ed64)


![image](https://github.com/refaee81/Purview_ScanUnsupportedDataSource-Denodo_Case-/assets/48224520/95490c60-4768-452e-8b06-49a48c743c77)


![image](https://github.com/refaee81/Purview_ScanUnsupportedDataSource-Denodo_Case-/assets/48224520/8e76846d-0835-4595-a212-d2f989a6533b)

Note: Screenshots have been adjusted to remove names of assets. 

# Key References:
1. Denodo: https://community.denodo.com/docs/html/browse/6.0/vdp/vql/stored_procedures/predefined_stored_procedures/catalog_metadata_views
2. Denodo: https://community.denodo.com/docs/html/browse/8.0/en/vdp/data_catalog_up_to_update_20210209/appendix/rest_api/rest_api
3. Denodo: https://community.denodo.com/kb/en/view/document/How%20to%20connect%20to%20Denodo%20from%20Python%20-%20a%20starter%20for%20Data%20Scientists
4. Microsoft: https://learn.microsoft.com/en-us/purview/create-entities?tabs=classic-portal
5. Microsoft: https://learn.microsoft.com/en-us/purview/concept-best-practices-asset-lifecycle
6. Github: https://github.com/wjohnson/pyapacheatlas/tree/master/samples/CRUD
7. Atlas API: https://atlas.apache.org/api/v2/index.html
8. https://datasmackdown.com/oss/pyapacheatlas/custom-types.html
