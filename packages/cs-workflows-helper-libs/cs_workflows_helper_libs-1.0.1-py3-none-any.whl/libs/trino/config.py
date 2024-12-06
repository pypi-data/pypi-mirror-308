"""Trino config."""
from pydantic_settings import BaseSettings

from libs.service_account.config import ServiceAccountConfig


class TrinoConfig(BaseSettings):
    """A class for Trino related settings."""

    url: str
    port: int = 443
    http_scheme: str = "https"
    oidc: ServiceAccountConfig

    class Config:
        """Trino settings config."""

        env_prefix = "TRINO_"
        env_nested_delimiter = "__"
