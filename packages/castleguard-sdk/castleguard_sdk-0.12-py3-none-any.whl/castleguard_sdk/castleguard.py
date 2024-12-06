import requests


from anomyzer import Anomyzer
from auth import Auth
from chat import Chat
from ner import Ner
from transcription import Transcription
from translate import Translate
from collection import Collection
from hearthbeat import HearthBeat
from vision import Vision


class CastleGuard(Auth, Chat, Translate, Ner, Transcription, Collection, Anomyzer, HearthBeat, Vision):
    def __init__(self, base_url, username, password, default_version="v1"):
        """
        Initialize the CastleGuard class with base credentials.

        :param base_url: Base URL for the CastleGuard API.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param default_version: Default API version to use if not provided in base_url.
        """
        self.base_url = self._normalize_url(base_url, default_version)
        self.username = username
        self.password = password
        self.token = None
        self.authenticate()

    def text_extraction(self, raw_text):
        """
        Extracts paragraphs from the provided raw text.

        :param raw_text: The raw text to extract paragraphs from.
        :return: A list of paragraphs or None if the request fails.
        """
        url = f'{self.base_url}/text-extraction'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "rawText": raw_text
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("paragraphs", [])
            else:
                self.log(f"Text extraction failed: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Text extraction request failed: {e}", logLevel=3)
            return None

    def text_extraction_from_document(self, file_path):
        """
        Extracts text from a binary document file.

        :param file_path: Path to the binary file to extract text from.
        :return: Extracted text or None if the request fails.
        """
        url = f'{self.base_url}/text-extraction/document'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'file': open(file_path, 'rb')
        }

        try:
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Text extraction from document failed: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Text extraction from document request failed: {e}", logLevel=3)
            return None
