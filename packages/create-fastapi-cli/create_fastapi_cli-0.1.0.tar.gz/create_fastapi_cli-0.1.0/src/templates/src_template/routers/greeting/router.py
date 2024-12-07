import logging

from fastapi import APIRouter

from src.decos import log_io
from src.routers.greeting.schema import GreetingRequest

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/greeting",
    description="Greets the user with a message.",
)
@log_io
async def greeting(req: GreetingRequest):
    logger.info(f"Received request: {req}")
    return {"message": f"Hello, {req.name}"}
