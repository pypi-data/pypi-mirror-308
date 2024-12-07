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
        self.thread_pool = ResourceManager.get_thread_pool()
        self.semaphore = ResourceManager.get_semaphore()

    async def connect(self):
        self.connection = await asyncssh.connect(self.hostname, username=self.username, password=self.password)
        self.sftp = await self.connection.start_sftp()

    async def disconnect(self):
        self.sftp.close()
        await self.sftp.wait_closed()
        self.connection.close()

    async def download_file(self, remote_path: str, local_path: str):
        async with self.semaphore:
            async with aiofiles.open(local_path, 'wb') as f:
                await self.sftp.get(remote_path, f)

    async def download_files_concurrently(self, remote_paths: list, local_dir: str):
        tasks = [self.download_file(remote_path, os.path.join(local_dir, os.path.basename(remote_path)))
                 for remote_path in remote_paths]
        return await asyncio.gather(*tasks)

    async def process_file_in_memory(self, remote_path: str):
        async with self.semaphore:
            async with self.sftp.open(remote_path, 'rb') as remote_file:
                data = await remote_file.read()
                fh = BytesIO(data)
                image = Image.open(fh)
                return image

    async def process_files_in_memory_concurrently(self, remote_paths: list):
        tasks = [self.process_file_in_memory(remote_path) for remote_path in remote_paths]
        return await asyncio.gather(*tasks)
    
    async def process_files_in_memory_in_batches(self, file_list, batch_size=100):
        """Process files in memory in smaller batches."""
        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i + batch_size]
            results = await self.process_files_in_memory_concurrently(batch)
            
    async def upload_file(self, local_file_path: str, remote_path: str):
        async with self.semaphore:
            async with aiofiles.open(local_file_path, 'rb') as f:
                async with self.sftp.open(remote_path, 'wb') as remote_file:
                    await remote_file.write(await f.read())

    async def upload_files_concurrently(self, files: list):
        tasks = [self.upload_file(file['local'], file['remote']) for file in files]
        return await asyncio.gather(*tasks)
