import spacy
import re
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

class NLPService:
    """Natural Language Processing service for text analysis"""
    
    def __init__(self):
        # Load models
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Leadership keywords for trait detection
        self.leadership_keywords = {
            "confidence": [
                "confident", "sure", "certain", "believe", "assured", "self-assured",
                "decisive", "definite", "positive", "strong", "capable"
            ],
            "collaboration": [
                "team", "together", "cooperation", "partnership", "collaborate",
                "support", "help", "share", "collective", "joint", "synergy"
            ],
            "decision_making": [
                "decide", "decision", "choice", "choose", "determine", "resolve",
                "conclude", "settle", "judgment", "verdict", "conclusion"
            ],
            "communication": [
                "communicate", "express", "convey", "articulate", "explain",
                "present", "speak", "listen", "discuss", "dialogue", "clear"
            ],
            "empathy": [
                "understand", "feel", "compassion", "care", "support",
                "listen", "empathize", "concern", "sensitive", "aware"
            ],
            "innovation": [
                "innovate", "creative", "new", "original", "breakthrough",
                "invent", "design", "imagine", "transform", "revolutionary"
            ],
            "resilience": [
                "persist", "resilient", "overcome", "recover", "bounce back",
                "endure", "persevere", "tough", "strong", "adapt"
            ],
            "strategic_thinking": [
                "strategy", "plan", "vision", "long-term", "goal", "objective",
                "analyze", "evaluate", "assess", "forecast", "anticipate"
            ]
        }
        
        # Communication style indicators
        self.communication_indicators = {
            "direct": [
                "direct", "straightforward", "clear", "explicit", "frank",
                "honest", "blunt", "straight", "to the point"
            ],
            "indirect": [
                "suggest", "imply", "hint", "subtle", "gentle", "polite",
                "diplomatic", "tactful", "considerate"
            ],
            "formal": [
                "formal", "professional", "respectful", "proper", "official",
                "business", "corporate", "structured"
            ],
            "informal": [
                "casual", "friendly", "relaxed", "comfortable", "natural",
                "easy-going", "approachable"
            ]
        }
    
    def extract_text_from_resume(self, text: str) -> Dict[str, Any]:
        """Extract key information from resume text"""
        doc = self.nlp(text)
        
        # Extract entities
        entities = {
            "persons": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
            "locations": [ent.text for ent in doc.ents if ent.label_ == "GPE"],
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
            "skills": [],
            "experience_years": []
        }
        
        # Extract skills using common patterns
        skill_patterns = [
            r'\b(Python|Java|JavaScript|React|Node\.js|SQL|AWS|Docker|Kubernetes)\b',
            r'\b(Leadership|Management|Project Management|Agile|Scrum)\b',
            r'\b(Communication|Teamwork|Problem Solving|Analytical)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["skills"].extend(matches)
        
        # Extract years of experience
        experience_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        matches = re.findall(experience_pattern, text, re.IGNORECASE)
        entities["experience_years"] = [int(match) for match in matches]
        
        return entities
    
    def analyze_communication_style(self, text: str) -> Dict[str, float]:
        """Analyze communication style from text"""
        doc = self.nlp(text)
        
        # Calculate style scores
        style_scores = {}
        
        for style, keywords in self.communication_indicators.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of keyword and its variations
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            
            # Normalize by text length
            style_scores[style] = min(score / len(doc) * 100, 100)
        
        # Analyze sentence structure
        sentences = list(doc.sents)
        if sentences:
            avg_sentence_length = np.mean([len(sent) for sent in sentences])
            style_scores["sentence_complexity"] = min(avg_sentence_length / 20 * 100, 100)
        else:
            style_scores["sentence_complexity"] = 0
        
        # Sentiment analysis
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        style_scores["sentiment_positive"] = sentiment["pos"] * 100
        style_scores["sentiment_negative"] = sentiment["neg"] * 100
        style_scores["sentiment_neutral"] = sentiment["neu"] * 100
        
        return style_scores
    
    def detect_leadership_traits(self, text: str) -> Dict[str, float]:
        """Detect leadership traits from text using keyword analysis and embeddings"""
        doc = self.nlp(text)
        text_lower = text.lower()
        
        trait_scores = {}
        
        # Keyword-based scoring
        for trait, keywords in self.leadership_keywords.items():
            score = 0
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            # Normalize by text length
            trait_scores[trait] = min(score / len(doc) * 100, 100)
        
        # Embedding-based similarity scoring
        try:
            # Get text embedding
            text_embedding = self.sentence_model.encode([text])[0]
            
            # Compare with trait embeddings (using keyword-based representations)
            for trait in self.leadership_keywords.keys():
                trait_keywords = ' '.join(self.leadership_keywords[trait])
                trait_embedding = self.sentence_model.encode([trait_keywords])[0]
                
                # Calculate cosine similarity
                similarity = cosine_similarity(
                    text_embedding.reshape(1, -1),
                    trait_embedding.reshape(1, -1)
                )[0][0]
                
                # Combine keyword and embedding scores
                trait_scores[trait] = (trait_scores[trait] + similarity * 100) / 2
        
        except Exception as e:
            print(f"Embedding analysis failed: {e}")
        
        return trait_scores
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate sentence embeddings for texts"""
        return self.sentence_model.encode(texts)
    
    def extract_text_features(self, text: str) -> Dict[str, Any]:
        """Extract comprehensive text features"""
        doc = self.nlp(text)
        
        features = {
            # Basic text statistics
            "word_count": len([token for token in doc if not token.is_space]),
            "sentence_count": len(list(doc.sents)),
            "paragraph_count": text.count('\n\n') + 1,
            "avg_sentence_length": np.mean([len(sent) for sent in doc.sents]) if list(doc.sents) else 0,
            
            # Part-of-speech distribution
            "pos_distribution": {
                "nouns": len([token for token in doc if token.pos_ == "NOUN"]),
                "verbs": len([token for token in doc if token.pos_ == "VERB"]),
                "adjectives": len([token for token in doc if token.pos_ == "ADJ"]),
                "adverbs": len([token for token in doc if token.pos_ == "ADV"])
            },
            
            # Readability metrics
            "flesch_reading_ease": self._calculate_flesch_reading_ease(text),
            
            # Named entities
            "entity_count": len(list(doc.ents)),
            
            # Sentiment
            "sentiment": self.sentiment_analyzer.polarity_scores(text)
        }
        
        return features
    
    def _calculate_flesch_reading_ease(self, text: str) -> float:
        """Calculate Flesch reading ease score"""
        doc = self.nlp(text)
        sentences = list(doc.sents)
        
        if not sentences:
            return 0
        
        total_words = len([token for token in doc if not token.is_space])
        total_sentences = len(sentences)
        total_syllables = sum(self._count_syllables(token.text) for token in doc if not token.is_space)
        
        if total_words == 0 or total_sentences == 0:
            return 0
        
        flesch = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        return max(0, min(100, flesch))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified version)"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_char_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    syllable_count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False
        
        # Remove silent 'e' at the end
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def analyze_responses(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze multiple responses together"""
        all_text = ' '.join(responses)
        
        analysis = {
            "overall_traits": self.detect_leadership_traits(all_text),
            "communication_style": self.analyze_communication_style(all_text),
            "text_features": self.extract_text_features(all_text),
            "individual_analyses": []
        }
        
        # Analyze each response individually
        for i, response in enumerate(responses):
            individual_analysis = {
                "response_id": i,
                "traits": self.detect_leadership_traits(response),
                "communication_style": self.analyze_communication_style(response),
                "sentiment": self.sentiment_analyzer.polarity_scores(response)
            }
            analysis["individual_analyses"].append(individual_analysis)
        
        return analysis
