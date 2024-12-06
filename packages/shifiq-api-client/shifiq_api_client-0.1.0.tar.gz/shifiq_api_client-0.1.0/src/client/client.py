import requests

class ApiClient:
    def __init__(self, api_key: str = None, base_url: str = "https://api.shifiq.io", api_version: str = "v1") -> None:
        self.url = f"{base_url}/{api_version}"
        self.api_key = api_key

    def request(self, method: str, path: str, **kwargs) -> dict:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.request(method, f"{self.url}/{path}", headers=headers, **kwargs)
        return response.json()