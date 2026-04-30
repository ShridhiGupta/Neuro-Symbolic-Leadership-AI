from typing import Dict, List, Any, Tuple
from app.models.schemas import CultureEnum, SymbolicReasoning
import json

class SymbolicReasoningService:
    """Symbolic reasoning engine for cultural context and rule-based evaluation"""
    
    def __init__(self):
        # Initialize cultural rules
        self.cultural_rules = self._initialize_cultural_rules()
        
        # Leadership trait rules
        self.leadership_rules = self._initialize_leadership_rules()
        
        # Communication style rules
        self.communication_rules = self._initialize_communication_rules()
    
    def _initialize_cultural_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cultural context rules"""
        return {
            "US": {
                "direct_communication_positive": {
                    "condition": lambda traits, comm: comm.get("direct", 0) > 60,
                    "effect": {"confidence": 0.2, "decision_making": 0.15},
                    "explanation": "Direct communication is valued in US leadership culture"
                },
                "informal_style_positive": {
                    "condition": lambda traits, comm: comm.get("informal", 0) > 50,
                    "effect": {"collaboration": 0.1, "communication": 0.15},
                    "explanation": "Informal approach fosters teamwork in US context"
                },
                "individual_achievement_focus": {
                    "condition": lambda traits, comm: traits.get("confidence", 0) > 70,
                    "effect": {"innovation": 0.15, "strategic_thinking": 0.1},
                    "explanation": "Individual initiative is encouraged in US leadership"
                }
            },
            "Japan": {
                "indirect_communication_positive": {
                    "condition": lambda traits, comm: comm.get("indirect", 0) > 60,
                    "effect": {"empathy": 0.2, "collaboration": 0.15},
                    "explanation": "Indirect communication shows respect and harmony in Japanese culture"
                },
                "formal_style_positive": {
                    "condition": lambda traits, comm: comm.get("formal", 0) > 70,
                    "effect": {"communication": 0.15, "strategic_thinking": 0.1},
                    "explanation": "Formality demonstrates respect for hierarchy in Japan"
                },
                "group_harmony_focus": {
                    "condition": lambda traits, comm: traits.get("collaboration", 0) > 60,
                    "effect": {"empathy": 0.15, "resilience": 0.1},
                    "explanation": "Group harmony is prioritized in Japanese leadership"
                },
                "direct_communication_negative": {
                    "condition": lambda traits, comm: comm.get("direct", 0) > 70,
                    "effect": {"communication": -0.1, "empathy": -0.15},
                    "explanation": "Excessive directness may be perceived as rude in Japanese culture"
                }
            },
            "India": {
                "respectful_communication": {
                    "condition": lambda traits, comm: comm.get("formal", 0) > 50 and comm.get("indirect", 0) > 40,
                    "effect": {"communication": 0.15, "empathy": 0.1},
                    "explanation": "Balanced respectful communication works well in Indian context"
                },
                "relationship_building": {
                    "condition": lambda traits, comm: traits.get("collaboration", 0) > 60,
                    "effect": {"empathy": 0.15, "communication": 0.1},
                    "explanation": "Relationship building is crucial in Indian leadership"
                },
                "hierarchy_respect": {
                    "condition": lambda traits, comm: comm.get("formal", 0) > 60,
                    "effect": {"strategic_thinking": 0.1, "decision_making": 0.15},
                    "explanation": "Respect for hierarchy is important in Indian organizations"
                }
            },
            "Germany": {
                "direct_communication_positive": {
                    "condition": lambda traits, comm: comm.get("direct", 0) > 70,
                    "effect": {"communication": 0.2, "decision_making": 0.15},
                    "explanation": "Directness is valued for clarity in German business culture"
                },
                "structured_approach": {
                    "condition": lambda traits, comm: comm.get("formal", 0) > 60,
                    "effect": {"strategic_thinking": 0.2, "decision_making": 0.15},
                    "explanation": "Structured approach aligns with German leadership expectations"
                },
                "efficiency_focus": {
                    "condition": lambda traits, comm: traits.get("decision_making", 0) > 70,
                    "effect": {"innovation": 0.1, "strategic_thinking": 0.15},
                    "explanation": "Efficiency and results are prioritized in German leadership"
                }
            },
            "Brazil": {
                "relationship_oriented": {
                    "condition": lambda traits, comm: traits.get("collaboration", 0) > 60 and comm.get("empathy", 0) > 50,
                    "effect": {"communication": 0.15, "collaboration": 0.2},
                    "explanation": "Relationship orientation is key in Brazilian leadership"
                },
                "flexible_communication": {
                    "condition": lambda traits, comm: comm.get("informal", 0) > 50,
                    "effect": {"collaboration": 0.15, "innovation": 0.1},
                    "explanation": "Flexible communication style works well in Brazilian context"
                },
                "emotional_expression_positive": {
                    "condition": lambda traits, comm: comm.get("sentiment_positive", 0) > 60,
                    "effect": {"empathy": 0.2, "communication": 0.1},
                    "explanation": "Emotional expression is accepted in Brazilian culture"
                }
            }
        }
    
    def _initialize_leadership_rules(self) -> List[Dict[str, Any]]:
        """Initialize leadership evaluation rules"""
        return [
            {
                "name": "confidence_with_collaboration",
                "condition": lambda traits: traits.get("confidence", 0) > 70 and traits.get("collaboration", 0) > 60,
                "effect": {"overall": 0.1, "leadership_potential": 0.15},
                "explanation": "High confidence combined with collaboration indicates strong leadership potential"
            },
            {
                "name": "strategic_with_innovation",
                "condition": lambda traits: traits.get("strategic_thinking", 0) > 70 and traits.get("innovation", 0) > 60,
                "effect": {"overall": 0.1, "visionary_leadership": 0.2},
                "explanation": "Strategic thinking paired with innovation suggests visionary leadership"
            },
            {
                "name": "communication_with_empathy",
                "condition": lambda traits: traits.get("communication", 0) > 70 and traits.get("empathy", 0) > 60,
                "effect": {"overall": 0.1, "people_leadership": 0.15},
                "explanation": "Strong communication combined with empathy indicates effective people leadership"
            },
            {
                "name": "resilience_with_decision_making",
                "condition": lambda traits: traits.get("resilience", 0) > 70 and traits.get("decision_making", 0) > 60,
                "effect": {"overall": 0.1, "crisis_leadership": 0.2},
                "explanation": "Resilience combined with decision-making ability suggests strong crisis leadership"
            },
            {
                "name": "low_confidence_with_high_collaboration",
                "condition": lambda traits: traits.get("confidence", 0) < 50 and traits.get("collaboration", 0) > 70,
                "effect": {"confidence": 0.15, "communication": 0.1},
                "explanation": "High collaboration can compensate for lower confidence"
            },
            {
                "name": "high_innovation_low_strategic",
                "condition": lambda traits: traits.get("innovation", 0) > 70 and traits.get("strategic_thinking", 0) < 50,
                "effect": {"strategic_thinking": 0.1, "decision_making": 0.05},
                "explanation": "Innovation should be balanced with strategic thinking"
            }
        ]
    
    def _initialize_communication_rules(self) -> List[Dict[str, Any]]:
        """Initialize communication style evaluation rules"""
        return [
            {
                "name": "balanced_directness",
                "condition": lambda comm: 40 < comm.get("direct", 0) < 80,
                "effect": {"communication": 0.1},
                "explanation": "Balanced directness in communication is generally effective"
            },
            {
                "name": "excessive_formality",
                "condition": lambda comm: comm.get("formal", 0) > 85,
                "effect": {"communication": -0.1, "collaboration": -0.05},
                "explanation": "Excessive formality may hinder open communication"
            },
            {
                "name": "too_informal",
                "condition": lambda comm: comm.get("informal", 0) > 85,
                "effect": {"communication": -0.05, "strategic_thinking": -0.1},
                "explanation": "Too informal may lack professional credibility"
            },
            {
                "name": "positive_sentiment_advantage",
                "condition": lambda comm: comm.get("sentiment_positive", 0) > 60,
                "effect": {"communication": 0.1, "collaboration": 0.1},
                "explanation": "Positive sentiment enhances communication effectiveness"
            },
            {
                "name": "negative_sentiment_impact",
                "condition": lambda comm: comm.get("sentiment_negative", 0) > 40,
                "effect": {"communication": -0.1, "empathy": -0.05},
                "explanation": "High negative sentiment may affect team dynamics"
            }
        ]
    
    def apply_cultural_rules(self, culture: str, traits: Dict[str, float], 
                          communication: Dict[str, float]) -> Tuple[Dict[str, float], List[str]]:
        """Apply cultural context rules to adjust trait scores"""
        if culture not in self.cultural_rules:
            return traits, ["No specific cultural rules for this culture"]
        
        adjusted_traits = traits.copy()
        applied_rules = []
        cultural_rules = self.cultural_rules[culture]
        
        for rule_name, rule in cultural_rules.items():
            try:
                if rule["condition"](traits, communication):
                    # Apply rule effects
                    for trait, effect in rule["effect"].items():
                        if trait in adjusted_traits:
                            adjusted_traits[trait] = max(0, min(100, adjusted_traits[trait] + effect * 100))
                    
                    applied_rules.append(rule["explanation"])
            except Exception as e:
                print(f"Error applying rule {rule_name}: {e}")
        
        return adjusted_traits, applied_rules
    
    def apply_leadership_rules(self, traits: Dict[str, float]) -> Tuple[Dict[str, float], List[str]]:
        """Apply leadership evaluation rules"""
        adjusted_traits = traits.copy()
        applied_rules = []
        
        for rule in self.leadership_rules:
            try:
                if rule["condition"](traits):
                    # Apply rule effects
                    for trait, effect in rule["effect"].items():
                        if trait in adjusted_traits:
                            adjusted_traits[trait] = max(0, min(100, adjusted_traits[trait] + effect * 100))
                    
                    applied_rules.append(rule["explanation"])
            except Exception as e:
                print(f"Error applying leadership rule {rule['name']}: {e}")
        
        return adjusted_traits, applied_rules
    
    def apply_communication_rules(self, communication: Dict[str, float]) -> Tuple[Dict[str, float], List[str]]:
        """Apply communication style rules"""
        adjusted_communication = communication.copy()
        applied_rules = []
        
        for rule in self.communication_rules:
            try:
                if rule["condition"](communication):
                    # Apply rule effects
                    for trait, effect in rule["effect"].items():
                        if trait in adjusted_communication:
                            adjusted_communication[trait] = max(0, min(100, adjusted_communication[trait] + effect * 100))
                    
                    applied_rules.append(rule["explanation"])
            except Exception as e:
                print(f"Error applying communication rule {rule['name']}: {e}")
        
        return adjusted_communication, applied_rules
    
    def evaluate_leadership_potential(self, traits: Dict[str, float], 
                                    cultural_adjustments: Dict[str, float]) -> Dict[str, Any]:
        """Evaluate overall leadership potential"""
        # Calculate weighted score
        weights = {
            "confidence": 0.15,
            "collaboration": 0.15,
            "decision_making": 0.15,
            "communication": 0.15,
            "empathy": 0.10,
            "innovation": 0.10,
            "resilience": 0.10,
            "strategic_thinking": 0.10
        }
        
        weighted_score = 0
        for trait, weight in weights.items():
            trait_score = cultural_adjustments.get(trait, traits.get(trait, 0))
            weighted_score += trait_score * weight
        
        # Determine leadership level
        if weighted_score >= 85:
            leadership_level = "Executive Level"
        elif weighted_score >= 75:
            leadership_level = "Senior Management"
        elif weighted_score >= 65:
            leadership_level = "Middle Management"
        elif weighted_score >= 55:
            leadership_level = "Junior Management"
        else:
            leadership_level = "Individual Contributor"
        
        # Identify strengths and areas for improvement
        sorted_traits = sorted(cultural_adjustments.items(), key=lambda x: x[1], reverse=True)
        strengths = [trait for trait, score in sorted_traits[:3] if score > 70]
        improvements = [trait for trait, score in sorted_traits[-3:] if score < 60]
        
        return {
            "overall_score": weighted_score,
            "leadership_level": leadership_level,
            "strengths": strengths,
            "areas_for_improvement": improvements,
            "trait_ranking": sorted_traits
        }
    
    def generate_explanations(self, traits: Dict[str, float], cultural_rules: List[str], 
                            leadership_rules: List[str], communication_rules: List[str]) -> List[str]:
        """Generate comprehensive explanations for the evaluation"""
        explanations = []
        
        # Add cultural explanations
        if cultural_rules:
            explanations.append("Cultural Context Adjustments:")
            explanations.extend([f"- {rule}" for rule in cultural_rules])
        
        # Add leadership explanations
        if leadership_rules:
            explanations.append("\nLeadership Pattern Analysis:")
            explanations.extend([f"- {rule}" for rule in leadership_rules])
        
        # Add communication explanations
        if communication_rules:
            explanations.append("\nCommunication Style Insights:")
            explanations.extend([f"- {rule}" for rule in communication_rules])
        
        # Add trait-specific explanations
        explanations.append("\nTrait Analysis:")
        for trait, score in traits.items():
            if score >= 80:
                explanations.append(f"- {trait.replace('_', ' ').title()}: Excellent ({score:.1f}/100)")
            elif score >= 60:
                explanations.append(f"- {trait.replace('_', ' ').title()}: Good ({score:.1f}/100)")
            elif score >= 40:
                explanations.append(f"- {trait.replace('_', ' ').title()}: Moderate ({score:.1f}/100)")
            else:
                explanations.append(f"- {trait.replace('_', ' ').title()}: Needs Development ({score:.1f}/100)")
        
        return explanations
    
    def perform_symbolic_reasoning(self, culture: str, traits: Dict[str, float], 
                                 communication: Dict[str, float]) -> SymbolicReasoning:
        """Perform complete symbolic reasoning analysis"""
        # Apply different rule sets
        cultural_adjustments, cultural_rules = self.apply_cultural_rules(culture, traits, communication)
        leadership_adjustments, leadership_rules = self.apply_leadership_rules(traits)
        communication_adjustments, communication_rules = self.apply_communication_rules(communication)
        
        # Combine all adjustments
        final_traits = traits.copy()
        for trait in final_traits:
            final_traits[trait] = (
                traits[trait] * 0.4 +  # Original neural analysis
                cultural_adjustments.get(trait, traits[trait]) * 0.3 +  # Cultural adjustments
                leadership_adjustments.get(trait, traits[trait]) * 0.3  # Leadership rule adjustments
            )
        
        # Generate explanations
        all_explanations = self.generate_explanations(
            final_traits, cultural_rules, leadership_rules, communication_rules
        )
        
        # Calculate rule confidence
        total_rules = len(cultural_rules) + len(leadership_rules) + len(communication_rules)
        rule_confidence = min(total_rules / 10, 1.0)  # Normalize to 0-1
        
        return SymbolicReasoning(
            applied_rules=cultural_rules + leadership_rules + communication_rules,
            cultural_adjustments=cultural_adjustments,
            logic_explanations=all_explanations,
            rule_confidence=rule_confidence
        )
