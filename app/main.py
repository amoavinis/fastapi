from fastapi import FastAPI
from app.db.database import get_db
from app.config import settings
from app.routes import vehicles, users, devices

app = FastAPI()

app.include_router(vehicles.router)
app.include_router(users.router)
app.include_router(devices.router)


@app.get("/")
async def root():
    return settings
