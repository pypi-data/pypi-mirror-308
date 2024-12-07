import logging
from typing import Optional, Type, TypeVar
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from src.config import config

logger = logging.getLogger(__name__)

class MongoClient:
    def __init__(self):
        self.client = None

    def connect(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        if loop:
            self.client = AsyncIOMotorClient(config.mongo.unicode_string(), io_loop=loop)
        else:
            self.client = AsyncIOMotorClient(config.mongo.unicode_string())
        logger.info(f'Connected to mongo: {config.mongo.unicode_string()}')

    def close(self):
        self.client.close()
        logger.info('Disconnected from mongo')


mongo_client = MongoClient()

def on_startup_db(loop: Optional[asyncio.AbstractEventLoop] = None):
    mongo_client.connect(loop)


def on_shutdown_db():
    mongo_client.close()


def get_database(database: str):
    return mongo_client.client[database]

T = TypeVar('T', bound=BaseModel)
class BaseCollection:
    def __init__(self, collection_name: str, document_type: Type[T]):
        self.collection = get_database(config.database)[collection_name]
        self.document_type = document_type

    async def insert_one(self, document: T, **kwargs):
        result = await self.collection.insert_one(
            {
                **document.model_dump(),
                **kwargs,
            }
        )
        return result.inserted_id

    async def find_by_id(self, id: str, serialize: bool = False):
        result = await self.collection.find_one({'_id': id})
        if result and serialize:
            return self.document_type(**result)
        return result

    async def update_by_id(self, id: str, **kwargs) -> bool:
        result = await self.collection.update_one(
            {'_id': id},
            {'$set': kwargs},
        )
        return result.matched_count != 0

    async def delete_by_id(self, id: str) -> bool:
        result = await self.collection.delete_one({'_id': id})
        return result.deleted_count != 0

    async def get_all(self, page: int, size: int):
        cursor = self.collection.find().skip(page * size).limit(size)
        return await cursor.to_list(length=size)
