import uvicorn
from fastapi import Depends, FastAPI

from src.auth.base_config import auth_backend, current_user, fastapi_users
from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead
from src.posts.router import router as router_post

app = FastAPI(title="Social Media")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_post)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)