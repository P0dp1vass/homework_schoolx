from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from sqlalchemy import text

from api.tasks import router as task_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from core.database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.handlers import register_exception_handlers
from core.minio_client import minio_client

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
    # Base.metadata.create_all is sync, so it uses engine.begin()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schemas are verified.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Check DB
    await db.execute(text("SELECT 1"))
    # Check Minio
    try:
        minio_client.list_buckets()
    except Exception as e:
        return {"status": "error", "minio": str(e)}
    return {"status": "ok"}

@app.get("/info")
async def info_check():
    return {"version": "0.1.0", "env": "dev"}

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(comments_router)
