"""GoogleSheets client."""

from google.oauth2 import service_account
import gspread

from libs.google_sheets.config import GoogleSheetsConfig


class GoogleSheetsClient:
    """Wrapper around the Googlesheets client."""

    def __init__(self):
        """Initialize GoogleSheets client."""
        self.config = GoogleSheetsConfig()

    def authenticate_google_sheets(self):
        """Authenticate in GoogleSheets."""
        service_account_dict = self.config.oidc.model_dump()
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(service_account_dict, scopes=scopes)
        client = gspread.authorize(creds)
        return client

    def write_to_google_sheets(self, values):
        """Write data into a sheet."""
        client = self.authenticate_google_sheets()
        sheet = client.open_by_key(self.config.sheet_id).worksheet(self.config.sheet_name)

        # Clear existing content in the sheet
        sheet.clear()

        # Write the data to the sheet
        sheet.update(range_name=self.config.range_name, values=values)
