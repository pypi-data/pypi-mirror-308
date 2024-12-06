"""Generic service account config."""
from pydantic import validator
from pydantic_settings import BaseSettings


class ServiceAccountConfig(BaseSettings):
    """A class for OIDC settings."""

    type: str = "service_account"
    universe_domain: str = "googleapis.com"
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    token_uri: str = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"

    @validator("private_key", pre=True)
    def replace_newlines(cls, value):
        """Convert keys passed as a single line into a multiline string."""
        return value.replace("\\n", "\n")
