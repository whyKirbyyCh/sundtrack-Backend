from fastapi import APIRouter

affiliate_router: APIRouter = APIRouter(
    prefix="/affiliate",
    tags=["affiliate"]
)

@affiliate_router.post("/register/{code}")
def register(code):
    return {"code" : code}
