from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# -----------------------------
# MCP SERVER INIT
# -----------------------------
mcp = FastMCP("mcpnowsimilarity")

# -----------------------------
# SERVICENOW CONFIG
# -----------------------------
INSTANCE_URL = " https://dev211849.service-now.com "
USERNAME = "admin"
PASSWORD = " iiI-E2@8ijOZ "

# -----------------------------
# COMMON REQUEST FUNCTION
# -----------------------------
async def make_sn_request(url: str) -> dict[str, Any] | None:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (USERNAME, PASSWORD)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, auth=auth, headers=headers, timeout=30)
            print("STATUS:", response.status_code)
            print("URL:", url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("ERROR:", e)
            return None

# -----------------------------
# UTILITY
# -----------------------------
def get_keywords(text: str) -> list[str]:
    return [word.lower() for word in text.split() if word.strip()]

# -----------------------------
# MCP TOOLS
# -----------------------------

@mcp.tool()
async def nowtest():
    """Basic MCP server test"""
    return "Server is running and ready!"

@mcp.tool()
async def nowtestauth():
    """Verify ServiceNow authentication"""
    url = f"{INSTANCE_URL}/api/now/table/incident?sysparm_limit=1"
    data = await make_sn_request(url)
    if not data:
        return "Auth failed or instance not reachable"
    return "Authentication successful"

@mcp.tool()
async def nowtestauthInput(tableName: str):
    """Get sample data from any ServiceNow table"""
    url = f"{INSTANCE_URL}/api/now/table/{tableName}?sysparm_limit=1"
    data = await make_sn_request(url)
    if not data:
        return f"Unable to access table: {tableName}"
    return data

@mcp.tool()
async def similarincidentsfortext(inputText: str):
    """Find incidents using keywords in short_description"""
    keywords = get_keywords(inputText)

    for keyword in keywords:
        url = (
            f"{INSTANCE_URL}/api/now/table/incident"
            f"?sysparm_fields=number,short_description"
            f"&sysparm_query=short_descriptionCONTAINS{keyword}"
        )
        data = await make_sn_request(url)
        if data and data.get("result"):
            return data["result"]

    return "No similar incidents found"

@mcp.tool()
async def getshortdescforincident(incidentNumber: str):
    """Get short description for a given incident number"""
    url = (
        f"{INSTANCE_URL}/api/now/table/incident"
        f"?sysparm_fields=short_description"
        f"&sysparm_query=number={incidentNumber}"
    )
    data = await make_sn_request(url)

    if data and data.get("result"):
        return data["result"][0]["short_description"]

    return None

@mcp.tool()
async def similarincidentsforincident(incidentNumber: str):
    """Find incidents similar to a given incident"""
    short_desc = await getshortdescforincident(incidentNumber)

    if not short_desc:
        return f"Incident {incidentNumber} not found"

    return await similarincidentsfortext(short_desc)

# -----------------------------
# RUN MCP SERVER
# -----------------------------
if _name_ == "_main_":
    mcp.run(transport="stdio")
