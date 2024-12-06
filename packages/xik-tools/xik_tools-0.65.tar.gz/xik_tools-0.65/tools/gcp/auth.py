from googleapiclient.discovery import build
from google.oauth2 import service_account
import logging

class GCP_AUTH:
    @staticmethod
    def authenticate_with_json(json_path: str):
        logging.info("Authenticating Google Calendar service...")
        try:
            # JSON 파일을 통해 자격 증명 생성
            credentials = service_account.Credentials.from_service_account_file(json_path)
            service = build('calendar', 'v3', credentials=credentials)
            logging.info("Successfully authenticated Google Calendar service.")
            return service
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            raise ValueError(f"Authentication failed: {e}")