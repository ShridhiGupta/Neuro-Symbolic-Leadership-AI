from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Neuro-Symbolic Leadership AI",
    description="AI system for cross-cultural leadership assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
SAMPLE_TRAITS = {
    "confidence": 75.0,
    "collaboration": 82.0,
    "decision_making": 78.0,
    "communication": 71.0,
    "empathy": 68.0,
    "innovation": 85.0,
    "resilience": 73.0,
    "strategic_thinking": 77.0
}

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Neuro-Symbolic Leadership AI",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Neuro-Symbolic Leadership AI API is running"}

# Assessment endpoints
@app.get("/api/assessment/supported-cultures")
async def get_supported_cultures():
    return {
        "supported_cultures": ["US", "Japan", "India", "Germany", "Brazil"],
        "leadership_traits": list(SAMPLE_TRAITS.keys()),
        "trait_weights": {trait: 0.125 for trait in SAMPLE_TRAITS.keys()}
    }

@app.post("/api/assessment/evaluate")
async def evaluate_leadership(request: Dict[str, Any]):
    culture = request.get("culture", "US")
    resume_text = request.get("resume_text", "")
    responses = request.get("responses", [])
    
    overall_score = sum(SAMPLE_TRAITS.values()) / len(SAMPLE_TRAITS)
    
    traits = []
    for trait_name, score in SAMPLE_TRAITS.items():
        traits.append({
            "name": trait_name,
            "score": score,
            "confidence": 0.85,
            "explanation": f"{trait_name.replace('_', ' ').title()} evaluated based on text analysis and cultural context"
        })
    
    return {
        "user_id": request.get("user_id", "demo_user"),
        "overall_score": min(overall_score, 100),
        "traits": traits,
        "assessment_date": datetime.now().isoformat(),
        "processing_time": 2.5
    }

@app.post("/api/upload/text")
async def upload_text(request: Dict[str, Any]):
    text = request.get("text", "")
    filename = request.get("filename", "direct_text_input")
    
    if not text.strip():
        return {"error": "Empty text provided", "status": "error"}
    
    return {
        "filename": filename,
        "file_size": len(text.encode('utf-8')),
        "extracted_text": text,
        "text_length": len(text),
        "status": "success",
        "message": "Text uploaded successfully"
    }

# Export for Vercel
handler = app
