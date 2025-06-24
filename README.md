# ServiceNowMCPServer
ServiceNow MCP Server
Installing Claude desktop
 
Create your own ServiceNow MCP Server
Testing authentication
Prompt: Test function to verify nowauth is running with authentication.
Endpoint: GET https://dev251734.service-now.com/api/x_146833_awesomevi/test
 
Testing with an input parameter
Endpoint: GET https://dev251734.service-now.com/api/x_146833_awesomevi/test/{table_name}
Prompt: Get ServiceNow table description for a given table.
 
 
Testing with OOB APIs
Get short description for a given incident
Endpoint: GET https://dev251734.service-now.com/api/now/table/incident?sysparm_fields=short_description&sysparm_query=number={inputincident}
Prompt: Get short_description for a given incident based on input incident number INC0008001

 

Similar incidents for a given incident 
 
 
 
 
 
