import asyncio
import aiofiles
import asyncssh
import os
from typing import List
from lib4gd.resource_manager import ResourceManager

class SFTPDownloader:
    def __init__(self, hostname: str, username: str, password: str, max_concurrent_downloads: int = 10):
        """
        Initialize the SFTPDownloader with connection details and concurrency controls.

        :param hostname: The SFTP server hostname.
        :param username: The username for SFTP authentication.
        :param password: The password for SFTP authentication.
        :param max_concurrent_downloads: Maximum number of concurrent downloads allowed.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.semaphore = ResourceManager.get_semaphore(max_concurrent_downloads)
        self.thread_pool = ResourceManager.get_thread_pool(max_concurrent_downloads)

    async def connect(self):
        """Establish an SFTP connection."""
        self.connection = await asyncssh.connect(self.hostname, username=self.username, password=self.password)
        self.sftp = await self.connection.start_sftp()

    async def disconnect(self):
        """Close the SFTP connection."""
        self.sftp.close()
        await self.sftp.wait_closed()
        self.connection.close()

    async def download_file(self, remote_path: str, local_path: str):
        """Download a single file from the SFTP server to the local system."""
        async with self.semaphore:
            async with aiofiles.open(local_path, 'wb') as f:
                await self.sftp.get(remote_path, f)

    async def download_files(self, remote_paths: List[str], local_dir: str):
        """Download multiple files from the SFTP server in parallel."""
        await self.connect()

        tasks = []
        for remote_path in remote_paths:
            local_path = os.path.join(local_dir, os.path.basename(remote_path))
            tasks.append(self.download_file(remote_path, local_path))

        await asyncio.gather(*tasks)
        await self.disconnect()
