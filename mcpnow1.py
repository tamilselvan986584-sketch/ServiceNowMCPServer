from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("mcpnowsimilarity", version="1.0.0", description="MCP ServiceNow Integration")

# ✅ Your ServiceNow instance
INSTANCE_URL = "https://dev211849.service-now.com"
USERNAME = "admin"
PASSWORD = "iiI-E2@8ijOZ"

# -------------------------------
# Common API Request Function
# -------------------------------
async def make_request(url: str) -> dict[str, Any] | None:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                auth=(USERNAME, PASSWORD),
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# -------------------------------
# Utility Function
# -------------------------------
def getKeywords(inputText: str) -> list[str]:
    return [word.lower() for word in inputText.split() if word.strip()]

# -------------------------------
# MCP Tools
# -------------------------------

@mcp.tool()
async def nowtest():
    """Test MCP server"""
    return "✅ MCP Server is running!"

@mcp.tool()
async def nowtestauth():
    """Test ServiceNow connection"""
    url = f"{INSTANCE_URL}/api/now/table/incident?sysparm_limit=1"
    return await make_request(url)

@mcp.tool()
async def nowtestauthInput(tableName: str):
    """Fetch any ServiceNow table data"""
    url = f"{INSTANCE_URL}/api/now/table/{tableName}?sysparm_limit=5"
    return await make_request(url)

@mcp.tool()
async def similarincidentsfortext(inputText: str):
    """Find similar incidents using keywords"""
    keywords = getKeywords(inputText)

    results = []
    for keyword in keywords:
        url = f"{INSTANCE_URL}/api/now/table/incident?sysparm_fields=number,short_description&sysparm_query=short_descriptionCONTAINS{keyword}"
        data = await make_request(url)

        if data and "result" in data:
            results.extend(data["result"])

    if not results:
        return "No similar incidents found."

    return results

@mcp.tool()
async def getshortdescforincident(inputincident: str):
    """Get short description of an incident"""
    url = f"{INSTANCE_URL}/api/now/table/incident?sysparm_query=number={inputincident}&sysparm_fields=short_description"
    
    data = await make_request(url)

    if data and data.get("result"):
        return data["result"][0]["short_description"]

    return "Incident not found."

@mcp.tool()
async def similarincidentsforincident(inputincident: str):
    """Find similar incidents based on an incident number"""

    # ✅ FIX: await required
    short_desc = await getshortdescforincident(inputincident)

    if isinstance(short_desc, str):
        return await similarincidentsfortext(short_desc)

    return "Unable to find similar incidents."

# -------------------------------
# Run MCP Server
# -------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
