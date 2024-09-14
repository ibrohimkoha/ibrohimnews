from fastapi import FastAPI
from users.main import router as users_router
from posts.main import router as posts_router

app = FastAPI(title="NewsIbrohim")

app.include_router(router=users_router)
app.include_router(router=posts_router)