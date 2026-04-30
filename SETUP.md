# 🚀 Setup Guide: Neuro-Symbolic Leadership AI System

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.9 or higher
- **Node.js**: 16.0 or higher
- **npm**: 7.0 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: Minimum 2GB free space

### Required Software
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

## 🛠️ Installation Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd neuro-symbolic-leadership-ai
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2.3 Download NLP Models
```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
"
```

#### 2.4 Initialize Database
```bash
# The database will be automatically created when you first run the application
# This will create a SQLite database in the backend/data/ directory
```

#### 2.5 Test Backend Installation
```bash
python main.py
```

You should see output indicating the server is running on `http://localhost:8000`

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory
```bash
cd frontend
```

#### 3.2 Install Node.js Dependencies
```bash
npm install
```

#### 3.3 Test Frontend Installation
```bash
npm start
```

The frontend should open automatically in your browser at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Backend Configuration
DEBUG=True
DATABASE_URL=sqlite:///./data/leadership_assessment.db
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Frontend Configuration (create .env in frontend directory)
REACT_APP_API_URL=http://localhost:8000
```

### Custom Configuration

Edit `backend/app/core/config.py` to modify:

- Supported cultures
- Leadership traits weights
- Model configurations
- File upload settings

## 🚀 Running the Application

### Method 1: Development Mode (Recommended)

#### Terminal 1: Backend Server
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

#### Terminal 2: Frontend Server
```bash
cd frontend
npm start
```

### Method 2: Production Mode

#### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm run build
# Serve the build directory with your preferred web server
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
cd backend
python -m pytest tests/test_api.py -v
```

## 📊 First Run Verification

### 1. Check Backend Health
Open your browser and navigate to:
```
http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "Neuro-Symbolic Leadership AI",
  "version": "1.0.0"
}
```

### 2. Check API Documentation
Navigate to:
```
http://localhost:8000/docs
```

You should see the FastAPI interactive documentation.

### 3. Check Frontend
Navigate to:
```
http://localhost:3000
```

You should see the Neuro-Symbolic Leadership AI dashboard.

### 4. Test Sample Assessment

1. Navigate to the Assessment page
2. Select a cultural context (e.g., "US")
3. Paste sample text from `backend/data/sample_resumes.txt`
4. Complete the assessment steps
5. View your results

## 🔍 Troubleshooting

### Common Issues

#### 1. Python Module Installation Errors
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific versions if needed
pip install fastapi==0.104.1 uvicorn==0.24.0
```

#### 2. spaCy Model Download Issues
```bash
# Try downloading manually
python -m spacy download en_core_web_sm --user

# Or use alternative model
python -m spacy download en_core_web_lg
```

#### 3. Frontend Build Errors
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. Port Conflicts
```bash
# Check what's using port 8000
netstat -tulpn | grep :8000

# Kill the process
kill -9 <PID>

# Or use different ports
python main.py --port 8001
```

#### 5. Database Issues
```bash
# Delete and recreate database
rm backend/data/leadership_assessment.db
python main.py  # Will recreate automatically
```

### Performance Issues

#### 1. Slow Model Loading
- Ensure you have sufficient RAM (8GB+ recommended)
- Consider using a smaller sentence transformer model
- Close other memory-intensive applications

#### 2. Slow API Responses
- Check system resources
- Monitor CPU and memory usage
- Consider reducing text input size for testing

## 📚 Sample Data Usage

### Using Sample Resumes
1. Open `backend/data/sample_resumes.txt`
2. Copy any resume sample
3. Paste it in the Upload or Assessment page
4. Run the assessment to see sample results

### Using Sample Responses
1. Open `backend/data/sample_responses.txt`
2. Copy leadership responses
3. Use them in the assessment form
4. Compare results across different cultural contexts

## 🔒 Security Considerations

### Development Mode
- The setup uses default configurations suitable for development
- No authentication is implemented in the basic setup

### Production Deployment
- Implement proper authentication
- Use HTTPS
- Set up proper CORS policies
- Implement rate limiting
- Use environment variables for sensitive data

## 📈 Performance Optimization

### Backend Optimization
```bash
# Install with performance packages
pip install uvloop  # For better async performance

# Use production server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Optimization
```bash
# Build for production
npm run build

# Analyze bundle size
npm run analyze
```

## 🤝 Contributing

### Development Workflow
1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request

### Code Style
- Backend: Follow PEP 8
- Frontend: Use ESLint configuration
- Add comments for complex logic
- Update documentation

## 📞 Support

### Getting Help
1. Check this setup guide
2. Review the troubleshooting section
3. Check the API documentation at `/docs`
4. Look at the sample data for examples

### Common Questions
- **Q: Can I use different models?** A: Yes, modify the configuration in `config.py`
- **Q: How do I add new cultures?** A: Update the cultural rules in the symbolic reasoning service
- **Q: Can I customize the traits?** A: Yes, modify the trait definitions and weights in the configuration

## 🎯 Next Steps

After successful setup:

1. **Explore the Dashboard**: View sample assessments and analytics
2. **Try Cultural Comparison**: Compare the same text across different cultures
3. **Test Trait Development**: Get personalized recommendations
4. **Review API Documentation**: Understand all available endpoints
5. **Customize Configuration**: Adapt the system to your needs

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**🎉 Congratulations!** Your Neuro-Symbolic Leadership AI system is now ready to use.
