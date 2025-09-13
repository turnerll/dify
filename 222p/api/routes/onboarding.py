# Onboarding routes
from fastapi import APIRouter

router = APIRouter()

@router.get("/questions")
async def get_questions():
    return {"message": "Get onboarding questions - to be implemented"}

@router.post("/responses")
async def submit_responses():
    return {"message": "Submit responses - to be implemented"}