from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class CultureEnum(str, Enum):
    """Supported cultural contexts"""
    US = "US"
    JAPAN = "Japan"
    INDIA = "India"
    GERMANY = "Germany"
    BRAZIL = "Brazil"
    CHINA = "China"
    UK = "UK"
    FRANCE = "France"
    CANADA = "Canada"
    AUSTRALIA = "Australia"

class LeadershipTrait(BaseModel):
    """Individual leadership trait score"""
    name: str
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    explanation: str

class CulturalContext(BaseModel):
    """Cultural context information"""
    culture: CultureEnum
    communication_style: Dict[str, Any]
    leadership_expectations: Dict[str, Any]
    cultural_norms: Dict[str, Any]

class AssessmentInput(BaseModel):
    """Input for leadership assessment"""
    user_id: Optional[str] = None
    culture: CultureEnum
    resume_text: Optional[str] = None
    responses: List[str] = Field(default_factory=list)
    scenario_answers: Dict[str, str] = Field(default_factory=dict)

class NeuralAnalysis(BaseModel):
    """Results from neural network analysis"""
    embeddings: List[float]
    communication_patterns: Dict[str, float]
    trait_indicators: Dict[str, float]
    confidence_scores: Dict[str, float]

class SymbolicReasoning(BaseModel):
    """Results from symbolic reasoning engine"""
    applied_rules: List[str]
    cultural_adjustments: Dict[str, float]
    logic_explanations: List[str]
    rule_confidence: float

class AssessmentResult(BaseModel):
    """Complete assessment result"""
    user_id: Optional[str] = None
    overall_score: float = Field(ge=0, le=100)
    traits: List[LeadershipTrait]
    cultural_insights: Dict[str, Any]
    neural_analysis: NeuralAnalysis
    symbolic_reasoning: SymbolicReasoning
    recommendations: List[str]
    explanations: List[str]
    assessment_date: datetime = Field(default_factory=datetime.now)
    processing_time: Optional[float] = None

class Recommendation(BaseModel):
    """Leadership development recommendation"""
    category: str
    priority: str  # high, medium, low
    action: str
    rationale: str
    resources: List[str] = Field(default_factory=list)

class FileUploadResponse(BaseModel):
    """Response for file upload"""
    filename: str
    file_size: int
    extracted_text: Optional[str] = None
    text_length: Optional[int] = None
    status: str
    message: str

class AnalysisRequest(BaseModel):
    """Request for detailed analysis"""
    text: str
    culture: CultureEnum
    analysis_type: str = "full"  # full, traits_only, cultural_only

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, str] = Field(default_factory=dict)

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
