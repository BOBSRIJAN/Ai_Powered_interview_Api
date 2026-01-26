from fastapi import FastAPI
from app.Routers.route import router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.DbConfig.MongoDBAtlas import establishConnection, terminatedConnection

"""FastAPI application with MongoDB connection management."""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ 
        Lifespan context manager to handle startup and shutdown events.
        Establishes a connection to the database on startup and terminates it on shutdown.
    """
    establishConnection()
    yield
    terminatedConnection()

app = FastAPI(
    title="FastAPI MongoEngine App",
    lifespan=lifespan
)

ALLOWHOST = ["http://localhost:8000", "http://127.0.0.1:8000", "*" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWHOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome To Resume Service Backend API!"}