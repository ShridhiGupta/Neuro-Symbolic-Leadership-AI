import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import asyncio

from app.models.schemas import AssessmentResult, CulturalContext

class DatabaseService:
    """Database service for SQLite operations"""
    
    def __init__(self):
        self.db_path = "data/leadership_assessment.db"
        self.init_db()
    
    async def init_db(self):
        """Initialize database tables"""
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                culture TEXT,
                overall_score REAL,
                traits TEXT,
                cultural_insights TEXT,
                neural_analysis TEXT,
                symbolic_reasoning TEXT,
                recommendations TEXT,
                explanations TEXT,
                assessment_date TEXT,
                processing_time REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create cultural_contexts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cultural_contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                culture TEXT UNIQUE,
                communication_style TEXT,
                leadership_expectations TEXT,
                cultural_norms TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                name TEXT,
                email TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create file_uploads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                filename TEXT,
                file_size INTEGER,
                extracted_text TEXT,
                text_length INTEGER,
                upload_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize cultural contexts
        await self._initialize_cultural_contexts()
    
    async def _initialize_cultural_contexts(self):
        """Initialize cultural context data"""
        cultural_data = {
            "US": {
                "communication_style": {
                    "directness": 0.8,
                    "formality": 0.4,
                    "context_level": 0.3,
                    "emotional_expression": 0.6
                },
                "leadership_expectations": {
                    "autonomy": 0.9,
                    "decisiveness": 0.8,
                    "innovation": 0.9,
                    "collaboration": 0.7
                },
                "cultural_norms": {
                    "hierarchy": 0.3,
                    "individualism": 0.9,
                    "risk_taking": 0.7,
                    "long_term_orientation": 0.4
                }
            },
            "Japan": {
                "communication_style": {
                    "directness": 0.2,
                    "formality": 0.9,
                    "context_level": 0.9,
                    "emotional_expression": 0.2
                },
                "leadership_expectations": {
                    "autonomy": 0.3,
                    "decisiveness": 0.5,
                    "innovation": 0.6,
                    "collaboration": 0.9
                },
                "cultural_norms": {
                    "hierarchy": 0.9,
                    "individualism": 0.3,
                    "risk_taking": 0.3,
                    "long_term_orientation": 0.8
                }
            },
            "India": {
                "communication_style": {
                    "directness": 0.5,
                    "formality": 0.7,
                    "context_level": 0.6,
                    "emotional_expression": 0.5
                },
                "leadership_expectations": {
                    "autonomy": 0.6,
                    "decisiveness": 0.7,
                    "innovation": 0.7,
                    "collaboration": 0.8
                },
                "cultural_norms": {
                    "hierarchy": 0.7,
                    "individualism": 0.5,
                    "risk_taking": 0.5,
                    "long_term_orientation": 0.6
                }
            },
            "Germany": {
                "communication_style": {
                    "directness": 0.8,
                    "formality": 0.6,
                    "context_level": 0.4,
                    "emotional_expression": 0.3
                },
                "leadership_expectations": {
                    "autonomy": 0.7,
                    "decisiveness": 0.9,
                    "innovation": 0.8,
                    "collaboration": 0.6
                },
                "cultural_norms": {
                    "hierarchy": 0.5,
                    "individualism": 0.8,
                    "risk_taking": 0.4,
                    "long_term_orientation": 0.7
                }
            },
            "Brazil": {
                "communication_style": {
                    "directness": 0.6,
                    "formality": 0.5,
                    "context_level": 0.7,
                    "emotional_expression": 0.8
                },
                "leadership_expectations": {
                    "autonomy": 0.5,
                    "decisiveness": 0.6,
                    "innovation": 0.7,
                    "collaboration": 0.8
                },
                "cultural_norms": {
                    "hierarchy": 0.6,
                    "individualism": 0.6,
                    "risk_taking": 0.7,
                    "long_term_orientation": 0.5
                }
            }
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for culture, data in cultural_data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO cultural_contexts 
                (culture, communication_style, leadership_expectations, cultural_norms)
                VALUES (?, ?, ?, ?)
            ''', (
                culture,
                json.dumps(data["communication_style"]),
                json.dumps(data["leadership_expectations"]),
                json.dumps(data["cultural_norms"])
            ))
        
        conn.commit()
        conn.close()
    
    async def save_assessment(self, result: AssessmentResult) -> int:
        """Save assessment result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO assessments 
            (user_id, culture, overall_score, traits, cultural_insights, 
             neural_analysis, symbolic_reasoning, recommendations, explanations, 
             assessment_date, processing_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.user_id,
            result.traits[0].name if result.traits else "Unknown",  # Simplified for now
            result.overall_score,
            json.dumps([trait.dict() for trait in result.traits]),
            json.dumps(result.cultural_insights),
            json.dumps(result.neural_analysis.dict()),
            json.dumps(result.symbolic_reasoning.dict()),
            json.dumps(result.recommendations),
            json.dumps(result.explanations),
            result.assessment_date.isoformat(),
            result.processing_time
        ))
        
        assessment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return assessment_id
    
    async def get_cultural_context(self, culture: str) -> Optional[Dict[str, Any]]:
        """Get cultural context data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT communication_style, leadership_expectations, cultural_norms
            FROM cultural_contexts WHERE culture = ?
        ''', (culture,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "culture": culture,
                "communication_style": json.loads(result[0]),
                "leadership_expectations": json.loads(result[1]),
                "cultural_norms": json.loads(result[2])
            }
        
        return None
    
    async def get_user_assessments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all assessments for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM assessments WHERE user_id = ? ORDER BY assessment_date DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        assessments = []
        for row in results:
            assessments.append({
                "id": row[0],
                "user_id": row[1],
                "culture": row[2],
                "overall_score": row[3],
                "assessment_date": row[10],
                "processing_time": row[11]
            })
        
        return assessments
    
    async def save_file_upload(self, user_id: str, filename: str, file_size: int, 
                             extracted_text: str) -> int:
        """Save file upload information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO file_uploads (user_id, filename, file_size, extracted_text, text_length)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, filename, file_size, extracted_text, len(extracted_text)))
        
        upload_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return upload_id
