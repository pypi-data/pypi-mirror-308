import asyncio
import logging
import time
import psutil  # For memory and CPU usage
from motor.motor_asyncio import AsyncIOMotorClient
from lib4gd.resource_manager import ResourceManager

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBHandler:
    def __init__(self, connection_string, db_name, collection_name, max_concurrent_requests=5):
        logger.info("Initializing MongoDBHandler for database: %s, collection: %s", db_name, collection_name)
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.resource_manager = ResourceManager(max_concurrent=max_concurrent_requests)

    def _log_metrics(self, operation: str, start_time: float, end_time: float):
        """
        Logs time taken, memory usage, and CPU usage for an operation.

        :param operation: Name of the operation performed.
        :param start_time: Start time of the operation.
        :param end_time: End time of the operation.
        """
        duration = end_time - start_time
        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        cpu_usage = psutil.cpu_percent(interval=None)  # CPU usage since last call
        logger.info(
            "%s completed in %.2f seconds. Memory usage: %.2f MB. CPU usage: %.2f%%.",
            operation, duration, memory_usage, cpu_usage
        )

    async def insert_many(self, documents):
        """Insert multiple documents concurrently with ResourceManager."""
        logger.info("Inserting %d documents into the collection.", len(documents))
        start_time = time.time()

        async def insert_document(doc):
            async with self.resource_manager.get_semaphore():
                return await self.collection.insert_one(doc)

        tasks = [insert_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        logger.info("Inserted %d documents successfully.", len(results))
        self._log_metrics("Insert Many", start_time, end_time)
        return results

    async def fetch_many(self, query, batch_size=100):
        """Read documents in parallel with ResourceManager."""
        logger.info("Fetching documents with query: %s", query)
        start_time = time.time()

        total_count = await self.collection.count_documents(query)
        logger.info("Total documents matching query: %d", total_count)

        async def fetch_batch(skip):
            async with self.resource_manager.get_semaphore():
                cursor = self.collection.find(query).skip(skip).limit(batch_size)
                return await cursor.to_list(length=batch_size)

        tasks = [fetch_batch(skip) for skip in range(0, total_count, batch_size)]
        results = await asyncio.gather(*tasks)
        
        documents = [doc for batch in results for doc in batch]
        end_time = time.time()
        logger.info("Fetched %d documents successfully.", len(documents))
        self._log_metrics("Fetch Many", start_time, end_time)
        return documents

    async def update_many(self, query, update_values):
        """Update documents concurrently with ResourceManager."""
        logger.info("Updating documents matching query: %s with values: %s", query, update_values)
        start_time = time.time()

        async with self.resource_manager.get_semaphore():
            result = await self.collection.update_many(query, {'$set': update_values})
        
        end_time = time.time()
        logger.info("Updated %d documents successfully.", result.modified_count)
        self._log_metrics("Update Many", start_time, end_time)
        return result

    async def delete_many(self, query):
        """Delete documents concurrently with ResourceManager."""
        logger.info("Deleting documents matching query: %s", query)
        start_time = time.time()

        async with self.resource_manager.get_semaphore():
            result = await self.collection.delete_many(query)
        
        end_time = time.time()
        logger.info("Deleted %d documents successfully.", result.deleted_count)
        self._log_metrics("Delete Many", start_time, end_time)
        return result

    def shutdown(self):
        """Shut down the MongoDB connection."""
        logger.info("Shutting down MongoDB connection.")
        self.client.close()
