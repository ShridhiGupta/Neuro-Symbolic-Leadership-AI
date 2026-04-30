from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Neuro-Symbolic Leadership AI"
    debug: bool = True
    version: str = "1.0.0"
    
    # Database
    database_url: str = "sqlite:///./data/leadership_assessment.db"
    
    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "uploads"
    allowed_extensions: list = [".pdf", ".txt", ".docx"]
    
    # AI Model Configuration
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    spacy_model: str = "en_core_web_sm"
    
    # Cultural Context
    supported_cultures: list = [
        "US", "Japan", "India", "Germany", "Brazil", 
        "China", "UK", "France", "Canada", "Australia"
    ]
    
    # Leadership Traits
    leadership_traits: list = [
        "confidence", "collaboration", "decision_making",
        "communication", "empathy", "innovation", 
        "resilience", "strategic_thinking"
    ]
    
    # Scoring Configuration
    max_score: int = 100
    trait_weight: dict = {
        "confidence": 0.15,
        "collaboration": 0.15,
        "decision_making": 0.15,
        "communication": 0.15,
        "empathy": 0.10,
        "innovation": 0.10,
        "resilience": 0.10,
        "strategic_thinking": 0.10
    }
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
