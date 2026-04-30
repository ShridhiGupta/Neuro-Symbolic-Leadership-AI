from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import AnalysisRequest
from app.services.nlp_service import NLPService

router = APIRouter()
nlp_service = NLPService()

@router.post("/communication-style")
async def analyze_communication_style(text: str):
    """Analyze communication patterns from text"""
    try:
        analysis = nlp_service.analyze_communication_style(text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/leadership-traits")
async def analyze_leadership_traits(text: str):
    """Detect leadership traits from text"""
    try:
        traits = nlp_service.detect_leadership_traits(text)
        return {"traits": traits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/resume-extraction")
async def extract_resume_info(text: str):
    """Extract key information from resume text"""
    try:
        info = nlp_service.extract_text_from_resume(text)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@router.post("/text-features")
async def extract_text_features(text: str):
    """Extract comprehensive text features"""
    try:
        features = nlp_service.extract_text_features(text)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature extraction failed: {str(e)}")
