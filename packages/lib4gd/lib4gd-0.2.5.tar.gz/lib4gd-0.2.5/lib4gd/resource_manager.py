import asyncio
from concurrent.futures import ThreadPoolExecutor

class ResourceManager:
    """
    A centralized resource manager for handling shared resources like 
    thread pools and semaphores within the lib4gd library.

    This class helps control and manage concurrent operations by 
    providing a shared ThreadPoolExecutor and Semaphore instance. 
    It ensures that resources are used efficiently across the library.
    """

    _thread_pool = None
    _semaphore = None

    @classmethod
    def get_thread_pool(cls, max_workers: int = 10):
        """
        Get or create a shared ThreadPoolExecutor for managing thread-based concurrency.

        If a ThreadPoolExecutor instance does not already exist, this method creates one 
        with the specified number of max_workers.

        :param max_workers: The maximum number of threads that can run concurrently.
        :return: A ThreadPoolExecutor instance.
        """
        if cls._thread_pool is None:
            cls._thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        return cls._thread_pool

    @classmethod
    def get_semaphore(cls, max_concurrent: int = 10):
        """
        Get or create a shared Semaphore for managing asyncio-based concurrency.

        The Semaphore limits the number of concurrent tasks that can be run simultaneously.
        If a Semaphore instance does not already exist, this method creates one with the 
        specified maximum concurrency.

        :param max_concurrent: The maximum number of concurrent tasks allowed.
        :return: An asyncio.Semaphore instance.
        """
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(max_concurrent)
        return cls._semaphore

    @classmethod
    def shutdown_resources(cls):
        """
        Shutdown and clean up the shared resources.

        This method shuts down the ThreadPoolExecutor gracefully, waiting for all 
        running threads to complete. It also resets the Semaphore instance.

        It is recommended to call this method during application shutdown to release 
        any resources held by the library.
        """
        if cls._thread_pool:
            cls._thread_pool.shutdown(wait=True)
        cls._thread_pool = None
        cls._semaphore = None
