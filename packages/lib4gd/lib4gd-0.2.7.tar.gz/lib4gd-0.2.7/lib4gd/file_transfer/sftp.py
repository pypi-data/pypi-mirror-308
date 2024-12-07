import os
import aiofiles
import asyncssh
import asyncio
from PIL import Image
from io import BytesIO
from lib4gd.resource_manager import ResourceManager

class SFTPHandler:
    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.connection = None
        self.sftp = None

    async def connect(self):
        """
        Establish an SFTP connection.
        """
        self.connection = await asyncssh.connect(self.hostname, username=self.username, password=self.password)
        self.sftp = await self.connection.start_sftp()

    async def disconnect(self):
        """
        Close the SFTP connection.
        """
        if self.sftp:
            self.sftp.close()
            await self.sftp.wait_closed()
        if self.connection:
            self.connection.close()

    async def download_file(self, remote_path: str, local_path: str):
        """
        Download a single file from the SFTP server.
        """
        async with ResourceManager.get_semaphore():
            async with aiofiles.open(local_path, 'wb') as f:
                await self.sftp.get(remote_path, f)

    async def download_files_concurrently(self, remote_paths: list, local_dir: str):
        """
        Download multiple files concurrently from the SFTP server.
        """
        tasks = [
            self.download_file(remote_path, os.path.join(local_dir, os.path.basename(remote_path)))
            for remote_path in remote_paths
        ]
        return await asyncio.gather(*tasks)

    async def process_file_in_memory(self, remote_path: str):
        """
        Download and process a file in memory.
        """
        async with ResourceManager.get_semaphore():
            async with self.sftp.open(remote_path, 'rb') as remote_file:
                data = await remote_file.read()
                fh = BytesIO(data)
                image = Image.open(fh)
                return image

    async def process_files_in_memory_concurrently(self, remote_paths: list):
        """
        Process multiple files in memory concurrently.
        """
        tasks = [self.process_file_in_memory(remote_path) for remote_path in remote_paths]
        return await asyncio.gather(*tasks)
    
    async def process_files_in_memory_in_batches(self, file_list, batch_size=100):
        """
        Process files in memory in smaller batches.
        """
        all_results = []
        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i + batch_size]
            results = await self.process_files_in_memory_concurrently(batch)
            all_results.extend(results)
        return all_results
            
    async def upload_file(self, local_file_path: str, remote_path: str):
        """
        Upload a single file to the SFTP server.
        """
        async with ResourceManager.get_semaphore():
            async with aiofiles.open(local_file_path, 'rb') as f:
                async with self.sftp.open(remote_path, 'wb') as remote_file:
                    await remote_file.write(await f.read())

    async def upload_files_concurrently(self, files: list):
        """
        Upload multiple files concurrently to the SFTP server.

        :param files: List of dictionaries with 'local' and 'remote' file paths.
        """
        tasks = [self.upload_file(file['local'], file['remote']) for file in files]
        return await asyncio.gather(*tasks)
