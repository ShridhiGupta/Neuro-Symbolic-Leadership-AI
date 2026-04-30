from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from pathlib import Path

from app.core.config import settings
from app.api.routes import assessment, upload, analysis
from app.services.database_service import DatabaseService

# Initialize FastAPI app
app = FastAPI(
    title="Neuro-Symbolic Leadership AI",
    description="AI system for cross-cultural leadership assessment",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(assessment.router, prefix="/api/assessment", tags=["assessment"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Neuro-Symbolic Leadership AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 20px; background: #f0f8ff; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Neuro-Symbolic Leadership AI</h1>
            <div class="status">
                <h2>✅ Backend API Server Running</h2>
                <p>API Documentation: <a href="/docs">/docs</a></p>
                <p>Frontend should be running on: <a href="http://localhost:3000">http://localhost:3000</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.on_event("startup")
async def startup_event():
    """Initialize database and models on startup"""
    print("🚀 Starting Neuro-Symbolic Leadership AI...")
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Initialize database
    db_service = DatabaseService()
    await db_service.init_db()
    
    print("✅ Backend initialized successfully")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Neuro-Symbolic Leadership AI"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
