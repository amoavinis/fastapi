from fastapi import FastAPI
from app.db.database import get_db
from app.config import settings
from app.routes import vehicles

app = FastAPI()

app.include_router(vehicles.router)


@app.get("/")
async def root():
    return settings
