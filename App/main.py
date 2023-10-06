from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routes import service, user, mechanic, auth, vehicle, work, map
from config import Settings

import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(mechanic.router)
app.include_router(map.router)
app.include_router(vehicle.router)
app.include_router(service.router)
app.include_router(work.router)


@app.get("/")
def root():
    return {
        "api_name": "FixMyRide",
        "api_version": "1.0",
        "available_resources": [
            {
            "name": "user",
            "description": "Endpoint to manage user data",
            "link": "/user"
            },
            {
            "name": "mechanic",
            "description": "Endpoint to manage mechanic data",
            "link": "/mechanic"
            },
            {
            "name": "service",
            "description": "Endpoint to retrieve services",
            "link": "/service"
            },
            {
            "name": "map",
            "description": "Endpoint to retrieve map",
            "link": "/map"
            }
        ],
        "documentation_link": "https://api.fixmyride.com/docs",
        "contact_email": "support@fixmyride.com",
        "authentication_info": {
            "method": "API Key",
            "details": "Use your API key to authenticate requests."
        }
        }
