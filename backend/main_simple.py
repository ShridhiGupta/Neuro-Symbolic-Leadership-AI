from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os
import json
from typing import Dict, Any
from datetime import datetime

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

# Sample data for demonstration
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

SAMPLE_CULTURAL_CONTEXTS = {
    "US": {
        "communication_style": {"directness": 0.8, "formality": 0.4},
        "leadership_expectations": {"autonomy": 0.9, "innovation": 0.9},
        "cultural_norms": {"individualism": 0.9, "risk_taking": 0.7}
    },
    "Japan": {
        "communication_style": {"directness": 0.2, "formality": 0.9},
        "leadership_expectations": {"collaboration": 0.9, "harmony": 0.9},
        "cultural_norms": {"hierarchy": 0.9, "group_harmony": 0.9}
    },
    "India": {
        "communication_style": {"directness": 0.5, "formality": 0.7},
        "leadership_expectations": {"relationship": 0.8, "hierarchy": 0.7},
        "cultural_norms": {"relationships": 0.8, "respect": 0.8}
    }
}

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
            .feature { margin: 10px 0; padding: 10px; background: #e8f5e8; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Neuro-Symbolic Leadership AI</h1>
            <div class="status">
                <h2>Backend API Server Running</h2>
                <p>API Documentation: <a href="/docs">/docs</a></p>
                <p>Frontend should be running on: <a href="http://localhost:3000">http://localhost:3000</a></p>
            </div>
            <h3>Available Features:</h3>
            <div class="feature">Leadership Assessment</div>
            <div class="feature">Cultural Context Analysis</div>
            <div class="feature">Text Upload & Processing</div>
            <div class="feature">Trait Analysis</div>
            <div class="feature">Cross-Cultural Comparison</div>
            <div class="feature">Recommendation System</div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Neuro-Symbolic Leadership AI",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/assessment/supported-cultures")
async def get_supported_cultures():
    """Get list of supported cultural contexts"""
    return {
        "supported_cultures": ["US", "Japan", "India", "Germany", "Brazil"],
        "leadership_traits": list(SAMPLE_TRAITS.keys()),
        "trait_weights": {trait: 0.125 for trait in SAMPLE_TRAITS.keys()}
    }

@app.get("/api/assessment/leadership-traits")
async def get_leadership_traits():
    """Get information about leadership traits evaluated"""
    trait_info = {}
    for trait, score in SAMPLE_TRAITS.items():
        trait_info[trait] = {
            "weight": 0.125,
            "description": trait.replace('_', ' ').title()
        }
    
    return {
        "traits": trait_info,
        "total_traits": len(SAMPLE_TRAITS),
        "scoring_method": "Neural analysis + Symbolic reasoning + Cultural context"
    }

@app.post("/api/assessment/analyze-text")
async def analyze_text(request: Dict[str, Any]):
    """Analyze text for leadership traits and communication patterns"""
    text = request.get("text", "")
    culture = request.get("culture", "US")
    
    # Simple mock analysis based on text length and keywords
    word_count = len(text.split())
    base_score = min(word_count / 2, 100)  # Simple scoring
    
    # Adjust traits based on cultural context
    traits = SAMPLE_TRAITS.copy()
    if culture == "Japan":
        traits["collaboration"] += 10
        traits["directness"] = max(traits.get("directness", 50) - 20, 0)
    elif culture == "US":
        traits["confidence"] += 10
        traits["innovation"] += 10
    
    communication_patterns = {
        "direct": 70 if "direct" in text.lower() else 50,
        "formal": 60 if "formal" in text.lower() else 40,
        "sentiment_positive": 80 if "good" in text.lower() or "great" in text.lower() else 60,
        "word_count": word_count
    }
    
    return {
        "traits": traits,
        "communication": communication_patterns,
        "culture": culture,
        "analysis_type": request.get("analysis_type", "full")
    }

@app.post("/api/assessment/evaluate")
async def evaluate_leadership(request: Dict[str, Any]):
    """Perform complete leadership assessment"""
    culture = request.get("culture", "US")
    resume_text = request.get("resume_text", "")
    responses = request.get("responses", [])
    
    # Generate mock assessment results
    overall_score = sum(SAMPLE_TRAITS.values()) / len(SAMPLE_TRAITS)
    
    # Adjust based on culture
    if culture == "Japan":
        overall_score += 5  # Bonus for cultural alignment
    elif culture == "US":
        overall_score += 3
    
    # Create trait list with explanations
    traits = []
    for trait_name, score in SAMPLE_TRAITS.items():
        traits.append({
            "name": trait_name,
            "score": score,
            "confidence": 0.85,
            "explanation": f"{trait_name.replace('_', ' ').title()} evaluated based on text analysis and cultural context"
        })
    
    # Generate recommendations
    recommendations = [
        f"Focus on improving {traits[-1]['name'].replace('_', ' ')} for better leadership outcomes",
        "Consider developing cross-cultural communication skills",
        "Practice strategic thinking in complex situations",
        "Build stronger collaborative relationships with team members"
    ]
    
    # Generate explanations
    explanations = [
        f"Analysis shows strong {traits[0]['name'].replace('_', ' ')} skills",
        f"Cultural context ({culture}) influences leadership effectiveness",
        "Communication patterns indicate clear and direct style",
        "Leadership potential demonstrated through experience and responses"
    ]
    
    return {
        "user_id": request.get("user_id", "demo_user"),
        "overall_score": min(overall_score, 100),
        "traits": traits,
        "cultural_insights": SAMPLE_CULTURAL_CONTEXTS.get(culture, SAMPLE_CULTURAL_CONTEXTS["US"]),
        "neural_analysis": {
            "embeddings": [0.1] * 384,  # Mock embedding
            "communication_patterns": {"direct": 70, "formal": 60},
            "trait_indicators": SAMPLE_TRAITS,
            "confidence_scores": {trait: 0.85 for trait in SAMPLE_TRAITS.keys()}
        },
        "symbolic_reasoning": {
            "applied_rules": ["cultural_context_adjustment", "leadership_pattern_analysis"],
            "cultural_adjustments": SAMPLE_TRAITS,
            "logic_explanations": explanations,
            "rule_confidence": 0.9
        },
        "recommendations": recommendations,
        "explanations": explanations,
        "assessment_date": datetime.now().isoformat(),
        "processing_time": 2.5
    }

@app.post("/api/upload/text")
async def upload_text(request: Dict[str, Any]):
    """Upload text directly"""
    text = request.get("text", "")
    filename = request.get("filename", "direct_text_input")
    user_id = request.get("user_id", "anonymous")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided")
    
    return {
        "filename": filename,
        "file_size": len(text.encode('utf-8')),
        "extracted_text": text,
        "text_length": len(text),
        "status": "success",
        "message": "Text uploaded successfully"
    }

@app.post("/api/upload/resume")
async def upload_resume():
    """Upload resume file (mock implementation)"""
    # Since we can't handle file uploads in this simplified version,
    # we'll return a mock response that simulates successful upload
    return {
        "filename": "sample_resume.pdf",
        "file_size": 1024000,  # 1MB
        "extracted_text": "Sample resume text for demonstration purposes. This is a mock response since file upload requires multipart form handling.",
        "text_length": 100,
        "status": "success",
        "message": "File uploaded and text extracted successfully (mock implementation)"
    }

@app.get("/api/upload/supported-formats")
async def get_supported_formats():
    """Get supported file formats"""
    return {
        "supported_formats": [".pdf", ".txt", ".docx"],
        "max_file_size_mb": 10,
        "upload_directory": "uploads"
    }

@app.get("/api/assessment/cultural-comparison/{user_id}")
async def get_cultural_comparison(user_id: str, text: str = ""):
    """Compare how the same input would be evaluated across different cultures"""
    cultural_comparison = {}
    
    for culture in ["US", "Japan", "India"]:
        # Adjust traits based on cultural context
        adjusted_traits = SAMPLE_TRAITS.copy()
        if culture == "Japan":
            adjusted_traits["collaboration"] += 15
            adjusted_traits["empathy"] += 10
        elif culture == "US":
            adjusted_traits["confidence"] += 15
            adjusted_traits["innovation"] += 10
        elif culture == "India":
            adjusted_traits["communication"] += 10
            adjusted_traits["strategic_thinking"] += 5
        
        overall_score = sum(adjusted_traits.values()) / len(adjusted_traits)
        
        cultural_comparison[culture] = {
            "overall_score": overall_score,
            "traits": adjusted_traits,
            "applied_rules": [f"cultural_adjustment_{culture.lower()}"],
            "cultural_insights": [f"Leadership style aligns well with {culture} cultural context"]
        }
    
    return {
        "user_id": user_id,
        "base_traits": SAMPLE_TRAITS,
        "cultural_comparison": cultural_comparison,
        "insights": {
            "highest_scoring_culture": max(cultural_comparison.items(), key=lambda x: x[1]["overall_score"])[0],
            "lowest_scoring_culture": min(cultural_comparison.items(), key=lambda x: x[1]["overall_score"])[0],
            "cultural_variance": max([c["overall_score"] for c in cultural_comparison.values()]) - 
                             min([c["overall_score"] for c in cultural_comparison.values()])
        }
    }

@app.get("/api/assessment/trait-development/{trait_name}")
async def get_trait_development_plan(trait_name: str, current_score: float = 70.0):
    """Get detailed development plan for a specific trait"""
    development_plan = {
        "trait": trait_name,
        "current_score": current_score,
        "current_level": "medium" if current_score > 60 else "low",
        "target_level": "high",
        "immediate_actions": [
            f"Practice {trait_name.replace('_', ' ')} in daily situations",
            f"Seek feedback on {trait_name.replace('_', ' ')} skills",
            f"Study examples of strong {trait_name.replace('_', ' ')} in leaders"
        ],
        "next_steps": [
            "Take on leadership challenges that require this trait",
            "Mentor others in developing this skill",
            "Read books and take courses on this topic"
        ],
        "resources": [
            "Leadership development courses",
            "Executive coaching programs",
            "Industry workshops and seminars"
        ],
        "success_metrics": [
            f"Increase {trait_name} score by 10 points",
            f"Receive positive feedback on {trait_name}",
            f"Successfully apply {trait_name} in real situations"
        ]
    }
    
    return development_plan

@app.post("/api/analysis/communication-style")
async def analyze_communication_style(request: Dict[str, Any]):
    """Analyze communication patterns from text"""
    text = request.get("text", "")
    
    # Simple mock analysis
    analysis = {
        "direct": 70 if "direct" in text.lower() else 50,
        "indirect": 30 if "indirect" in text.lower() else 50,
        "formal": 60 if "formal" in text.lower() else 40,
        "informal": 40 if "informal" in text.lower() else 60,
        "sentiment_positive": 80 if any(word in text.lower() for word in ["good", "great", "excellent"]) else 60,
        "sentiment_negative": 20 if any(word in text.lower() for word in ["bad", "poor", "terrible"]) else 10,
        "sentiment_neutral": 100 - (80 if any(word in text.lower() for word in ["good", "great", "excellent"]) else 60) - (20 if any(word in text.lower() for word in ["bad", "poor", "terrible"]) else 10)
    }
    
    return analysis

@app.post("/api/analysis/leadership-traits")
async def analyze_leadership_traits(request: Dict[str, Any]):
    """Detect leadership traits from text"""
    text = request.get("text", "")
    
    # Simple keyword-based trait detection
    traits = SAMPLE_TRAITS.copy()
    
    # Adjust based on keywords
    if "confident" in text.lower():
        traits["confidence"] += 10
    if "team" in text.lower() or "collaborate" in text.lower():
        traits["collaboration"] += 10
    if "decide" in text.lower() or "decision" in text.lower():
        traits["decision_making"] += 10
    if "communicate" in text.lower():
        traits["communication"] += 10
    
    return {"traits": traits}

if __name__ == "__main__":
    print("Starting Neuro-Symbolic Leadership AI Backend...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Frontend should run at: http://localhost:3000")
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
