from fastapi import FastAPI
from app.Routers.route import router
from contextlib import asynccontextmanager
from app.DbConfig.MongoDBAtlas import establishConnection, terminatedConnection
from app.Worker.EventHandler import eventHandler
from app.Worker.KafkaConsumer import startConsumer
import threading
import logging

stop_event = threading.Event()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def initSubprocess() -> None:
    startConsumer(eventHandler, stop_event)
    logger.info("Fast Api custom worker started.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    establishConnection()
    thread = threading.Thread(target=initSubprocess, daemon=True)
    thread.start()
    yield
    stop_event.set()
    thread.join(timeout=5)
    terminatedConnection()

app = FastAPI(title="FastAPI MongoEngine App", lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome To Interview Question Service"}