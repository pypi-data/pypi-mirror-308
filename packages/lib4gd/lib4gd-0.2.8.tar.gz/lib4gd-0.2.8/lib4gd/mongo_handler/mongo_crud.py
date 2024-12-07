import asyncio
import logging
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

    async def insert_many(self, documents):
        """Insert multiple documents concurrently with ResourceManager."""
        logger.info("Inserting %d documents into the collection.", len(documents))

        async def insert_document(doc):
            async with self.resource_manager.get_semaphore():
                return await self.collection.insert_one(doc)

        tasks = [insert_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        
        logger.info("Inserted %d documents successfully.", len(results))
        return results

    async def fetch_many(self, query, batch_size=100):
        """Read documents in parallel with ResourceManager."""
        logger.info("Fetching documents with query: %s", query)
        total_count = await self.collection.count_documents(query)
        logger.info("Total documents matching query: %d", total_count)

        async def fetch_batch(skip):
            async with self.resource_manager.get_semaphore():
                cursor = self.collection.find(query).skip(skip).limit(batch_size)
                return await cursor.to_list(length=batch_size)

        tasks = [fetch_batch(skip) for skip in range(0, total_count, batch_size)]
        results = await asyncio.gather(*tasks)
        
        documents = [doc for batch in results for doc in batch]
        logger.info("Fetched %d documents successfully.", len(documents))
        return documents

    async def update_many(self, query, update_values):
        """Update documents concurrently with ResourceManager."""
        logger.info("Updating documents matching query: %s with values: %s", query, update_values)
        async with self.resource_manager.get_semaphore():
            result = await self.collection.update_many(query, {'$set': update_values})
        
        logger.info("Updated %d documents successfully.", result.modified_count)
        return result

    async def delete_many(self, query):
        """Delete documents concurrently with ResourceManager."""
        logger.info("Deleting documents matching query: %s", query)
        async with self.resource_manager.get_semaphore():
            result = await self.collection.delete_many(query)
        
        logger.info("Deleted %d documents successfully.", result.deleted_count)
        return result

    def shutdown(self):
        """Shut down the MongoDB connection."""
        logger.info("Shutting down MongoDB connection.")
        self.client.close()
