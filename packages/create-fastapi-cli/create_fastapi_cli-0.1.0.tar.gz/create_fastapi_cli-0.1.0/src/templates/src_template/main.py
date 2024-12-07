import logging

import uvloop
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import on_shutdown_db, on_startup_db

from src.config import config
from src.routers.greeting.router import router as greeting_router
from src.utils import configure_logging

logger = logging.getLogger(__name__)

configure_logging()

def on_startup():
    uvloop.install()

    on_startup_db()

    logger.info(f'Server started on {config.env}')

def on_shutdown():
    on_shutdown_db()
    logger.info('Server stopped')


app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
app.add_middleware(CorrelationIdMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(greeting_router, prefix="/api", tags=["greeting"])
