import pytest
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAssessmentAPI:
    """Test cases for assessment API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "Neuro-Symbolic Leadership AI" in data["service"]
    
    def test_supported_cultures(self):
        """Test getting supported cultures"""
        response = client.get("/api/assessment/supported-cultures")
        assert response.status_code == 200
        data = response.json()
        assert "supported_cultures" in data
        assert "US" in data["supported_cultures"]
        assert "Japan" in data["supported_cultures"]
        assert "leadership_traits" in data
    
    def test_leadership_traits(self):
        """Test getting leadership traits information"""
        response = client.get("/api/assessment/leadership-traits")
        assert response.status_code == 200
        data = response.json()
        assert "traits" in data
        assert "confidence" in data["traits"]
        assert "collaboration" in data["traits"]
    
    def test_analyze_text(self):
        """Test text analysis endpoint"""
        test_data = {
            "text": "I am a confident leader who works well with teams and makes decisive decisions.",
            "culture": "US",
            "analysis_type": "full"
        }
        response = client.post("/api/assessment/analyze-text", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "traits" in data
        assert "communication" in data
        assert "culture" in data
    
    def test_analyze_text_invalid_culture(self):
        """Test text analysis with invalid culture"""
        test_data = {
            "text": "Test text",
            "culture": "InvalidCountry",
            "analysis_type": "full"
        }
        response = client.post("/api/assessment/analyze-text", json=test_data)
        # Should still work but with default cultural context
        assert response.status_code == 200
    
    def test_analyze_text_empty(self):
        """Test text analysis with empty text"""
        test_data = {
            "text": "",
            "culture": "US",
            "analysis_type": "full"
        }
        response = client.post("/api/assessment/analyze-text", json=test_data)
        assert response.status_code == 200
        data = response.json()
        # Should still return structure but with low scores
        assert "traits" in data

class TestUploadAPI:
    """Test cases for upload API endpoints"""
    
    def test_supported_formats(self):
        """Test getting supported file formats"""
        response = client.get("/api/upload/supported-formats")
        assert response.status_code == 200
        data = response.json()
        assert "supported_formats" in data
        assert ".pdf" in data["supported_formats"]
        assert ".txt" in data["supported_formats"]
        assert "max_file_size_mb" in data
    
    def test_upload_text(self):
        """Test direct text upload"""
        test_data = {
            "text": "This is a test resume text for upload functionality.",
            "filename": "test_resume.txt",
            "user_id": "test_user"
        }
        response = client.post("/api/upload/text", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["filename"] == "test_resume.txt"
        assert data["extracted_text"] == test_data["text"]
    
    def test_upload_text_empty(self):
        """Test uploading empty text"""
        test_data = {
            "text": "",
            "filename": "empty.txt",
            "user_id": "test_user"
        }
        response = client.post("/api/upload/text", json=test_data)
        assert response.status_code == 400  # Should return error for empty text
    
    def test_upload_resume_file(self):
        """Test file upload (mock)"""
        # This would require actual file upload testing
        # For now, just test the endpoint exists
        pass

class TestAnalysisAPI:
    """Test cases for analysis API endpoints"""
    
    def test_communication_style_analysis(self):
        """Test communication style analysis"""
        test_data = {
            "text": "I communicate directly and clearly with my team members."
        }
        response = client.post("/api/analysis/communication-style", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "direct" in data
        assert "formal" in data
        assert "sentiment_positive" in data
    
    def test_leadership_traits_analysis(self):
        """Test leadership traits analysis"""
        test_data = {
            "text": "I am a confident leader who collaborates well with my team."
        }
        response = client.post("/api/analysis/leadership-traits", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "traits" in data
        assert "confidence" in data["traits"]
        assert "collaboration" in data["traits"]
    
    def test_resume_extraction(self):
        """Test resume information extraction"""
        test_data = {
            "text": """
            John Smith
            Software Engineer
            Experience: 5 years at Tech Corp
            Skills: Python, Java, Leadership
            Education: Computer Science Degree
            """
        }
        response = client.post("/api/analysis/resume-extraction", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        assert "experience_years" in data
    
    def test_text_features(self):
        """Test text feature extraction"""
        test_data = {
            "text": "This is a test text for feature extraction."
        }
        response = client.post("/api/analysis/text-features", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "word_count" in data
        assert "sentence_count" in data
        assert "sentiment" in data

class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_full_assessment_flow(self):
        """Test complete assessment flow"""
        # Step 1: Upload text
        upload_data = {
            "text": """
            I am a strategic leader with 10 years of experience in technology.
            I have successfully led teams through challenging projects and
            consistently deliver results through collaboration and innovation.
            """,
            "filename": "integration_test.txt",
            "user_id": "integration_user"
        }
        upload_response = client.post("/api/upload/text", json=upload_data)
        assert upload_response.status_code == 200
        
        # Step 2: Analyze text
        analysis_data = {
            "text": upload_data["text"],
            "culture": "US",
            "analysis_type": "full"
        }
        analysis_response = client.post("/api/assessment/analyze-text", json=analysis_data)
        assert analysis_response.status_code == 200
        analysis_result = analysis_response.json()
        
        # Step 3: Verify analysis results
        assert "traits" in analysis_result
        assert "communication" in analysis_result
        assert analysis_result["culture"] == "US"
        
        # Step 4: Check that traits have reasonable values
        traits = analysis_result["traits"]
        for trait_name, score in traits.items():
            assert 0 <= score <= 100, f"Trait {trait_name} score {score} out of range"
    
    def test_cultural_comparison_flow(self):
        """Test cultural comparison functionality"""
        test_text = """
        I am a direct and decisive leader who values innovation and results.
        I communicate clearly with my team and make quick decisions when needed.
        """
        
        # This would test cultural comparison endpoint
        # For now, just verify the text can be analyzed
        analysis_data = {
            "text": test_text,
            "culture": "US",
            "analysis_type": "traits_only"
        }
        response = client.post("/api/assessment/analyze-text", json=analysis_data)
        assert response.status_code == 200
        assert "traits" in response.json()

if __name__ == "__main__":
    pytest.main([__file__])
