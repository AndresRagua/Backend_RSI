# app/routers/home_router.py

from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

@router.get("/api")
async def root():
    return {"message": "Awesome Leads Manage"}