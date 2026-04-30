import React, { useState, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  CloudUpload,
  Description,
  Delete,
  CheckCircle,
  Error,
  FileUpload,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';

import api from '../services/api';

const Upload = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [extractedText, setExtractedText] = useState('');
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      handleFileUpload(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleFileUpload = async (file) => {
    try {
      setUploading(true);
      setError(null);
      setSuccess(null);
      setUploadProgress(0);

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);

      // Call the backend API (simplified version)
      const response = await api.post('/api/upload/resume');
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      setExtractedText(response.data.extracted_text);
      setSuccess('File uploaded and text extracted successfully!');
      setUploadedFiles([...uploadedFiles, response.data]);
      setUploadProgress(0);
    } catch (err) {
      setError(err.response?.data?.detail || 'File upload failed');
      setUploadProgress(0);
    } finally {
      setUploading(false);
    }
  };

  const handleTextUpload = async () => {
    if (!extractedText.trim()) {
      setError('Please enter some text to upload');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      setSuccess(null);

      const response = await api.post('/api/upload/text', {
        text: extractedText,
        filename: 'direct_text_input',
        user_id: 'current_user',
      });

      setSuccess('Text uploaded successfully!');
      setUploadedFiles([...uploadedFiles, response.data]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Text upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleProceedToAssessment = () => {
    // Store the extracted text in localStorage for the assessment page
    if (extractedText) {
      localStorage.setItem('resumeText', extractedText);
      navigate('/assessment');
    }
  };

  const handleDeleteFile = (index) => {
    const newFiles = uploadedFiles.filter((_, i) => i !== index);
    setUploadedFiles(newFiles);
  };

  const getFileIcon = (filename) => {
    if (filename.endsWith('.pdf')) return <Description color="error" />;
    if (filename.endsWith('.txt')) return <Description color="primary" />;
    if (filename.endsWith('.docx')) return <Description color="success" />;
    return <Description />;
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Upload Resume
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* File Upload Area */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload Resume File
            </Typography>
            
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed',
                borderColor: isDragActive ? 'primary.main' : 'grey.300',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? 'action.hover' : 'transparent',
                transition: 'all 0.2s ease',
                '&:hover': {
                  backgroundColor: 'action.hover',
                  borderColor: 'primary.main',
                },
              }}
            >
              <input {...getInputProps()} />
              <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                {isDragActive ? 'Drop your file here' : 'Drag & drop your resume'}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                or click to browse
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Supported formats: PDF, TXT, DOCX (Max 10MB)
              </Typography>
            </Box>

            {uploading && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" gutterBottom>
                  Uploading... {uploadProgress}%
                </Typography>
                <LinearProgress variant="determinate" value={uploadProgress} />
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Text Input Area */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Or Paste Resume Text
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={12}
              label="Resume Text"
              value={extractedText}
              onChange={(e) => setExtractedText(e.target.value)}
              placeholder="Paste your resume text here..."
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              onClick={handleTextUpload}
              disabled={uploading || !extractedText.trim()}
              startIcon={uploading ? <CircularProgress size={20} /> : <FileUpload />}
            >
              {uploading ? 'Processing...' : 'Upload Text'}
            </Button>
          </Paper>
        </Grid>

        {/* Extracted Text Preview */}
        {extractedText && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Extracted Text Preview
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={`${extractedText.length} characters`}
                  color="primary"
                  variant="outlined"
                  size="small"
                />
                <Chip
                  label={`${extractedText.split(' ').length} words`}
                  color="secondary"
                  variant="outlined"
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Box>
              <TextField
                fullWidth
                multiline
                rows={6}
                value={extractedText}
                onChange={(e) => setExtractedText(e.target.value)}
                variant="outlined"
                sx={{ mb: 2 }}
              />
              <Button
                variant="contained"
                onClick={handleProceedToAssessment}
                startIcon={<CheckCircle />}
                size="large"
              >
                Proceed to Assessment
              </Button>
            </Paper>
          </Grid>
        )}

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Uploaded Files
              </Typography>
              <List>
                {uploadedFiles.map((file, index) => (
                  <ListItem key={index} divider>
                    <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                      {getFileIcon(file.filename)}
                    </Box>
                    <ListItemText
                      primary={file.filename}
                      secondary={`${file.file_size} bytes | ${file.text_length} characters`}
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => handleDeleteFile(index)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        )}

        {/* Instructions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              How to Upload Your Resume
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      1. Choose Method
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Either drag & drop a file or paste your resume text directly.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      2. Upload & Extract
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Our system will automatically extract text from your file.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      3. Review & Proceed
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Review the extracted text and proceed to assessment.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Upload;
