from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build


class Google:
    @staticmethod
    def get_service():
        SCOPES = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
        ]

        credentials = service_account.Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        return build("sheets", "v4", credentials=credentials, cache_discovery=False)

    def append_values(self, values):
        # How the input data should be interpreted.
        value_input_option = "USER_ENTERED"  # TODO: Update placeholder value.

        # How the input data should be inserted.
        insert_data_option = "INSERT_ROWS"  # TODO: Update placeholder value.

        value_range_body = {
            "values": [values.split(";")],
            "majorDimension": "DIMENSION_UNSPECIFIED",
            "range": settings.GOOGLW_RANGE_NAME,
        }
        service = self.get_service()

        request = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=settings.GOOGLE_SPREADSHEET_ID,
                range=settings.GOOGLW_RANGE_NAME,
                valueInputOption=value_input_option,
                responseDateTimeRenderOption="SERIAL_NUMBER",
                insertDataOption=insert_data_option,
                body=value_range_body,
            )
        )
        response = request.execute()

        # return "Linha edicionada com sucesso"
        return response
