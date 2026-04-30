import time
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.models.schemas import (
    AssessmentInput, AssessmentResult, NeuralAnalysis, 
    LeadershipTrait, CulturalContext
)
from app.services.nlp_service import NLPService
from app.services.symbolic_reasoning_service import SymbolicReasoningService
from app.services.database_service import DatabaseService
from app.services.recommendation_service import RecommendationService
from app.core.config import settings

class AssessmentService:
    """Main assessment service combining neural and symbolic reasoning"""
    
    def __init__(self):
        self.nlp_service = NLPService()
        self.symbolic_service = SymbolicReasoningService()
        self.db_service = DatabaseService()
        self.recommendation_service = RecommendationService()
    
    async def perform_assessment(self, input_data: AssessmentInput) -> AssessmentResult:
        """Perform complete leadership assessment"""
        start_time = time.time()
        
        # Step 1: Neural Analysis
        neural_analysis = await self._perform_neural_analysis(input_data)
        
        # Step 2: Symbolic Reasoning
        symbolic_reasoning = await self._perform_symbolic_reasoning(
            input_data.culture, neural_analysis
        )
        
        # Step 3: Cultural Context Integration
        cultural_insights = await self._get_cultural_insights(input_data.culture)
        
        # Step 4: Generate Recommendations
        recommendations = await self._generate_recommendations(
            neural_analysis, symbolic_reasoning, cultural_insights
        )
        
        # Step 5: Calculate Final Scores
        final_traits = await self._calculate_final_traits(
            neural_analysis, symbolic_reasoning
        )
        
        # Step 6: Generate Explanations
        explanations = symbolic_reasoning.logic_explanations
        
        # Step 7: Calculate Overall Score
        overall_score = await self._calculate_overall_score(final_traits)
        
        processing_time = time.time() - start_time
        
        # Create assessment result
        result = AssessmentResult(
            user_id=input_data.user_id,
            overall_score=overall_score,
            traits=final_traits,
            cultural_insights=cultural_insights,
            neural_analysis=neural_analysis,
            symbolic_reasoning=symbolic_reasoning,
            recommendations=recommendations,
            explanations=explanations,
            processing_time=processing_time
        )
        
        # Save to database
        await self.db_service.save_assessment(result)
        
        return result
    
    async def _perform_neural_analysis(self, input_data: AssessmentInput) -> NeuralAnalysis:
        """Perform neural network analysis"""
        # Combine all text for analysis
        all_text = input_data.resume_text or ""
        all_text += " " + " ".join(input_data.responses)
        all_text += " " + " ".join(input_data.scenario_answers.values())
        
        # Generate embeddings
        embeddings = self.nlp_service.generate_embeddings([all_text])[0]
        
        # Analyze communication patterns
        communication_patterns = self.nlp_service.analyze_communication_style(all_text)
        
        # Detect leadership traits
        trait_indicators = self.nlp_service.detect_leadership_traits(all_text)
        
        # Calculate confidence scores based on text length and quality
        text_length = len(all_text.split())
        base_confidence = min(text_length / 100, 1.0)  # More text = higher confidence
        
        confidence_scores = {}
        for trait in settings.leadership_traits:
            confidence_scores[trait] = base_confidence * 0.8  # Base confidence
        
        # Adjust confidence based on communication clarity
        if communication_patterns.get("sentiment_positive", 0) > 50:
            for trait in confidence_scores:
                confidence_scores[trait] *= 1.1
        
        return NeuralAnalysis(
            embeddings=embeddings.tolist(),
            communication_patterns=communication_patterns,
            trait_indicators=trait_indicators,
            confidence_scores=confidence_scores
        )
    
    async def _perform_symbolic_reasoning(self, culture: str, 
                                        neural_analysis: NeuralAnalysis) -> Any:
        """Perform symbolic reasoning on neural analysis results"""
        return self.symbolic_service.perform_symbolic_reasoning(
            culture=culture,
            traits=neural_analysis.trait_indicators,
            communication=neural_analysis.communication_patterns
        )
    
    async def _get_cultural_insights(self, culture: str) -> Dict[str, Any]:
        """Get cultural context insights"""
        cultural_context = await self.db_service.get_cultural_context(culture)
        
        if not cultural_context:
            # Fallback to default cultural insights
            return {
                "culture": culture,
                "communication_style": {"directness": 0.5, "formality": 0.5},
                "leadership_expectations": {"autonomy": 0.5, "collaboration": 0.5},
                "cultural_norms": {"hierarchy": 0.5, "individualism": 0.5},
                "note": "Default cultural context used"
            }
        
        return cultural_context
    
    async def _generate_recommendations(self, neural_analysis: NeuralAnalysis,
                                      symbolic_reasoning: Any,
                                      cultural_insights: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        return await self.recommendation_service.generate_recommendations(
            neural_analysis.trait_indicators,
            symbolic_reasoning.cultural_adjustments,
            cultural_insights
        )
    
    async def _calculate_final_traits(self, neural_analysis: NeuralAnalysis,
                                     symbolic_reasoning: Any) -> List[LeadershipTrait]:
        """Calculate final trait scores combining neural and symbolic results"""
        final_traits = []
        
        base_traits = neural_analysis.trait_indicators
        cultural_adjustments = symbolic_reasoning.cultural_adjustments
        
        for trait_name in settings.leadership_traits:
            base_score = base_traits.get(trait_name, 0)
            cultural_score = cultural_adjustments.get(trait_name, base_score)
            
            # Weighted combination: 60% neural, 40% symbolic
            final_score = base_score * 0.6 + cultural_score * 0.4
            
            # Calculate confidence
            neural_confidence = neural_analysis.confidence_scores.get(trait_name, 0.5)
            symbolic_confidence = symbolic_reasoning.rule_confidence
            final_confidence = (neural_confidence + symbolic_confidence) / 2
            
            # Generate explanation
            explanation = f"{trait_name.replace('_', ' ').title()} score based on neural analysis ({base_score:.1f}) and cultural context adjustments ({cultural_score:.1f})"
            
            final_traits.append(LeadershipTrait(
                name=trait_name,
                score=min(100, max(0, final_score)),
                confidence=final_confidence,
                explanation=explanation
            ))
        
        return final_traits
    
    async def _calculate_overall_score(self, traits: List[LeadershipTrait]) -> float:
        """Calculate overall leadership score"""
        weighted_score = 0
        
        for trait in traits:
            weight = settings.trait_weight.get(trait.name, 0.125)  # Default weight
            weighted_score += trait.score * weight
        
        return min(100, max(0, weighted_score))
    
    async def compare_assessments(self, user_id: str, 
                                 assessment_ids: List[int]) -> Dict[str, Any]:
        """Compare multiple assessments for the same user"""
        assessments = []
        
        for assessment_id in assessment_ids:
            # This would typically fetch from database
            # For now, return placeholder
            pass
        
        return {
            "comparison": "Assessment comparison functionality",
            "user_id": user_id,
            "assessment_count": len(assessment_ids)
        }
    
    async def get_cultural_comparison(self, traits: Dict[str, float], 
                                    text: str) -> Dict[str, Any]:
        """Compare how the same traits would be evaluated across different cultures"""
        cultural_comparison = {}
        
        for culture in settings.supported_cultures:
            # Perform symbolic reasoning for each culture
            communication_patterns = self.nlp_service.analyze_communication_style(text)
            symbolic_result = self.symbolic_service.perform_symbolic_reasoning(
                culture, traits, communication_patterns
            )
            
            # Calculate adjusted scores
            adjusted_traits = {}
            for trait in settings.leadership_traits:
                base_score = traits.get(trait, 0)
                cultural_score = symbolic_result.cultural_adjustments.get(trait, base_score)
                adjusted_traits[trait] = base_score * 0.6 + cultural_score * 0.4
            
            # Calculate overall score for this culture
            overall_score = 0
            for trait, score in adjusted_traits.items():
                weight = settings.trait_weight.get(trait, 0.125)
                overall_score += score * weight
            
            cultural_comparison[culture] = {
                "overall_score": overall_score,
                "traits": adjusted_traits,
                "applied_rules": symbolic_result.applied_rules,
                "cultural_insights": symbolic_result.logic_explanations[:3]  # Top 3 insights
            }
        
        return cultural_comparison
    
    async def get_trait_development_plan(self, trait_name: str, 
                                       current_score: float) -> Dict[str, Any]:
        """Get detailed development plan for a specific trait"""
        return await self.recommendation_service.get_trait_development_plan(
            trait_name, current_score
        )
