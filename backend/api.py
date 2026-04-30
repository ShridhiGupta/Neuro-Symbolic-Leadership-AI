from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from datetime import datetime

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

# Health check endpoint
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

@app.get("/api/assessment/leadership-traits")
async def get_leadership_traits():
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
    text = request.get("text", "")
    culture = request.get("culture", "US")
    
    word_count = len(text.split())
    base_score = min(word_count / 2, 100)
    
    traits = SAMPLE_TRAITS.copy()
    if culture == "Japan":
        traits["collaboration"] += 10
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
    culture = request.get("culture", "US")
    resume_text = request.get("resume_text", "")
    responses = request.get("responses", [])
    
    overall_score = sum(SAMPLE_TRAITS.values()) / len(SAMPLE_TRAITS)
    
    if culture == "Japan":
        overall_score += 5
    elif culture == "US":
        overall_score += 3
    
    traits = []
    for trait_name, score in SAMPLE_TRAITS.items():
        traits.append({
            "name": trait_name,
            "score": score,
            "confidence": 0.85,
            "explanation": f"{trait_name.replace('_', ' ').title()} evaluated based on text analysis and cultural context"
        })
    
    recommendations = [
        f"Focus on improving {traits[-1]['name'].replace('_', ' ')} for better leadership outcomes",
        "Consider developing cross-cultural communication skills",
        "Practice strategic thinking in complex situations",
        "Build stronger collaborative relationships with team members"
    ]
    
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
            "embeddings": [0.1] * 384,
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
    text = request.get("text", "")
    filename = request.get("filename", "direct_text_input")
    user_id = request.get("user_id", "anonymous")
    
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

@app.get("/api/assessment/cultural-comparison/{user_id}")
async def get_cultural_comparison(user_id: str, text: str = ""):
    cultural_comparison = {}
    
    for culture in ["US", "Japan", "India"]:
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
    text = request.get("text", "")
    
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
    text = request.get("text", "")
    
    traits = SAMPLE_TRAITS.copy()
    
    if "confident" in text.lower():
        traits["confidence"] += 10
    if "team" in text.lower() or "collaborate" in text.lower():
        traits["collaboration"] += 10
    if "decide" in text.lower() or "decision" in text.lower():
        traits["decision_making"] += 10
    if "communicate" in text.lower():
        traits["communication"] += 10
    
    return {"traits": traits}

# Export the app for Vercel
handler = app
