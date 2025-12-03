from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow Framer, local dev, everything 
    allow_credentials=True,
    allow_methods=["*"],          # allows POST, GET, OPTIONS, etc
    allow_headers=["*"],          # allow all headers including file uploads
)

app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")


