from fastapi import FastAPI
import logging
import sys

from api.tasks import router as task_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from core.database import engine, Base
from core.handlers import register_exception_handlers
from models import User, Task

# Базовая настройка логирования в приложении
logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the School X Backend...")
    logger.info("Database schemas are verified.")
    yield

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(comments_router)
