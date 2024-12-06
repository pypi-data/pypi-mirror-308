import os
import io
import re
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from concurrent.futures import ThreadPoolExecutor
from lib4gd.resource_manager import ResourceManager

class GoogleDriveDownloader:
    def __init__(self, credentials_path: str, max_concurrent_downloads: int = 10):
        """
        Initialize the GoogleDriveDownloader with service account credentials and concurrency controls.

        :param credentials_path: Path to the service account credentials JSON file.
        :param max_concurrent_downloads: Maximum number of concurrent downloads allowed.
        """
        self.credentials_path = credentials_path
        self.service = self._authenticate()
        self.semaphore = ResourceManager.get_semaphore(max_concurrent_downloads)
        self.thread_pool = ResourceManager.get_thread_pool(max_concurrent_downloads)

    def _authenticate(self):
        """Authenticate using the service account credentials and return a Google Drive service instance."""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)

    def extract_folder_id_from_url(self, url: str) -> str:
        """
        Extract the folder ID from a Google Drive folder URL.

        :param url: Google Drive folder URL.
        :return: Folder ID.
        """
        match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid Google Drive folder URL")

    def extract_folder_name(self, folder_id: str) -> str:
        """
        Retrieve the folder name given its ID.

        :param folder_id: Google Drive folder ID.
        :return: Folder name.
        """
        folder_metadata = self.service.files().get(fileId=folder_id, fields='name').execute()
        return folder_metadata['name']

    def list_files_in_folder(self, folder_id: str) -> list:
        """
        List all files in a Google Drive folder.

        :param folder_id: Google Drive folder ID.
        :return: List of file metadata dictionaries.
        """
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
        return results.get('files', [])

    async def _download_file_async(self, file_id: str, file_name: str, destination_folder: str):
        """
        Asynchronously download a single file from Google Drive.

        :param file_id: The Google Drive file ID.
        :param file_name: Name of the file to save as locally.
        :param destination_folder: Local directory to save the downloaded file.
        """
        request = self.service.files().get_media(fileId=file_id)
        file_path = os.path.join(destination_folder, file_name)

        async with self.semaphore:
            with open(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    await asyncio.get_event_loop().run_in_executor(self.thread_pool, downloader.next_chunk)

    async def download_files_from_folder(self, folder_url: str, destination_folder: str = 'downloaded_files'):
        """
        Download all files from a Google Drive folder asynchronously.

        :param folder_url: Google Drive folder URL.
        :param destination_folder: Local directory to save the downloaded files.
        """
        folder_id = self.extract_folder_id_from_url(folder_url)
        folder_name = self.extract_folder_name(folder_id)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        files = self.list_files_in_folder(folder_id)
        if not files:
            raise FileNotFoundError('No files found in the folder.')

        tasks = [self._download_file_async(file['id'], file['name'], destination_folder) for file in files]
        await asyncio.gather(*tasks)

        print(f"All files from '{folder_name}' have been downloaded to '{destination_folder}'.")
