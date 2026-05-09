from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def home():
    return FileResponse("static/index.html")

@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@router.get("/{page}")
def pages(page: str):
    return FileResponse(f"static/{page}.html")