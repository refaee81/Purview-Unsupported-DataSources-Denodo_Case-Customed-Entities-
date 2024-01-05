# Purview_ScanUnsupportedDataSource-Denodo_Case-
This solution is designed and implemented for the purpose of enabling purview scanning unregistered/unsupported data sources. The process is built using different REST API requests as well as python loops to read external sources, and replicate exisiting assets by building customed entities. This case is for Denodo as purview unsupported platform.
# The solution entails three main process: 
1. Query Denodo Catalog and building up Catalog Views DataFrame.
2. Building a Denodo Customed Data Source and/or a Denodo Collection in Purivew.
3. Buidling up Denodo Entities, Schemas, and Heirarchies in Purview.  
