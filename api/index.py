from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the main application
from main_simple import app as backend_app

# Create FastAPI app for Vercel
app = FastAPI(title="Neuro-Symbolic Leadership AI API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all backend routes
for route in backend_app.routes:
    app.include_router(route)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Neuro-Symbolic Leadership AI"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Neuro-Symbolic Leadership AI API is running"}

# Export the app for Vercel
handler = app
