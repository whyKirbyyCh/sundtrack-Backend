from functools import lru_cache
from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from src.config import Settings
from src.affiliate.router import affiliate_router
from src.analysis.client import AnalysisClient


app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version
    }

@app.on_event("shutdown")
async def shutdown_analysisclient():
    await AnalysisClient.CLIENT.aclose()

app.include_router(affiliate_router)


print(affiliate_router)
