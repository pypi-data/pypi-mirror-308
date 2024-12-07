import asyncio
from concurrent.futures import ThreadPoolExecutor

class ResourceManager:
    """
    A centralized resource manager for handling shared resources like 
    thread pools and semaphores within the lib4gd library.

    This class helps control and manage concurrent operations by 
    providing both instance-based and class-level shared resources.
    It also allows dynamic adjustment of concurrency limits.
    """

    _class_thread_pool = None
    _class_semaphore = None

    def __init__(self, max_workers=10, max_concurrent=10):
        """
        Initialize an instance of ResourceManager with configurable concurrency limits.

        :param max_workers: Maximum threads in the thread pool (default: 10).
        :param max_concurrent: Maximum concurrent tasks allowed in the Semaphore (default: 10).
        """
        self.max_workers = max_workers
        self.max_concurrent = max_concurrent
        self._thread_pool = None
        self._semaphore = None

    def get_thread_pool(self):
        """
        Get or create an instance-specific ThreadPoolExecutor.
        """
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        return self._thread_pool

    def get_semaphore(self):
        """
        Get or create an instance-specific asyncio.Semaphore.
        """
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
        return self._semaphore

    def adjust_concurrency(self, max_workers=None, max_concurrent=None):
        """
        Adjust concurrency limits dynamically for threads and asyncio tasks.

        :param max_workers: New maximum threads for ThreadPoolExecutor.
        :param max_concurrent: New maximum concurrent tasks for Semaphore.
        """
        if max_workers is not None:
            self.max_workers = max_workers
            if self._thread_pool:
                self._thread_pool.shutdown(wait=True)
                self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

        if max_concurrent is not None:
            self.max_concurrent = max_concurrent
            if self._semaphore:
                self._semaphore = asyncio.Semaphore(max_concurrent)

    @classmethod
    def get_class_thread_pool(cls, max_workers=10):
        """
        Get or create a shared class-level ThreadPoolExecutor.
        """
        if cls._class_thread_pool is None:
            cls._class_thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        return cls._class_thread_pool

    @classmethod
    def get_class_semaphore(cls, max_concurrent=10):
        """
        Get or create a shared class-level asyncio.Semaphore.
        """
        if cls._class_semaphore is None:
            cls._class_semaphore = asyncio.Semaphore(max_concurrent)
        return cls._class_semaphore

    @classmethod
    def shutdown_class_resources(cls):
        """
        Shutdown shared class-level resources.
        """
        if cls._class_thread_pool:
            cls._class_thread_pool.shutdown(wait=True)
        cls._class_thread_pool = None
        cls._class_semaphore = None

    def shutdown_resources(self):
        """
        Shutdown instance-specific resources.
        """
        if self._thread_pool:
            self._thread_pool.shutdown(wait=True)
        self._thread_pool = None
        self._semaphore = None
