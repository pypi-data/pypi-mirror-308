import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from PIL import Image
import asyncio
from lib4gd.resource_manager import ResourceManager

class GoogleDriveHandler:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.service = self._authenticate()
        self.thread_pool = ResourceManager.get_thread_pool()
        self.semaphore = ResourceManager.get_semaphore()

    def _authenticate(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=['https://www.googleapis.com/auth/drive.file']
        )
        return build('drive', 'v3', credentials=credentials)

    def list_files_in_folder(self, folder_id: str) -> list:
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
        return results.get('files', [])

    def download_file(self, file_id: str, file_name: str, destination_folder: str):
        request = self.service.files().get_media(fileId=file_id)
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    async def _download_file_async(self, file_id: str, file_name: str, destination_folder: str):
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.thread_pool, self.download_file, file_id, file_name, destination_folder)

    async def download_files_concurrently(self, file_list, destination_folder: str):
        tasks = [self._download_file_async(file['id'], file['name'], destination_folder) for file in file_list]
        return await asyncio.gather(*tasks)

    async def process_file_in_memory(self, file_id: str):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = await asyncio.get_event_loop().run_in_executor(self.thread_pool, downloader.next_chunk)
        fh.seek(0)
        image = Image.open(fh)
        return image
    
    async def process_files_in_memory_in_batches(self, file_list, batch_size=100):
        """Process files in memory in smaller batches."""
        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i + batch_size]
            results = await self.process_files_in_memory_concurrently(batch)

    async def process_files_in_memory_concurrently(self, file_list):
        tasks = [self.process_file_in_memory(file['id']) for file in file_list]
        return await asyncio.gather(*tasks)

    def upload_file(self, local_file_path: str, folder_id: str):
        file_metadata = {'name': os.path.basename(local_file_path), 'parents': [folder_id]}
        media = MediaFileUpload(local_file_path, resumable=True)
        uploaded_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return uploaded_file['id']

    async def _upload_file_async(self, local_file_path: str, folder_id: str):
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.thread_pool, self.upload_file, local_file_path, folder_id)

    async def upload_files_concurrently(self, files: list, folder_id: str):
        tasks = [self._upload_file_async(file_path, folder_id) for file_path in files]
        return await asyncio.gather(*tasks)
