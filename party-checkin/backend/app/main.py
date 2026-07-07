from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.admin import router as admin_router
from app.database import Base, engine
from app.models.attendee import Attendee
from app.api.checkin import router as checkin_router
from fastapi.responses import FileResponse
from app.api.upload import router as upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Party Check-In API",
    version="1.0"
)

app.include_router(checkin_router)
app.include_router(admin_router)
app.include_router(upload_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/admin")
def admin_page():
    return FileResponse("static/admin.html")