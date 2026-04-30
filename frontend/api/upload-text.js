// Vercel Serverless Function for Text Upload
export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get the backend URL from environment
    const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
    
    // Forward the request to the backend
    const response = await fetch(`${BACKEND_URL}/api/upload/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Vercel-Serverless-Function',
        'X-Forwarded-For': req.headers['x-forwarded-for'] || 'unknown',
        'X-Forwarded-Host': req.headers['x-forwarded-host'] || 'unknown',
      },
      body: JSON.stringify(req.body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Backend error:', errorText);
      return res.status(response.status).json({ 
        error: 'Backend request failed',
        details: errorText
      });
    }

    const data = await response.json();
    
    return res.status(200).json(data);
    
  } catch (error) {
    console.error('Function error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      message: error.message
    });
  }
}
