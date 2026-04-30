from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import asyncio

from app.models.schemas import (
    AssessmentInput, AssessmentResult, AnalysisRequest,
    SuccessResponse, ErrorResponse
)
from app.services.assessment_service import AssessmentService

router = APIRouter()
assessment_service = AssessmentService()

@router.post("/evaluate", response_model=AssessmentResult)
async def evaluate_leadership(input_data: AssessmentInput):
    """
    Perform complete leadership assessment combining neural and symbolic reasoning
    
    - **culture**: Cultural context for evaluation
    - **resume_text**: Extracted text from resume
    - **responses**: List of written responses to leadership questions
    - **scenario_answers**: Dict of scenario-based answers
    """
    try:
        result = await assessment_service.perform_assessment(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@router.post("/analyze-text", response_model=Dict[str, Any])
async def analyze_text(request: AnalysisRequest):
    """
    Analyze text for leadership traits and communication patterns
    
    - **text**: Text to analyze
    - **culture**: Cultural context
    - **analysis_type**: Type of analysis (full, traits_only, cultural_only)
    """
    try:
        from app.services.nlp_service import NLPService
        from app.services.symbolic_reasoning_service import SymbolicReasoningService
        
        nlp_service = NLPService()
        symbolic_service = SymbolicReasoningService()
        
        # Perform neural analysis
        traits = nlp_service.detect_leadership_traits(request.text)
        communication = nlp_service.analyze_communication_style(request.text)
        
        result = {
            "traits": traits,
            "communication": communication,
            "culture": request.culture
        }
        
        # Add symbolic reasoning if requested
        if request.analysis_type in ["full", "cultural_only"]:
            symbolic_result = symbolic_service.perform_symbolic_reasoning(
                request.culture, traits, communication
            )
            result["symbolic_reasoning"] = symbolic_result.dict()
        
        # Add text features if full analysis
        if request.analysis_type == "full":
            features = nlp_service.extract_text_features(request.text)
            result["text_features"] = features
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

@router.get("/cultural-comparison/{user_id}")
async def get_cultural_comparison(user_id: str, text: str):
    """
    Compare how the same input would be evaluated across different cultures
    
    - **user_id**: User identifier
    - **text**: Text to analyze across cultures
    """
    try:
        # Get base traits from neural analysis
        from app.services.nlp_service import NLPService
        nlp_service = NLPService()
        base_traits = nlp_service.detect_leadership_traits(text)
        
        # Get cultural comparison
        comparison = await assessment_service.get_cultural_comparison(
            base_traits, text
        )
        
        return {
            "user_id": user_id,
            "base_traits": base_traits,
            "cultural_comparison": comparison,
            "insights": {
                "highest_scoring_culture": max(comparison.items(), key=lambda x: x[1]["overall_score"])[0],
                "lowest_scoring_culture": min(comparison.items(), key=lambda x: x[1]["overall_score"])[0],
                "cultural_variance": max([c["overall_score"] for c in comparison.values()]) - 
                                 min([c["overall_score"] for c in comparison.values()])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cultural comparison failed: {str(e)}")

@router.get("/trait-development/{trait_name}")
async def get_trait_development_plan(trait_name: str, current_score: float):
    """
    Get detailed development plan for a specific trait
    
    - **trait_name**: Name of the trait to develop
    - **current_score**: Current score for the trait (0-100)
    """
    try:
        development_plan = await assessment_service.get_trait_development_plan(
            trait_name, current_score
        )
        return development_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Development plan generation failed: {str(e)}")

@router.get("/user-assessments/{user_id}")
async def get_user_assessments(user_id: str):
    """
    Get all assessments for a specific user
    
    - **user_id**: User identifier
    """
    try:
        from app.services.database_service import DatabaseService
        db_service = DatabaseService()
        assessments = await db_service.get_user_assessments(user_id)
        
        return {
            "user_id": user_id,
            "assessments": assessments,
            "total_assessments": len(assessments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user assessments: {str(e)}")

@router.post("/compare-assessments")
async def compare_assessments(user_id: str, assessment_ids: List[int]):
    """
    Compare multiple assessments for the same user
    
    - **user_id**: User identifier
    - **assessment_ids**: List of assessment IDs to compare
    """
    try:
        comparison = await assessment_service.compare_assessments(user_id, assessment_ids)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment comparison failed: {str(e)}")

@router.get("/supported-cultures")
async def get_supported_cultures():
    """Get list of supported cultural contexts"""
    try:
        from app.core.config import settings
        return {
            "supported_cultures": settings.supported_cultures,
            "leadership_traits": settings.leadership_traits,
            "trait_weights": settings.trait_weight
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get supported cultures: {str(e)}")

@router.get("/leadership-traits")
async def get_leadership_traits():
    """Get information about leadership traits evaluated"""
    try:
        from app.core.config import settings
        trait_info = {}
        
        for trait in settings.leadership_traits:
            trait_info[trait] = {
                "weight": settings.trait_weight.get(trait, 0.125),
                "description": trait.replace('_', ' ').title()
            }
        
        return {
            "traits": trait_info,
            "total_traits": len(settings.leadership_traits),
            "scoring_method": "Neural analysis + Symbolic reasoning + Cultural context"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trait information: {str(e)}")
