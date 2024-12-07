import os
from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    from src.config import config
    from src.database import on_shutdown_db, on_startup_db
    from src.main import app

    mongo: MongoDbContainer = MongoDbContainer("mongo:7")
    mongo.start()
    os.environ["MONGO"] = mongo.get_connection_url()

    config.reload_mongo()

    on_startup_db()

    yield app

    on_shutdown_db()

    mongo.stop()


@pytest_asyncio.fixture(scope="session")
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
def mongo(app) -> AsyncGenerator[AsyncIOMotorClient, None]:
    from src.config import config

    client = AsyncIOMotorClient(config.mongo.unicode_string())

    yield client

    client.close()
