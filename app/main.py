from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import auth, properties, uploads, reviews, ai
import os
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app = FastAPI(
    title="Real Estate API",
    description="Backend for a real estate listing platform",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
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
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
