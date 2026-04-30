# 🏗️ System Architecture Documentation

## Overview

The Neuro-Symbolic Leadership AI system combines neural networks with symbolic reasoning to provide culturally-aware leadership assessments. This document outlines the complete system architecture, components, and data flow.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Engine     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Database      │    │   Local Models  │
                       │   (SQLite)      │    │   (Transformers)│
                       └─────────────────┘    └─────────────────┘
```

## Component Architecture

### 1. Frontend Layer (React)

**Purpose**: User interface and data visualization

**Components**:
- **Header**: Navigation and user interface
- **Dashboard**: Analytics and overview
- **Assessment**: Multi-step assessment form
- **Upload**: File upload and text input
- **CulturalComparison**: Cross-cultural analysis
- **TraitDevelopment**: Personalized recommendations

**Key Technologies**:
- React 18 with hooks
- Material-UI for components
- Chart.js/Recharts for visualization
- Axios for API communication
- React Router for navigation

### 2. Backend API Layer (FastAPI)

**Purpose**: HTTP API and business logic orchestration

**Components**:
- **API Routes**: RESTful endpoints
- **Request/Response Models**: Pydantic schemas
- **Middleware**: CORS, authentication, error handling
- **Service Layer**: Business logic coordination

**Key Technologies**:
- FastAPI for high-performance API
- Pydantic for data validation
- Uvicorn for ASGI server
- SQLAlchemy for database ORM

### 3. AI Engine Layer

**Purpose**: Core AI processing and reasoning

**Components**:
- **NLP Service**: Text processing and feature extraction
- **Neural Analysis**: Embedding generation and trait detection
- **Symbolic Reasoning**: Rule-based cultural adaptation
- **Recommendation Service**: Personalized development plans

**Key Technologies**:
- spaCy for NLP processing
- Sentence Transformers for embeddings
- Custom rule engine for symbolic reasoning
- NumPy/Scikit-learn for numerical operations

## Data Flow Architecture

### Assessment Flow

```
User Input → Frontend → API → NLP Service → Neural Analysis → Symbolic Reasoning → Results → Frontend
```

**Detailed Flow**:

1. **Input Collection**
   - Resume text (PDF/TXT upload or direct input)
   - Leadership scenario responses
   - Cultural context selection

2. **Neural Processing**
   - Text preprocessing and cleaning
   - Embedding generation (all-MiniLM-L6-v2)
   - Trait detection using keyword analysis + embeddings
   - Communication style analysis

3. **Symbolic Reasoning**
   - Cultural rule application
   - Leadership pattern evaluation
   - Communication style adjustment
   - Explainable logic generation

4. **Result Integration**
   - Combine neural and symbolic outputs
   - Generate overall scores
   - Create recommendations
   - Format for frontend display

### File Upload Flow

```
File Upload → API → Text Extraction → Database → Assessment → Results
```

**Detailed Flow**:

1. **File Reception**
   - Multi-part form data handling
   - File validation (type, size)
   - Temporary storage

2. **Text Extraction**
   - PDF processing with PyMuPDF
   - TXT file reading
   - DOCX parsing (basic)
   - Text cleaning and normalization

3. **Storage**
   - Database record creation
   - File metadata storage
   - Extracted text storage

## Service Architecture

### NLP Service

```python
class NLPService:
    """Natural Language Processing service"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def detect_leadership_traits(self, text: str) -> Dict[str, float]
    def analyze_communication_style(self, text: str) -> Dict[str, float]
    def extract_text_from_resume(self, text: str) -> Dict[str, Any]
    def generate_embeddings(self, texts: List[str]) -> np.ndarray
```

**Key Methods**:
- **Trait Detection**: Keyword analysis + embedding similarity
- **Communication Analysis**: Directness, formality, sentiment
- **Resume Extraction**: Skills, experience, entities
- **Feature Extraction**: Readability, complexity, structure

### Symbolic Reasoning Service

```python
class SymbolicReasoningService:
    """Symbolic reasoning engine for cultural context"""
    
    def __init__(self):
        self.cultural_rules = self._initialize_cultural_rules()
        self.leadership_rules = self._initialize_leadership_rules()
    
    def apply_cultural_rules(self, culture: str, traits: Dict, communication: Dict)
    def apply_leadership_rules(self, traits: Dict) -> Tuple[Dict, List[str]]
    def perform_symbolic_reasoning(self, culture: str, traits: Dict, communication: Dict)
```

**Rule Categories**:
- **Cultural Rules**: Culture-specific trait adjustments
- **Leadership Rules**: Trait combination patterns
- **Communication Rules**: Style effectiveness evaluation

### Assessment Service

```python
class AssessmentService:
    """Main assessment service combining neural and symbolic reasoning"""
    
    async def perform_assessment(self, input_data: AssessmentInput) -> AssessmentResult
    async def _perform_neural_analysis(self, input_data: AssessmentInput) -> NeuralAnalysis
    async def _perform_symbolic_reasoning(self, culture: str, neural_analysis: NeuralAnalysis)
    async def _calculate_final_traits(self, neural_analysis: NeuralAnalysis, symbolic_reasoning: Any)
```

## Database Architecture

### Schema Design

```sql
-- Assessments Table
CREATE TABLE assessments (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    culture TEXT,
    overall_score REAL,
    traits TEXT,  -- JSON
    cultural_insights TEXT,  -- JSON
    neural_analysis TEXT,  -- JSON
    symbolic_reasoning TEXT,  -- JSON
    recommendations TEXT,  -- JSON
    explanations TEXT,  -- JSON
    assessment_date TEXT,
    processing_time REAL
);

-- Cultural Contexts Table
CREATE TABLE cultural_contexts (
    id INTEGER PRIMARY KEY,
    culture TEXT UNIQUE,
    communication_style TEXT,  -- JSON
    leadership_expectations TEXT,  -- JSON
    cultural_norms TEXT  -- JSON
);

-- File Uploads Table
CREATE TABLE file_uploads (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    filename TEXT,
    file_size INTEGER,
    extracted_text TEXT,
    text_length INTEGER,
    upload_date TEXT
);
```

### Data Relationships

- **Users** → **Assessments** (1:N)
- **Assessments** → **File Uploads** (1:N, optional)
- **Cultural Contexts** → **Assessments** (1:N)

## Model Architecture

### Neural Components

#### 1. Sentence Transformer Model
- **Model**: all-MiniLM-L6-v2
- **Purpose**: Text embedding generation
- **Input**: Text strings
- **Output**: 384-dimensional vectors
- **Advantages**: Lightweight, fast, good performance

#### 2. spaCy NLP Pipeline
- **Model**: en_core_web_sm
- **Purpose**: Text processing and entity extraction
- **Components**: Tokenization, POS tagging, NER, dependency parsing
- **Advantages**: Fast, accurate, comprehensive

#### 3. Custom Neural Features
- **TF-IDF Vectorization**: Feature extraction
- **Sentiment Analysis**: VADER sentiment scoring
- **Readability Metrics**: Flesch reading ease

### Symbolic Components

#### 1. Cultural Rule Engine
```python
cultural_rules = {
    "US": {
        "direct_communication_positive": {
            "condition": lambda traits, comm: comm.get("direct", 0) > 60,
            "effect": {"confidence": 0.2, "decision_making": 0.15},
            "explanation": "Direct communication is valued in US leadership culture"
        }
    }
}
```

#### 2. Leadership Pattern Rules
```python
leadership_rules = [
    {
        "name": "confidence_with_collaboration",
        "condition": lambda traits: traits.get("confidence", 0) > 70 and traits.get("collaboration", 0) > 60,
        "effect": {"overall": 0.1, "leadership_potential": 0.15},
        "explanation": "High confidence combined with collaboration indicates strong leadership potential"
    }
]
```

## Security Architecture

### Authentication & Authorization
- **Development**: No authentication (simplified setup)
- **Production**: JWT-based authentication recommended
- **API Keys**: For external integrations

### Data Privacy
- **Local Processing**: No external API calls
- **Data Storage**: SQLite database (local)
- **File Handling**: Temporary files with cleanup

### Input Validation
- **File Upload**: Type, size, content validation
- **Text Input**: Length limits, sanitization
- **API Parameters**: Pydantic model validation

## Performance Architecture

### Optimization Strategies

#### Backend Optimization
1. **Model Caching**: Load models once at startup
2. **Async Processing**: FastAPI async endpoints
3. **Database Indexing**: Optimize query performance
4. **Connection Pooling**: Efficient database connections

#### Frontend Optimization
1. **Code Splitting**: Lazy loading of components
2. **Memoization**: React.memo for expensive renders
3. **Virtualization**: For large data lists
4. **Caching**: API response caching

#### AI Model Optimization
1. **Model Selection**: Lightweight models chosen for speed
2. **Batch Processing**: Process multiple texts together
3. **Feature Caching**: Cache expensive computations
4. **Approximation**: Use faster methods for large texts

### Scalability Considerations

#### Horizontal Scaling
- **API Servers**: Multiple FastAPI instances behind load balancer
- **Database**: SQLite for development, PostgreSQL for production
- **File Storage**: Cloud storage for production

#### Vertical Scaling
- **Memory**: Models require ~2GB RAM
- **CPU**: Multi-core processing for parallel analysis
- **Storage**: SSD for faster database operations

## Monitoring & Logging

### Application Monitoring
- **Health Checks**: `/health` endpoint
- **Performance Metrics**: Request timing, processing time
- **Error Tracking**: Exception logging and reporting

### AI Model Monitoring
- **Model Performance**: Accuracy, confidence scores
- **Processing Time**: Neural vs symbolic components
- **Resource Usage**: Memory, CPU utilization

### Business Metrics
- **Assessment Completion Rate**
- **User Engagement**
- **Cultural Comparison Usage**
- **Trait Development Plan Access**

## Deployment Architecture

### Development Environment
```
Local Machine
├── Backend (Python 3.9+)
├── Frontend (Node.js 16+)
├── Database (SQLite)
└── Models (Local files)
```

### Production Environment
```
Cloud Infrastructure
├── Load Balancer
├── API Servers (Multiple instances)
├── Database (PostgreSQL)
├── File Storage (S3/Cloud Storage)
├── Monitoring (Prometheus/Grafana)
└── Logging (ELK Stack)
```

### Container Architecture
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
```

## Integration Architecture

### External Integrations
- **File Processing**: PyMuPDF for PDF, python-docx for DOCX
- **Model Downloads**: Hugging Face Transformers
- **NLP Libraries**: spaCy, NLTK, TextBlob

### API Integrations
- **Frontend → Backend**: RESTful API calls
- **Backend → Database**: SQLAlchemy ORM
- **Services → Models**: Direct Python imports

### Future Integrations
- **Cloud Storage**: AWS S3, Google Cloud Storage
- **Authentication**: OAuth 2.0, SAML
- **Monitoring**: New Relic, DataDog
- **Analytics**: Google Analytics, Mixpanel

## Testing Architecture

### Testing Layers
1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Service interaction testing
3. **API Tests**: Endpoint testing
4. **End-to-End Tests**: Full user journey testing

### Test Frameworks
- **Backend**: pytest, pytest-asyncio
- **Frontend**: Jest, React Testing Library
- **API**: FastAPI TestClient
- **E2E**: Cypress (future implementation)

### Test Data
- **Sample Resumes**: Various cultural contexts
- **Sample Responses**: Leadership scenarios
- **Mock Data**: Synthetic test cases
- **Edge Cases**: Error conditions, boundary values

---

This architecture documentation provides a comprehensive overview of the Neuro-Symbolic Leadership AI system. For implementation details, refer to the specific component documentation and source code.
