from .auth import router as auth_router
from .tasks import router as task_router
from .comments import router as comments_router

routers = [auth_router, task_router, comments_router]
