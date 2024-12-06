import httpx
from typing import Optional, Dict, Any

class SpmHrisClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            "Authorization": f"token {api_key}:{api_secret}" if api_key and api_secret else ""
        }

    # Synchronous methods
    def get_doc(self, doctype: str, docname: str) -> Dict[str, Any]:
        """Fetches a single document by type and name (synchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        with httpx.Client(headers=self.headers) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def create_doc(self, doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new document in Frappe (synchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}"
        with httpx.Client(headers=self.headers) as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    def update_doc(self, doctype: str, docname: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing document (synchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        with httpx.Client(headers=self.headers) as client:
            response = client.put(url, json=data)
            response.raise_for_status()
            return response.json()

    def delete_doc(self, doctype: str, docname: str) -> Dict[str, Any]:
        """Deletes a document by type and name (synchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        with httpx.Client(headers=self.headers) as client:
            response = client.delete(url)
            response.raise_for_status()
            return response.json()

    # Asynchronous methods
    async def async_get_doc(self, doctype: str, docname: str) -> Dict[str, Any]:
        """Fetches a single document by type and name (asynchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def async_create_doc(self, doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new document in Frappe (asynchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def async_update_doc(self, doctype: str, docname: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing document (asynchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.put(url, json=data)
            response.raise_for_status()
            return response.json()

    async def async_delete_doc(self, doctype: str, docname: str) -> Dict[str, Any]:
        """Deletes a document by type and name (asynchronous)."""
        url = f"{self.base_url}/api/resource/{doctype}/{docname}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.delete(url)
            response.raise_for_status()
            return response.json()
