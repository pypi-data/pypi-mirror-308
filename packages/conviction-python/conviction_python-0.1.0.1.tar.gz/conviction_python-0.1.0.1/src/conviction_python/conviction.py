"""
Core functionality of conviction-python
"""

import requests
import aiohttp
from typing import Dict, Any

def run_tool(tool_uuid: str, api_key: str) -> Dict[str, Any]:
    """
    Run a tool with the given tool UUID and API key.
    
    Args:
        tool_uuid: The UUID of the tool to run
        api_key: API key for authentication
    
    Returns:
        Dict containing the API response
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    headers = {
        "X-API-KEY": f"{api_key}",
        "accept": "application/json"
    }

    base_url = "https://api.convictionai.io/api/v1"
    
    url = f"{base_url}/tool/run/{tool_uuid}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json() 

async def run_tool_async(tool_uuid: str, api_key: str) -> Dict[str, Any]:
    """
    Run a tool with the given tool UUID and API key asynchronously.
    
    Args:
        tool_uuid: The UUID of the tool to run
        api_key: API key for authentication
        
    Returns:
        Dict containing the API response
        
    Raises:
        aiohttp.ClientError: If the request fails
    """
    headers = {
        "X-API-KEY": f"{api_key}",
        "accept": "application/json"
    }

    base_url = "https://api.convictionai.io/api/v1"
    url = f"{base_url}/tool/run/{tool_uuid}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()