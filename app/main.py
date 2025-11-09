from fastapi import FastAPI
from app.db.database import get_db
from app.config import settings
from app.routes import vehicles, users

app = FastAPI()

app.include_router(vehicles.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return settings
