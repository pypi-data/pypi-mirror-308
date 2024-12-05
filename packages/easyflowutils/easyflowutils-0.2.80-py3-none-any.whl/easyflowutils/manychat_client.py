from typing import Any, Dict, List, Optional, Union
import requests


class ManyChatClient:
    """A Python client for the ManyChat API."""

    BASE_URL = "https://api.manychat.com"
    SUBSCRIBER_URL = f"{BASE_URL}/fb/subscriber"
    PAGE_URL = f"{BASE_URL}/fb/page"
    SENDING_URL = f"{BASE_URL}/fb/sending"

    def __init__(self, api_key: str):
        """
        Initialize the ManyChat client.

        Args:
            api_key (str): Your ManyChat API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(
            self,
            method: str,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request to the ManyChat API."""
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params
        )

        response.raise_for_status()
        return response.json()

    # Subscriber Methods
    def get_subscriber_info(self, subscriber_id: int) -> Dict[str, Any]:
        """Get information about a specific subscriber."""
        url = f"{self.SUBSCRIBER_URL}/getInfo"
        return self._make_request("GET", url, params={"subscriber_id": subscriber_id})

    def find_subscriber_custom_field(self, field_id: int, value: Any) -> Dict[str, Any]:
        """Find a subscriber by a custom field."""
        url = f"{self.SUBSCRIBER_URL}/findByCustomField"
        params = {"field_id": field_id, "value": value}
        return self._make_request("GET", url, params=params)

    def find_subscriber_by_system_field(self, email: Optional[str] = None, phone: Optional[str] = None) -> Dict[
        str, Any]:
        """Get a subscriber by email or phone number."""
        url = f"{self.SUBSCRIBER_URL}/findBySystemField"
        params = {}
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
        return self._make_request("GET", url, params=params)


if __name__ == '__main__':
    client = ManyChatClient('979425:e5c3b09a7323f6b34ade643ff18c0906')
    subscriber_info = client.get_subscriber_info(1104679673)
    user_by_system = client.find_subscriber_by_system_field(phone='972528393372')
    val = 1
