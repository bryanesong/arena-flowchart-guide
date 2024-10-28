import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from routers import router as routes

from fastapi.middleware.cors import CORSMiddleware

'''
from requests import Request
from contextlib import asynccontextmanager

import os

from arena_test_py.arena_code.secrets import SECRETS


POST /task/ - creates a new task.
GET /task/ - view all existing tasks.
GET /task/{id}/ - view a single task.
PUT /task/{id}/ - update a task.
DELETE /task/{id}/ - delete a task.
'''

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#starts mongodb connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    


#closes monogodb connection when server is down
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

#attaching routes to app
app.include_router(routes, tags=["flowcharts"],prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
