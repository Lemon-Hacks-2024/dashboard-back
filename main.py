from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from database.models import create_all
from endpoints.routers import router
from endpoints.auth import auth, executors
from helpers.control import header_control


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  await create_all()
    yield


app = FastAPI(
    title="Dashboard",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(
    router, prefix="/api/v1/dashboard",
    tags=["Dashboard"], dependencies=[Depends(header_control)]
)
app.include_router(
    auth, prefix="/token",
    tags=["Auth"], dependencies=[Depends(header_control)]
)
app.include_router(
    executors, prefix="/employees",
    tags=["Employees"], dependencies=[Depends(header_control)],
)

if __name__ == "__main__":
    uvicorn.run(app)
