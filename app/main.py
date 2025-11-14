from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import get_db
from app.config import settings
from app.routes import vehicles, users, devices, websocket

app = FastAPI()

# Configure CORS for WebSocket and API access from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicles.router)
app.include_router(users.router)
app.include_router(devices.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return settings
