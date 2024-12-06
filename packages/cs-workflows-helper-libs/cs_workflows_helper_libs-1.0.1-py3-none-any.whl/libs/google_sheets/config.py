"""GoogleSheets config."""
from pydantic_settings import BaseSettings

from libs.service_account.config import ServiceAccountConfig


class GoogleSheetsConfig(BaseSettings):
    """A class for GoogleSheets related settings."""

    sheet_id: str
    sheet_name: str
    range_name: str = "A1"
    oidc: ServiceAccountConfig

    class Config:
        """GoogleSheets settings config."""

        env_prefix = "GSHEETS_"
        env_nested_delimiter = "__"
