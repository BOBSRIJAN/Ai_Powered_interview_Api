from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.DbConfig.MongoDBAtlas import establishConnection, terminatedConnection
from app.Routers.route import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    establishConnection()
    yield
    terminatedConnection()

app = FastAPI(
    title="FastAPI MongoEngine App",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome To Interview Question Service"}