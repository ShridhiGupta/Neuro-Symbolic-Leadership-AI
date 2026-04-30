import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  TrendingUp,
  School,
  Timeline,
  CheckCircle,
} from '@mui/icons-material';

const TraitDevelopment = () => {
  const [selectedTrait, setSelectedTrait] = useState('confidence');
  const [currentScore, setCurrentScore] = useState(70);

  const traits = [
    { name: 'confidence', score: 75, description: 'Self-assurance and decisiveness' },
    { name: 'collaboration', score: 82, description: 'Teamwork and cooperation' },
    { name: 'decision_making', score: 78, description: 'Strategic choices and judgment' },
    { name: 'communication', score: 71, description: 'Clear and effective communication' },
    { name: 'empathy', score: 68, description: 'Understanding and relating to others' },
    { name: 'innovation', score: 85, description: 'Creativity and new ideas' },
    { name: 'resilience', score: 73, description: 'Adaptability and recovery' },
    { name: 'strategic_thinking', score: 77, description: 'Long-term planning and vision' },
  ];

  const developmentPlan = {
    immediate_actions: [
      `Practice ${selectedTrait.replace('_', ' ')} in daily situations`,
      `Seek feedback on ${selectedTrait.replace('_', ' ')} skills`,
      `Study examples of strong ${selectedTrait.replace('_', ' ')} in leaders`
    ],
    next_steps: [
      'Take on leadership challenges that require this trait',
      'Mentor others in developing this skill',
      'Read books and take courses on this topic'
    ],
    resources: [
      'Leadership development courses',
      'Executive coaching programs',
      'Industry workshops and seminars'
    ],
    success_metrics: [
      `Increase ${selectedTrait} score by 10 points`,
      `Receive positive feedback on ${selectedTrait}`,
      `Successfully apply ${selectedTrait} in real situations`
    ]
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Leadership Trait Development
      </Typography>

      <Grid container spacing={3}>
        {/* Trait Selection */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Select Trait to Develop
            </Typography>
            {traits.map((trait) => (
              <Card
                key={trait.name}
                sx={{ mb: 2, cursor: 'pointer', border: selectedTrait === trait.name ? 2 : 0, borderColor: 'primary.main' }}
                onClick={() => setSelectedTrait(trait.name)}
              >
                <CardContent>
                  <Typography variant="h6">
                    {trait.name.replace('_', ' ').toUpperCase()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {trait.description}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="body2" sx={{ mr: 1 }}>
                      Current Score:
                    </Typography>
                    <Typography variant="h6" color="primary">
                      {trait.score}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={trait.score}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            ))}
          </Paper>
        </Grid>

        {/* Development Plan */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Development Plan: {selectedTrait.replace('_', ' ').toUpperCase()}
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <Timeline sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Immediate Actions
                    </Typography>
                    <List dense>
                      {developmentPlan.immediate_actions.map((action, index) => (
                        <ListItem key={index}>
                          <ListItemText primary={action} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Next Steps
                    </Typography>
                    <List dense>
                      {developmentPlan.next_steps.map((step, index) => (
                        <ListItem key={index}>
                          <ListItemText primary={step} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <School sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Learning Resources
                    </Typography>
                    <List dense>
                      {developmentPlan.resources.map((resource, index) => (
                        <ListItem key={index}>
                          <ListItemText primary={resource} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <CheckCircle sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Success Metrics
                    </Typography>
                    <List dense>
                      {developmentPlan.success_metrics.map((metric, index) => (
                        <ListItem key={index}>
                          <ListItemText primary={metric} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                <strong>Current Level:</strong> {currentScore >= 80 ? 'Advanced' : currentScore >= 60 ? 'Intermediate' : 'Developing'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Target Level:</strong> Expert
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Estimated Timeline:</strong> 3-6 months with consistent practice
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TraitDevelopment;
