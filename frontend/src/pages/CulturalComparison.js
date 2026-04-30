import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Compare,
  Psychology,
  TrendingUp,
  Language,
  Assessment,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
} from 'recharts';

import api from '../services/api';

const CulturalComparison = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  const [inputText, setInputText] = useState('');
  const [selectedCulture, setSelectedCulture] = useState('US');
  const [tabValue, setTabValue] = useState(0);

  const cultures = ['US', 'Japan', 'India', 'Germany', 'Brazil', 'China', 'UK', 'France', 'Canada', 'Australia'];

  const handleComparison = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await api.get(`/api/assessment/cultural-comparison/current_user`, {
        params: { text: inputText }
      });

      setComparisonData(response.data);
      setTabValue(0);
    } catch (err) {
      setError('Cultural comparison failed. Please try again.');
      console.error('Comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getBarChartData = () => {
    if (!comparisonData) return [];

    return Object.entries(comparisonData.cultural_comparison).map(([culture, data]) => ({
      culture,
      score: data.overall_score,
    }));
  };

  const getRadarChartData = (culture) => {
    if (!comparisonData || !comparisonData.cultural_comparison[culture]) return [];

    const traits = comparisonData.cultural_comparison[culture].traits;
    return Object.entries(traits).map(([trait, score]) => ({
      trait: trait.replace('_', ' ').toUpperCase(),
      score,
      fullMark: 100,
    }));
  };

  const getTraitComparisonData = () => {
    if (!comparisonData) return [];

    const cultures = Object.keys(comparisonData.cultural_comparison);
    const traits = Object.keys(comparisonData.cultural_comparison[cultures[0]].traits);

    return traits.map(trait => {
      const data = { trait: trait.replace('_', ' ').toUpperCase() };
      cultures.forEach(culture => {
        data[culture] = comparisonData.cultural_comparison[culture].traits[trait];
      });
      return data;
    });
  };

  const getTopCultures = () => {
    if (!comparisonData) return [];

    return Object.entries(comparisonData.cultural_comparison)
      .sort(([,a], [,b]) => b.overall_score - a.overall_score)
      .slice(0, 5);
  };

  const renderTabContent = () => {
    if (!comparisonData) return null;

    switch (tabValue) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Overall Scores by Culture
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={getBarChartData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="culture" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="score" fill="#1976d2" />
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Top 5 Cultures for Your Leadership Style
                </Typography>
                {getTopCultures().map(([culture, data], index) => (
                  <Card key={culture} variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="h6">
                          {index + 1}. {culture}
                        </Typography>
                        <Typography variant="h5" color="primary">
                          {data.overall_score.toFixed(1)}
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={data.overall_score}
                        sx={{ mt: 1, height: 8, borderRadius: 4 }}
                      />
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Cultural variance: {comparisonData.insights.cultural_variance.toFixed(1)} points
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Paper>
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Trait Comparison Across Cultures
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={getTraitComparisonData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="trait" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    {cultures.slice(0, 5).map((culture, index) => (
                      <Bar
                        key={culture}
                        dataKey={culture}
                        fill={['#1976d2', '#dc004e', '#ffa726', '#66bb6a', '#ab47bc'][index]}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
          </Grid>
        );

      case 2:
        return (
          <Grid container spacing={3}>
            {cultures.slice(0, 6).map((culture) => (
              <Grid item xs={12} md={6} key={culture}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    {culture} Leadership Profile
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Overall Score: {comparisonData.cultural_comparison[culture].overall_score.toFixed(1)}/100
                  </Typography>
                  <ResponsiveContainer width="100%" height={250}>
                    <RadarChart data={getRadarChartData(culture)}>
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
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Key Insights:
                    </Typography>
                    {comparisonData.cultural_comparison[culture].cultural_insights.slice(0, 2).map((insight, index) => (
                      <Typography key={index} variant="caption" display="block">
                        • {insight}
                      </Typography>
                    ))}
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Cultural Comparison Analysis
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analyze Your Leadership Style Across Cultures
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Enter your leadership experience text to see how it would be evaluated across different cultural contexts.
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={6}
              label="Leadership Experience Text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Describe your leadership experience, challenges, and achievements..."
              sx={{ mb: 2 }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handleComparison}
              disabled={loading || !inputText.trim()}
              startIcon={loading ? <CircularProgress size={20} /> : <Compare />}
              size="large"
            >
              {loading ? 'Analyzing...' : 'Compare Across Cultures'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {comparisonData && (
        <Box>
          <Paper sx={{ mb: 3 }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              sx={{ borderBottom: 1, borderColor: 'divider' }}
            >
              <Tab label="Overall Comparison" />
              <Tab label="Trait Analysis" />
              <Tab label="Cultural Profiles" />
            </Tabs>
          </Paper>

          {renderTabContent()}

          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Key Insights
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" color="primary">
                      Best Match
                    </Typography>
                    <Typography variant="h5">
                      {comparisonData.insights.highest_scoring_culture}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Your leadership style aligns best with this culture
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" color="warning.main">
                      Cultural Adaptation Needed
                    </Typography>
                    <Typography variant="h5">
                      {comparisonData.insights.lowest_scoring_culture}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Requires most adaptation for this culture
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" color="info.main">
                      Cultural Variance
                    </Typography>
                    <Typography variant="h5">
                      {comparisonData.insights.cultural_variance.toFixed(1)} points
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Score range across all cultures
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Box>
      )}
    </Box>
  );
};

export default CulturalComparison;
