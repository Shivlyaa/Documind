from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")

