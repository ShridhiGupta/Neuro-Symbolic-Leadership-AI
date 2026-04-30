from typing import Dict, List, Any
from app.core.config import settings

class RecommendationService:
    """Service for generating personalized leadership development recommendations"""
    
    def __init__(self):
        self.recommendation_database = self._initialize_recommendation_database()
        self.skill_development_plans = self._initialize_development_plans()
        self.cultural_training_resources = self._initialize_cultural_resources()
    
    def _initialize_recommendation_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive recommendation database"""
        return {
            "confidence": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Practice public speaking through Toastmasters or similar groups",
                        "Take on leadership roles in low-stakes projects",
                        "Seek feedback from trusted colleagues and mentors",
                        "Read 'The Confidence Code' by Katty Kay and Claire Shipman",
                        "Set and achieve small, incremental goals to build momentum"
                    ],
                    "resources": [
                        "Toastmasters International",
                        "Dale Carnegie Training",
                        "Harvard Business Review - Leadership Articles",
                        "TED Talks on Confidence"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Lead cross-functional projects",
                        "Mentor junior team members",
                        "Present in team meetings and company-wide forums",
                        "Take calculated risks and learn from outcomes",
                        "Develop decision-making frameworks"
                    ],
                    "resources": [
                        "Project Management Professional (PMP) Certification",
                        "Harvard Business School Online - Leadership Courses",
                        "MindTools - Leadership Resources"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Lead strategic initiatives",
                        "Speak at industry conferences",
                        "Develop other leaders through coaching",
                        "Take on high-visibility projects",
                        "Share expertise through writing or teaching"
                    ],
                    "resources": [
                        "Executive Education Programs",
                        "Industry Leadership Conferences",
                        "Executive Coaching Services"
                    ]
                }
            },
            "collaboration": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Join cross-functional teams",
                        "Practice active listening techniques",
                        "Learn conflict resolution strategies",
                        "Participate in team-building activities",
                        "Seek diverse perspectives on projects"
                    ],
                    "resources": [
                        "Crucial Conversations Training",
                        "The Five Dysfunctions of a Team - Book",
                        "Team Building Workshops"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Facilitate team meetings",
                        "Lead collaborative projects",
                        "Mentor team members",
                        "Create knowledge-sharing systems",
                        "Build networks across departments"
                    ],
                    "resources": [
                        "Facilitation Training Programs",
                        "Network Building Workshops",
                        "Collaboration Tools Training"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Lead organizational change initiatives",
                        "Build strategic partnerships",
                        "Develop ecosystem thinking",
                        "Create collaborative cultures",
                        "Influence across organizational boundaries"
                    ],
                    "resources": [
                        "Strategic Partnerships Courses",
                        "Organizational Development Programs",
                        "Executive Leadership Retreats"
                    ]
                }
            },
            "decision_making": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Learn decision-making frameworks (SWOT, Decision Matrix)",
                        "Practice making decisions with incomplete information",
                        "Study case studies of successful decisions",
                        "Develop analytical thinking skills",
                        "Seek mentorship from experienced decision-makers"
                    ],
                    "resources": [
                        "Decision Making Courses - Coursera",
                        "Thinking, Fast and Slow - Book",
                        "Harvard Business Review - Decision Making"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Lead projects requiring complex decisions",
                        "Develop data-driven decision processes",
                        "Create decision-making playbooks",
                        "Practice stakeholder management",
                        "Learn to balance speed and accuracy"
                    ],
                    "resources": [
                        "Data Analytics Courses",
                        "Stakeholder Management Training",
                        "Business Analysis Certification"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Make strategic organizational decisions",
                        "Develop decision governance frameworks",
                        "Lead crisis decision-making",
                        "Teach decision-making to others",
                        "Influence high-level strategic choices"
                    ],
                    "resources": [
                        "Strategic Management Programs",
                        "Crisis Leadership Training",
                        "Board Governance Courses"
                    ]
                }
            },
            "communication": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Join public speaking groups",
                        "Practice writing clear, concise emails",
                        "Learn storytelling techniques",
                        "Study non-verbal communication",
                        "Record and review your presentations"
                    ],
                    "resources": [
                        "Toastmasters International",
                        "Storytelling Workshops",
                        "Business Writing Courses"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Lead team communications",
                        "Present to senior leadership",
                        "Develop communication strategies",
                        "Master difficult conversations",
                        "Create compelling presentations"
                    ],
                    "resources": [
                        "Advanced Presentation Skills",
                        "Executive Communication Programs",
                        "Difficult Conversations Training"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Communicate organizational vision",
                        "Lead change communication",
                        "Develop executive presence",
                        "Speak at industry events",
                        "Create communication frameworks"
                    ],
                    "resources": [
                        "Executive Presence Coaching",
                        "Change Management Certification",
                        "Public Speaking Masterclasses"
                    ]
                }
            },
            "empathy": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Practice active listening",
                        "Learn about emotional intelligence",
                        "Seek diverse perspectives",
                        "Volunteer for community service",
                        "Read books on human psychology"
                    ],
                    "resources": [
                        "Emotional Intelligence 2.0 - Book",
                        "Active Listening Workshops",
                        "Diversity and Inclusion Training"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Mentor team members",
                        "Lead with emotional intelligence",
                        "Develop coaching skills",
                        "Create inclusive environments",
                        "Practice servant leadership"
                    ],
                    "resources": [
                        "Coaching Certification Programs",
                        "Servant Leadership Courses",
                        "Inclusive Leadership Training"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Lead organizational culture initiatives",
                        "Develop other leaders emotionally",
                        "Create psychologically safe environments",
                        "Champion diversity and inclusion",
                        "Build empathetic organizations"
                    ],
                    "resources": [
                        "Organizational Culture Programs",
                        "Advanced Coaching Certification",
                        "Diversity Leadership Programs"
                    ]
                }
            },
            "innovation": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Practice creative thinking exercises",
                        "Learn design thinking methodology",
                        "Study innovation case studies",
                        "Join innovation challenges",
                        "Experiment with new approaches"
                    ],
                    "resources": [
                        "Design Thinking Courses",
                        "Creativity Workshops",
                        "Innovation Management Books"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Lead innovation projects",
                        "Create new processes or products",
                        "Challenge existing assumptions",
                        "Build innovation teams",
                        "Develop innovation frameworks"
                    ],
                    "resources": [
                        "Innovation Management Programs",
                        "Lean Startup Methodology",
                        "Agile Innovation Courses"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Drive organizational innovation",
                        "Create innovation ecosystems",
                        "Lead industry disruption",
                        "Develop innovation culture",
                        "Speak on innovation topics"
                    ],
                    "resources": [
                        "Executive Innovation Programs",
                        "Innovation Ecosystem Building",
                        "Industry Thought Leadership"
                    ]
                }
            },
            "resilience": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Practice stress management techniques",
                        "Develop growth mindset",
                        "Build support networks",
                        "Learn from failures",
                        "Practice mindfulness and meditation"
                    ],
                    "resources": [
                        "Mindfulness-Based Stress Reduction",
                        "Growth Mindset - Carol Dweck",
                        "Resilience Training Programs"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Lead through organizational changes",
                        "Handle difficult situations gracefully",
                        "Support others through challenges",
                        "Develop crisis management skills",
                        "Build resilient teams"
                    ],
                    "resources": [
                        "Change Management Certification",
                        "Crisis Leadership Training",
                        "Team Resilience Programs"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Lead organizational transformations",
                        "Build resilient organizations",
                        "Coach others on resilience",
                        "Navigate major disruptions",
                        "Create adaptive cultures"
                    ],
                    "resources": [
                        "Organizational Transformation Programs",
                        "Executive Resilience Coaching",
                        "Adaptive Leadership Courses"
                    ]
                }
            },
            "strategic_thinking": {
                "low_score": {
                    "threshold": 40,
                    "recommendations": [
                        "Learn strategic planning frameworks",
                        "Study industry trends and competitors",
                        "Practice long-term planning",
                        "Read business strategy books",
                        "Analyze case studies of strategic decisions"
                    ],
                    "resources": [
                        "Strategic Planning Courses",
                        "Competitive Analysis Tools",
                        "Harvard Business Review Strategy"
                    ]
                },
                "medium_score": {
                    "threshold": 70,
                    "recommendations": [
                        "Develop departmental strategies",
                        "Lead strategic initiatives",
                        "Create strategic partnerships",
                        "Analyze market opportunities",
                        "Build strategic thinking teams"
                    ],
                    "resources": [
                        "Strategic Management Certification",
                        "Market Analysis Programs",
                        "Business Strategy Workshops"
                    ]
                },
                "high_score": {
                    "threshold": 85,
                    "recommendations": [
                        "Shape organizational strategy",
                        "Lead industry strategic discussions",
                        "Develop new business models",
                        "Create strategic visions",
                        "Influence industry direction"
                    ],
                    "resources": [
                        "Executive Strategy Programs",
                        "Industry Strategy Forums",
                        "Business Model Innovation"
                    ]
                }
            }
        }
    
    def _initialize_development_plans(self) -> Dict[str, Dict[str, Any]]:
        """Initialize detailed development plans"""
        return {
            "30_day_plan": {
                "focus": "Quick wins and foundational habits",
                "activities": [
                    "Daily reflection on leadership moments",
                    "Weekly reading of leadership articles",
                    "Practice one new skill each week",
                    "Seek feedback from 3 colleagues"
                ]
            },
            "90_day_plan": {
                "focus": "Skill building and relationship development",
                "activities": [
                    "Complete one online course",
                    "Lead a small project",
                    "Develop mentorship relationship",
                    "Create personal development plan"
                ]
            },
            "1_year_plan": {
                "focus": "Comprehensive leadership development",
                "activities": [
                    "Achieve certification in key area",
                    "Lead significant organizational initiative",
                    "Build professional network",
                    "Develop leadership coaching skills"
                ]
            }
        }
    
    def _initialize_cultural_resources(self) -> Dict[str, List[str]]:
        """Initialize cultural-specific learning resources"""
        return {
            "US": [
                "Harvard Business Review - American Leadership",
                "West Point Leadership Academy",
                "American Management Association Courses"
            ],
            "Japan": [
                "Japanese Management Techniques - Books",
                "Kaizen and Continuous Improvement Training",
                "Japanese Business Etiquette Courses"
            ],
            "India": [
                "Indian Leadership Case Studies - IIM",
                "Emerging Markets Leadership Programs",
                "Indian Business Culture Workshops"
            ],
            "Germany": [
                "German Business Leadership Academy",
                "Mittelstand Management Programs",
                "German Engineering Leadership Courses"
            ],
            "Brazil": [
                "Latin American Leadership Programs",
                "Brazilian Business Culture Training",
                "Emerging Markets Leadership Brazil"
            ]
        }
    
    async def generate_recommendations(self, traits: Dict[str, float],
                                      cultural_adjustments: Dict[str, float],
                                      cultural_insights: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on assessment results"""
        recommendations = []
        culture = cultural_insights.get("culture", "US")
        
        # Analyze each trait and generate recommendations
        for trait_name, score in traits.items():
            trait_recommendations = self._get_trait_recommendations(trait_name, score)
            recommendations.extend(trait_recommendations)
        
        # Add cultural-specific recommendations
        cultural_recommendations = self._get_cultural_recommendations(culture, traits)
        recommendations.extend(cultural_recommendations)
        
        # Add top priority recommendations
        priority_recommendations = self._get_priority_recommendations(traits)
        recommendations.extend(priority_recommendations)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def _get_trait_recommendations(self, trait_name: str, score: float) -> List[str]:
        """Get recommendations for a specific trait based on score"""
        if trait_name not in self.recommendation_database:
            return []
        
        trait_data = self.recommendation_database[trait_name]
        
        # Determine score level
        if score < trait_data["low_score"]["threshold"]:
            return trait_data["low_score"]["recommendations"][:2]
        elif score < trait_data["medium_score"]["threshold"]:
            return trait_data["medium_score"]["recommendations"][:2]
        else:
            return trait_data["high_score"]["recommendations"][:1]
    
    def _get_cultural_recommendations(self, culture: str, traits: Dict[str, float]) -> List[str]:
        """Get cultural-specific recommendations"""
        cultural_resources = self.cultural_training_resources.get(culture, [])
        
        # Find areas that need improvement based on cultural context
        recommendations = []
        
        if culture == "Japan":
            if traits.get("direct", 50) > 70:
                recommendations.append("Consider developing more indirect communication styles for Japanese context")
            if traits.get("collaboration", 50) < 60:
                recommendations.append("Focus on building harmony and group consensus")
        
        elif culture == "US":
            if traits.get("direct", 50) < 50:
                recommendations.append("Develop more direct communication style for US business context")
            if traits.get("innovation", 50) < 60:
                recommendations.append("Emphasize innovation and initiative in US leadership style")
        
        elif culture == "Germany":
            if traits.get("formal", 50) < 60:
                recommendations.append("Adopt more structured and formal approach for German context")
            if traits.get("strategic_thinking", 50) < 70:
                recommendations.append("Focus on long-term strategic planning")
        
        # Add cultural learning resources
        if cultural_resources:
            recommendations.append(f"Explore cultural leadership resources: {cultural_resources[0]}")
        
        return recommendations[:3]
    
    def _get_priority_recommendations(self, traits: Dict[str, float]) -> List[str]:
        """Get high-priority recommendations based on critical gaps"""
        recommendations = []
        
        # Find traits with lowest scores
        sorted_traits = sorted(traits.items(), key=lambda x: x[1])
        lowest_traits = sorted_traits[:2]
        
        for trait_name, score in lowest_traits:
            if score < 50:
                recommendations.append(f"Priority: Focus on improving {trait_name.replace('_', ' ')} - current score: {score:.1f}")
        
        # Check for critical leadership combinations
        confidence = traits.get("confidence", 0)
        decision_making = traits.get("decision_making", 0)
        
        if confidence < 50 and decision_making < 50:
            recommendations.append("Critical: Develop confidence and decision-making skills together for leadership effectiveness")
        
        return recommendations[:2]
    
    async def get_trait_development_plan(self, trait_name: str, current_score: float) -> Dict[str, Any]:
        """Get detailed development plan for a specific trait"""
        if trait_name not in self.recommendation_database:
            return {"error": "Trait not found"}
        
        trait_data = self.recommendation_database[trait_name]
        
        # Determine current level
        if current_score < trait_data["low_score"]["threshold"]:
            current_level = "low_score"
            target_level = "medium_score"
        elif current_score < trait_data["medium_score"]["threshold"]:
            current_level = "medium_score"
            target_level = "high_score"
        else:
            current_level = "high_score"
            target_level = "mastery"
        
        # Get current and target recommendations
        current_recommendations = trait_data[current_level]["recommendations"]
        target_recommendations = trait_data.get(target_level, {}).get("recommendations", [])
        
        # Create development timeline
        development_plan = {
            "trait": trait_name,
            "current_score": current_score,
            "current_level": current_level,
            "target_level": target_level,
            "immediate_actions": current_recommendations[:3],
            "next_steps": target_recommendations[:2],
            "timeline": self.development_plans,
            "resources": trait_data[current_level]["resources"],
            "success_metrics": [
                f"Increase {trait_name} score by 10 points",
                f"Receive positive feedback on {trait_name}",
                f"Successfully apply {trait_name} in real situations"
            ]
        }
        
        return development_plan
