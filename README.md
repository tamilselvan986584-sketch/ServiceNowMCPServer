# ServiceNowMCPServer
ServiceNow MCP Server
**Installing Claude desktop**
 ![image](https://github.com/user-attachments/assets/0b62b5db-4ec3-4b76-bb54-03366beea510)

**Create your own ServiceNow MCP Server**
_Testing authentication_
Prompt: Test function to verify nowauth is running with authentication.
Endpoint: GET https://dev251734.service-now.com/api/x_146833_awesomevi/test
![image](https://github.com/user-attachments/assets/6eb6a035-0186-4874-a4b2-2784407afcb1)

 
_Testing with an input parameter_
Endpoint: GET https://dev251734.service-now.com/api/x_146833_awesomevi/test/{table_name}
Prompt: Get ServiceNow table description for a given table.
![image](https://github.com/user-attachments/assets/2d8c18c6-5332-4c7b-a796-690d8436a31c)
![image](https://github.com/user-attachments/assets/01a4c774-b7f4-4c0e-b5e5-f4a2a0ba5fdd)


 
 
_Testing with OOB APIs_
**_Get short description for a given incident_**
Endpoint: GET https://dev251734.service-now.com/api/now/table/incident?sysparm_fields=short_description&sysparm_query=number={inputincident}
Prompt: Get short_description for a given incident based on input incident number INC0008001
![image](https://github.com/user-attachments/assets/279e9d4f-8f83-444f-9a65-44231028bfcd)

 

**_Similar incidents for a given incident _**
![image](https://github.com/user-attachments/assets/8de32510-40c3-4da0-996b-92a1fb75ac14)
![image](https://github.com/user-attachments/assets/b2292fbe-71aa-4ffd-bc11-e1abbb104e8b)
![image](https://github.com/user-attachments/assets/4251d28e-d543-4009-83e8-696f70ee4bf1)
![image](https://github.com/user-attachments/assets/87cf0c42-a5b7-4540-a675-ac9e9b7398ed)
![image](https://github.com/user-attachments/assets/a4c94ad4-ba39-47f1-b723-c188a8978b2b)




 
 
 
 
 
