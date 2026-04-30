import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Button,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Psychology,
  TrendingUp,
  Assessment,
  Compare,
  Timeline,
  Star,
  Upload,
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
  LineChart,
  Line,
} from 'recharts';

import api from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recentAssessments, setRecentAssessments] = useState([]);
  const [overallStats, setOverallStats] = useState({
    totalAssessments: 0,
    averageScore: 0,
    topTrait: '',
    improvementAreas: [],
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      // In a real app, this would fetch from the API
      // For now, using mock data
      const mockData = {
        recentAssessments: [
          {
            id: 1,
            date: '2024-01-15',
            culture: 'US',
            overallScore: 78,
            traits: [
              { name: 'confidence', score: 85 },
              { name: 'collaboration', score: 72 },
              { name: 'decision_making', score: 80 },
              { name: 'communication', score: 75 },
              { name: 'empathy', score: 68 },
              { name: 'innovation', score: 82 },
              { name: 'resilience', score: 76 },
              { name: 'strategic_thinking', score: 71 },
            ],
          },
          {
            id: 2,
            date: '2024-01-10',
            culture: 'Japan',
            overallScore: 72,
            traits: [
              { name: 'confidence', score: 65 },
              { name: 'collaboration', score: 88 },
              { name: 'decision_making', score: 70 },
              { name: 'communication', score: 68 },
              { name: 'empathy', score: 85 },
              { name: 'innovation', score: 60 },
              { name: 'resilience', score: 74 },
              { name: 'strategic_thinking', score: 66 },
            ],
          },
        ],
        overallStats: {
          totalAssessments: 12,
          averageScore: 75.3,
          topTrait: 'collaboration',
          improvementAreas: ['empathy', 'strategic_thinking'],
        },
      };

      setRecentAssessments(mockData.recentAssessments);
      setOverallStats(mockData.overallStats);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRadarData = (assessment) => {
    return assessment.traits.map(trait => ({
      trait: trait.name.replace('_', ' ').toUpperCase(),
      score: trait.score,
      fullMark: 100,
    }));
  };

  const getTraitComparisonData = () => {
    if (recentAssessments.length < 2) return [];
    
    const latest = recentAssessments[0];
    const previous = recentAssessments[1];
    
    return latest.traits.map(trait => {
      const previousTrait = previous.traits.find(t => t.name === trait.name);
      return {
        trait: trait.name.replace('_', ' ').toUpperCase(),
        current: trait.score,
        previous: previousTrait ? previousTrait.score : 0,
      };
    });
  };

  const getProgressData = () => {
    return [
      { month: 'Sep', score: 68 },
      { month: 'Oct', score: 71 },
      { month: 'Nov', score: 74 },
      { month: 'Dec', score: 76 },
      { month: 'Jan', score: 78 },
    ];
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={loadDashboardData}>
          Retry
        </Button>
      </Box>
    );
  }

  const latestAssessment = recentAssessments[0];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Leadership Assessment Dashboard
      </Typography>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Assessment sx={{ mr: 1, color: 'white' }} />
                <Typography variant="h6">{overallStats.totalAssessments}</Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Total Assessments
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUp sx={{ mr: 1, color: 'white' }} />
                <Typography variant="h6">{overallStats.averageScore.toFixed(1)}</Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Average Score
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Star sx={{ mr: 1, color: 'white' }} />
                <Typography variant="h6">{overallStats.topTrait}</Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Top Trait
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Psychology sx={{ mr: 1, color: 'white' }} />
                <Typography variant="h6">{overallStats.improvementAreas.length}</Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Areas to Improve
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Latest Assessment Overview */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Latest Assessment Overview
            </Typography>
            {latestAssessment && (
              <Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Culture: {latestAssessment.culture} | Date: {latestAssessment.date}
                  </Typography>
                  <Typography variant="h5" color="primary" sx={{ mt: 1 }}>
                    Overall Score: {latestAssessment.overallScore}/100
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={latestAssessment.overallScore}
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </Box>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={getRadarData(latestAssessment)}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="trait" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    <Radar
                      name="Score"
                      dataKey="score"
                      stroke="#6366f1"
                      fill="#818cf8"
                      fillOpacity={0.6}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Trait Comparison */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Trait Comparison (Current vs Previous)
            </Typography>
            {getTraitComparisonData().length > 0 && (
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={getTraitComparisonData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="trait" angle={-45} textAnchor="end" height={80} />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="current" fill="#6366f1" name="Current" />
                  <Bar dataKey="previous" fill="#ec4899" name="Previous" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Progress Over Time */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Progress Over Time
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={getProgressData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#10b981"
                  strokeWidth={3}
                  dot={{ fill: '#10b981', r: 6 }}
                  name="Overall Score"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                startIcon={<Assessment />}
                onClick={() => navigate('/assessment')}
                fullWidth
              >
                New Assessment
              </Button>
              <Button
                variant="outlined"
                startIcon={<Upload />}
                onClick={() => navigate('/upload')}
                fullWidth
              >
                Upload Resume
              </Button>
              <Button
                variant="outlined"
                startIcon={<Compare />}
                onClick={() => navigate('/cultural-comparison')}
                fullWidth
              >
                Cultural Comparison
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Improvement Areas */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Focus Areas
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {overallStats.improvementAreas.map((area, index) => (
                <Chip
                  key={index}
                  label={area.replace('_', ' ').toUpperCase()}
                  sx={{ 
                    background: 'linear-gradient(45deg, #f59e0b 30%, #d97706 90%)',
                    color: 'white',
                    fontWeight: 'bold',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #d97706 30%, #92400e 90%)',
                    }
                  }}
                  clickable
                  onClick={() => navigate('/trait-development')}
                />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
