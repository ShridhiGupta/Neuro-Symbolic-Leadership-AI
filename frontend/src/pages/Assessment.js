import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Divider,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Psychology,
  Upload,
  Assessment as AssessmentIcon,
  TrendingUp,
  ArrowForward,
  CheckCircle,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

import api from '../services/api';

const LeadershipAssessment = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [formData, setFormData] = useState({
    culture: 'US',
    resumeText: '',
    responses: ['', '', ''],
    scenarioAnswers: {},
  });

  const navigate = useNavigate();

  const steps = [
    'Cultural Context',
    'Resume Upload',
    'Leadership Responses',
    'Scenario Questions',
    'Results',
  ];

  const leadershipQuestions = [
    "Describe a situation where you had to lead a team through a difficult challenge. What was your approach and what was the outcome?",
    "How do you balance the need for decisive action with the importance of team collaboration?",
    "Tell me about a time when you had to adapt your leadership style to work with different team members or cultural contexts.",
  ];

  const scenarioQuestions = [
    {
      id: 'conflict_resolution',
      question: "Two team members have conflicting approaches to a project. How do you handle this situation?",
    },
    {
      id: 'change_management',
      question: "Your team is resistant to a major organizational change. What steps do you take?",
    },
    {
      id: 'resource_allocation',
      question: "You have limited resources but multiple important projects. How do you prioritize and allocate?",
    },
  ];

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      setActiveStep(0);
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleResponseChange = (index, value) => {
    const newResponses = [...formData.responses];
    newResponses[index] = value;
    setFormData((prev) => ({
      ...prev,
      responses: newResponses,
    }));
  };

  const handleScenarioChange = (scenarioId, value) => {
    setFormData((prev) => ({
      ...prev,
      scenarioAnswers: {
        ...prev.scenarioAnswers,
        [scenarioId]: value,
      },
    }));
  };

  const handleSubmitAssessment = async () => {
    try {
      setLoading(true);
      setError(null);

      const assessmentData = {
        culture: formData.culture,
        resume_text: formData.resumeText,
        responses: formData.responses.filter(r => r.trim() !== ''),
        scenario_answers: formData.scenarioAnswers,
      };

      const result = await api.post('/api/assessment/evaluate', assessmentData);
      setAssessmentResult(result.data);
      setActiveStep(4); // Move to results step
    } catch (err) {
      setError('Assessment failed. Please try again.');
      console.error('Assessment error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRadarData = (traits) => {
    return traits.map(trait => ({
      trait: trait.name.replace('_', ' ').toUpperCase(),
      score: trait.score,
      fullMark: 100,
    }));
  };

  const getTraitBarData = (traits) => {
    return traits.map(trait => ({
      trait: trait.name.replace('_', ' ').toUpperCase(),
      score: trait.score,
      confidence: trait.confidence * 100,
    }));
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Cultural Context
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Select the cultural context for your leadership assessment. This will help us provide culturally relevant insights.
            </Typography>
            <FormControl fullWidth>
              <InputLabel>Cultural Context</InputLabel>
              <Select
                value={formData.culture}
                onChange={(e) => handleInputChange('culture', e.target.value)}
                label="Cultural Context"
              >
                <MenuItem value="US">United States</MenuItem>
                <MenuItem value="Japan">Japan</MenuItem>
                <MenuItem value="India">India</MenuItem>
                <MenuItem value="Germany">Germany</MenuItem>
                <MenuItem value="Brazil">Brazil</MenuItem>
                <MenuItem value="China">China</MenuItem>
                <MenuItem value="UK">United Kingdom</MenuItem>
                <MenuItem value="France">France</MenuItem>
                <MenuItem value="Canada">Canada</MenuItem>
                <MenuItem value="Australia">Australia</MenuItem>
              </Select>
            </FormControl>
            <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="body2">
                <strong>Selected Culture:</strong> {formData.culture}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                The assessment will be tailored to {formData.culture} leadership expectations and cultural norms.
              </Typography>
            </Box>
          </Paper>
        );

      case 1:
        return (
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Resume Information
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Paste your resume text or upload a file. This helps us understand your background and experience.
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={8}
              label="Resume Text"
              value={formData.resumeText}
              onChange={(e) => handleInputChange('resumeText', e.target.value)}
              placeholder="Paste your resume text here..."
              sx={{ mb: 2 }}
            />
            <Button
              variant="outlined"
              startIcon={<Upload />}
              onClick={() => navigate('/upload')}
              sx={{ mb: 2 }}
            >
              Upload Resume File
            </Button>
            {formData.resumeText && (
              <Box sx={{ p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
                <Typography variant="body2">
                  <CheckCircle sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Resume text added ({formData.resumeText.length} characters)
                </Typography>
              </Box>
            )}
          </Paper>
        );

      case 2:
        return (
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Leadership Experience
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Please answer the following questions about your leadership experience.
            </Typography>
            {leadershipQuestions.map((question, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Question {index + 1}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {question}
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={formData.responses[index]}
                  onChange={(e) => handleResponseChange(index, e.target.value)}
                  placeholder="Type your response here..."
                />
              </Box>
            ))}
          </Paper>
        );

      case 3:
        return (
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Leadership Scenarios
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              How would you handle these common leadership challenges?
            </Typography>
            {scenarioQuestions.map((scenario) => (
              <Box key={scenario.id} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  {scenario.id.replace('_', ' ').toUpperCase()}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {scenario.question}
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  value={formData.scenarioAnswers[scenario.id] || ''}
                  onChange={(e) => handleScenarioChange(scenario.id, e.target.value)}
                  placeholder="Describe your approach..."
                />
              </Box>
            ))}
          </Paper>
        );

      case 4:
        return assessmentResult ? (
          <Box>
            <Paper sx={{ p: 4, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Assessment Results
              </Typography>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h4" color="primary">
                  Overall Score: {assessmentResult.overall_score.toFixed(1)}/100
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={assessmentResult.overall_score}
                  sx={{ mt: 1, height: 10, borderRadius: 5 }}
                />
              </Box>
              <Typography variant="body2" color="text.secondary">
                Culture: {formData.culture} | Processing Time: {assessmentResult.processing_time?.toFixed(2)}s
              </Typography>
            </Paper>

            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Leadership Traits Radar
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={getRadarData(assessmentResult.traits)}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="trait" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      <Radar
                        name="Score"
                        dataKey="score"
                        stroke="#1976d2"
                        fill="#1976d2"
                        fillOpacity={0.6}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>

              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Trait Breakdown
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getTraitBarData(assessmentResult.traits)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="trait" angle={-45} textAnchor="end" height={80} />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="score" fill="#1976d2" name="Score" />
                      <Bar dataKey="confidence" fill="#dc004e" name="Confidence %" />
                    </BarChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>

              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Top Strengths
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    {assessmentResult.traits
                      .sort((a, b) => b.score - a.score)
                      .slice(0, 3)
                      .map((trait, index) => (
                        <Chip
                          key={index}
                          label={`${trait.name.replace('_', ' ').toUpperCase()}: ${trait.score.toFixed(1)}`}
                          color="success"
                          variant="outlined"
                        />
                      ))}
                  </Box>
                </Paper>
              </Grid>

              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Areas for Development
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    {assessmentResult.traits
                      .sort((a, b) => a.score - b.score)
                      .slice(0, 3)
                      .map((trait, index) => (
                        <Chip
                          key={index}
                          label={`${trait.name.replace('_', ' ').toUpperCase()}: ${trait.score.toFixed(1)}`}
                          color="warning"
                          variant="outlined"
                        />
                      ))}
                  </Box>
                </Paper>
              </Grid>

              <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Key Insights
                  </Typography>
                  {assessmentResult.explanations.slice(0, 5).map((explanation, index) => (
                    <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                      • {explanation}
                    </Typography>
                  ))}
                </Paper>
              </Grid>

              <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Personalized Recommendations
                  </Typography>
                  {assessmentResult.recommendations.slice(0, 5).map((recommendation, index) => (
                    <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                      {index + 1}. {recommendation}
                    </Typography>
                  ))}
                </Paper>
              </Grid>
            </Grid>
          </Box>
        ) : (
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Complete Your Assessment
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Please complete all previous steps to see your results.
            </Typography>
          </Paper>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Leadership Assessment
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Stepper activeStep={activeStep} sx={{ mb: 4 }} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {renderStepContent(activeStep)}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
          variant="outlined"
        >
          Back
        </Button>
        <Box>
          {activeStep === 3 ? (
            <Button
              variant="contained"
              onClick={handleSubmitAssessment}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <AssessmentIcon />}
            >
              {loading ? 'Analyzing...' : 'Submit Assessment'}
            </Button>
          ) : activeStep === 4 ? (
            <Button
              variant="contained"
              onClick={() => navigate('/dashboard')}
              startIcon={<TrendingUp />}
            >
              View Dashboard
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={handleNext}
              endIcon={<ArrowForward />}
            >
              Next
            </Button>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default LeadershipAssessment;
