import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from lib4gd.resource_manager import ResourceManager

class MongoDBHandler:
    def __init__(self, connection_string, db_name, collection_name, max_concurrent_requests=5):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.resource_manager = ResourceManager(max_concurrent=max_concurrent_requests)

    async def insert_many(self, documents):
        """Insert multiple documents concurrently with ResourceManager."""
        async def insert_document(doc):
            async with self.resource_manager.get_semaphore():
                return await self.collection.insert_one(doc)

        tasks = [insert_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        return results

    async def fetch_many(self, query, batch_size=100):
        """Read documents in parallel with ResourceManager."""
        total_count = await self.collection.count_documents(query)
        batch_count = (total_count + batch_size - 1) // batch_size

        async def fetch_batch(skip):
            async with self.resource_manager.get_semaphore():
                cursor = self.collection.find(query).skip(skip).limit(batch_size)
                return await cursor.to_list(length=batch_size)

        tasks = [fetch_batch(skip) for skip in range(0, total_count, batch_size)]
        results = await asyncio.gather(*tasks)
        
        documents = [doc for batch in results for doc in batch]
        return documents

    async def update_many(self, query, update_values):
        """Update documents concurrently with ResourceManager."""
        async with self.resource_manager.get_semaphore():
            result = await self.collection.update_many(query, {'$set': update_values})
        return result

    async def delete_many(self, query):
        """Delete documents concurrently with ResourceManager."""
        async with self.resource_manager.get_semaphore():
            result = await self.collection.delete_many(query)
        return result

    def shutdown(self):
        """Shut down the MongoDB connection."""
        self.client.close()
