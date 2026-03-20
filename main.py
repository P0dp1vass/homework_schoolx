from fastapi import FastAPI
from api.tasks import router as task_router
from api.auth import router as auth_router
from core.database import engine, Base
from core.handlers import register_exception_handlers
from models import User, Task

Base.metadata.create_all(bind=engine)

app = FastAPI()
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(task_router)
