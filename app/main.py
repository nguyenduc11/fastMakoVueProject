import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import RedirectResponse

from app.routers import home, about, auth

app = FastAPI()

# MongoDB Atlas connection URI from environment variable
mongodb_uri = os.environ.get("MONGODB_URI")

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    try:
        app.mongodb_client = AsyncIOMotorClient(mongodb_uri)
        app.mongodb = app.mongodb_client.flask_web
        print("Connected to MongoDB Atlas - flask_web database")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    if hasattr(app, 'mongodb_client'):
        app.mongodb_client.close()
        print("Closed MongoDB Atlas connection")

# Rest of your FastAPI setup...