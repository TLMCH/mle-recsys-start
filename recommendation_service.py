import logging

from recommendations import Recommendations
from fastapi import FastAPI
from contextlib import asynccontextmanager

logger = logging.getLogger("uvicorn.error")
rec_store = Recommendations()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logger.info("Starting")
    rec_store.load(
        "personal",
        'final_recommendations_feat.parquet',
        columns=["user_id", "item_id", "rank"],
    )
    rec_store.load(
        "default",
        'top_recs.parquet',
        columns=["item_id", "rank"],
    )
    yield
    # этот код выполнится только один раз при остановке сервиса
    logger.info("Stopping")
    rec_store.stats()
    
# создаём приложение FastAPI
app = FastAPI(title="recommendations", lifespan=lifespan)

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    recs = [rec_store.get(user_id, k)]

    return {"recs": recs}