from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcpnowsimilarity", version="1.0.0", description="MCP Now Similarity Service")

# Constants
NWS_API_BASE = "https://dev251734.service-now.com"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = ("myadmin", "XXXXX")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, auth=auth, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
def getKeywords(inputText: str) -> list[str]:
    """Extract keywords from the input text."""
    # Simple keyword extraction logic (can be improved with NLP libraries)
    keywords = inputText.split()
    return [keyword.strip().lower() for keyword in keywords if keyword.strip()]
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)
        return "\n---\n".join(forecasts)
@mcp.tool()
async def nowtest():
    """Test function to verify mcp is running."""
    return "Server is running and ready to handle requests!"
@mcp.tool()
async def nowtestauth():
    """Test function to verify nowauth is running with authentication."""
    url = f"{NWS_API_BASE}/api/x_146833_awesomevi/test"
    data = await make_nws_request(url)
    if not data:
        return "Unable to fetch alerts or no alerts found."
    return data
@mcp.tool()
async def nowtestauthInput(tableName: str):
    """Get ServiceNow table description for a given table."""
    """
     Args:
        tableName: table name to query (e.g. incident, user)
    """
    url = f"{NWS_API_BASE}/api/x_146833_awesomevi/test/{tableName}"
    data = await make_nws_request(url)

    if not data:
        return "Unable to fetch alerts or no alerts found."
    return data
@mcp.tool()
async def similarincidentsfortext(inputText: str):
    """Get incidents based on input text."""
    """
     Args:
        inputText: input text to search for similar incidents
    """
    keywords = getKeywords(inputText)
    for keyword in keywords:
        url = f"{NWS_API_BASE}/api/now/table/incident?sysparm_fields=number,short_description&sysparm_query=short_descriptionCONTAINS{keyword}"
        data = await make_nws_request(url)
        if data:
            return data
    if not data:
        return "Unable to fetch alerts or no alerts found."
@mcp.tool()
async def getshortdescforincident(inputincident: str):
    """Get short_description for a given incident based on input incident number."""
    """
     Args:
        inputincident: input text to search for similar incidents
    """
    keywords = getKeywords(inputincident)
    for keyword in keywords:
        url = f"{NWS_API_BASE}/api/now/table/incident?sysparm_fields=short_description&sysparm_query=number={inputincident}"
        data = await make_nws_request(url)
        if data:
            return data
    if not data:
        return "Unable to fetch alerts or no alerts found."

@mcp.tool()
async def similarincidentsforincident(inputincident: str):
    """Get similar incidents based on given incident."""
    """
     Args:
        inputText: Get short_description for a given incident based on input incident number
    """
    inputText = getshortdescforincident(inputincident)
    similarincidentsfortext(inputText)

if __name__ == "__main__":
# Initialize and run the server
    mcp.run(transport='stdio')
