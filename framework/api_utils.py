import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def create_test_user(self, email, password):
        """Quickly creates a user so the mobile test can log in immediately."""
        payload = {"email": email, "password": password}
        response = self.session.post(f"{self.base_url}/api/v1/users", json=payload)
        response.raise_for_status()
        return response.json()