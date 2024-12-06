"""Trino client."""

from google.auth.transport import requests
from google.oauth2 import service_account
from trino.auth import JWTAuthentication
from trino.dbapi import connect

from libs.trino.config import TrinoConfig


class TrinoClient:
    """Wrapper around the Trino client."""

    def __init__(self):
        """Initialize Trino client."""
        self.config = TrinoConfig()

    def get_service_account_token(self):
        """Retrieve a token using the service account."""
        service_account_dict = self.config.oidc.model_dump()
        credentials = service_account.Credentials.from_service_account_info(
            service_account_dict, scopes=["openid", "email"]
        )
        credentials.refresh(requests.Request())
        return credentials.token

    def connect(self):
        """Connect to Trino."""
        token = self.get_service_account_token()
        return connect(
            host=self.config.url,
            port=self.config.port,
            http_scheme=self.config.http_scheme,
            auth=JWTAuthentication(token),
            verify=True,
        )
