from fastapi import APIRouter

router = APIRouter(tags=["health"], prefix="/health")

@router.get("")
async def health():
    return {"status" : "ok"}