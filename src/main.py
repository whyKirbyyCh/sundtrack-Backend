from functools import lru_cache
from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from config import Settings

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
