from fastapi import FastAPI
from app.routers import users_router, notes_router

app = FastAPI()

app.include_router(users_router)
app.include_router(notes_router)
