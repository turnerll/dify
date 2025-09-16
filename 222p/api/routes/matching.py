# Matching routes
from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
async def generate_matches():
    return {"message": "Generate matches - to be implemented"}

@router.get("/")
async def get_matches():
    return {"message": "Get user matches - to be implemented"}