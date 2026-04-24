import requests


class OverseerrAPI:
    def __init__(self, base_url, api_key=None, email=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        self.email = email
        self.password = password

        # Auto-login om credentials finns (Seer)
        if self.email and self.password:
            self._login()

        # fallback för gamla setups (kan tas bort senare)
        self.api_key = api_key

    def _login(self):
        r = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            json={
                "email": self.email,
                "password": self.password
            }
        )

        if r.status_code != 200:
            raise Exception(f"Seer login failed: {r.text}")

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        r = self.session.request(method, url, **kwargs)

        # auto re-login om session dör
        if r.status_code == 401 and self.email and self.password:
            self._login()
            r = self.session.request(method, url, **kwargs)

        return r

    def get_status(self):
        return self._request("GET", "/api/v1/status").json()

    def get_media(self, media_type, media_id):
        return self._request(
            "GET",
            f"/api/v1/{media_type}/{media_id}"
        ).json()

    def request_media(self, media_type, media_id):
        r = self._request(
            "POST",
            "/api/v1/request",
            json={
                "mediaType": media_type,
                "mediaId": media_id
            }
        )

        if r.status_code not in [200, 201]:
            raise Exception(f"Request failed: {r.text}")

        return r.json()
