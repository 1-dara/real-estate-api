from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, properties, uploads, reviews
import os

app = FastAPI(
    title="Real Estate API",
    description="Backend for a real estate listing platform",
    version="1.0.0"
)

# Allow frontend to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(properties.router,
                   prefix="/api/properties", tags=["Properties"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["Uploads"])
app.include_router(reviews.router, prefix="/api/properties", tags=["Reviews"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
