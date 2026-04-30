# 🚀 Deploy Neuro-Symbolic Leadership AI as Monorepo on Vercel

## **📋 Overview**

This guide shows how to deploy the full-stack Neuro-Symbolic Leadership AI application as a single monorepo on Vercel, with both React frontend and Python backend.

## **🏗️ Architecture**

```
Project Structure:
├── api/                    # Vercel Python functions
│   ├── index.py           # Main API entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   ├── build/            # Build output
│   └── package.json
├── backend/               # Backend source code
│   ├── app/
│   ├── services/
│   └── main_simple.py   # Backend application
└── vercel.json           # Vercel configuration
```

## **🛠️ Prerequisites**

1. **Vercel Account** - Create at [vercel.com](https://vercel.com)
2. **GitHub Repository** - Your project must be on GitHub
3. **Node.js 18+** - For frontend build
4. **Python 3.9+** - For backend

## **📦 Step 1: Prepare Repository**

### **A. Structure Your Repository**
```
neuro-symbolic-leadership-ai/
├── api/
├── frontend/
├── backend/
├── vercel.json
└── README.md
```

### **B. Update Files**
1. ✅ `vercel.json` - Already created
2. ✅ `api/index.py` - Already created
3. ✅ `api/requirements.txt` - Already created
4. ✅ `frontend/` - Already exists

## **📦 Step 2: Deploy to Vercel**

### **A. Import Project**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import from GitHub
4. Select: `ShridhiGupta/Neuro-Symbolic-Leadership-AI`
5. Framework: **Other**
6. Root Directory: Keep default

### **B. Configure Build**
Vercel will automatically detect your `vercel.json` configuration.

### **C. Add Environment Variables**
In Vercel Dashboard → Settings → Environment Variables:
```
PYTHON_VERSION=3.9
NODE_VERSION=18
```

### **D. Deploy**
Click "Deploy" and wait for the build to complete.

## **🔧 How It Works**

### **Frontend Deployment**
- React app builds to `frontend/build/`
- Served as static files
- SPA routing handled by `vercel.json`

### **Backend Deployment**
- Python functions in `api/` directory
- FastAPI application served as serverless functions
- API routes proxied through `routes` configuration

### **API Communication**
- Frontend calls: `/api/assessment/evaluate`
- Vercel routes to: `/api/index.py`
- Python function forwards to backend logic

## **🎯 Features Available**

### **✅ Working Features**
- ✅ Dashboard with charts
- ✅ Leadership assessment
- ✅ Cultural comparison
- ✅ Trait development
- ✅ Text upload functionality
- ✅ All UI components
- ✅ API endpoints

### **⚠️ Limitations**
- File upload (PDF/DOCX) - Requires file storage service
- Real-time features - Requires WebSocket setup
- Database persistence - Requires cloud database
- Large file processing - Lambda size limits

## **🔄 Testing After Deployment**

### **1. Frontend**
Visit your Vercel URL and test:
- Dashboard loads correctly
- Navigation works
- Charts display properly

### **2. Backend API**
Test these endpoints:
```bash
# Health check
curl https://your-app.vercel.app/health

# Assessment API
curl -X POST https://your-app.vercel.app/api/assessment/evaluate \
  -H "Content-Type: application/json" \
  -d '{
      "culture": "US",
      "resume_text": "I am a confident leader...",
      "responses": ["I lead teams effectively..."]
    }'
```

### **3. Full Integration**
- Complete an assessment
- Test cultural comparison
- Verify trait development

## **🌐 Free Tier Limitations**

### **Vercel Free Tier**
- **Functions**: 100k invocations/month
- **Bandwidth**: 100GB/month
- **Build Time**: 60s per build
- **Execution Time**: 10s per function

### **Recommendations**
- Optimize function execution time
- Use caching for repeated requests
- Monitor usage to stay within limits

## **🚀 Production Considerations**

### **Database**
- Use Vercel Postgres or external database
- Add connection pooling
- Implement proper migrations

### **File Storage**
- Use Vercel Blob Storage
- AWS S3 (recommended)
- Cloudinary

### **Scaling**
- Consider upgrading to Pro plan for higher limits
- Use edge functions for better performance
- Implement proper caching strategies

## **🔧 Troubleshooting**

### **Common Issues**

**Build Fails**
- Check `vercel.json` syntax
- Verify Python version compatibility
- Ensure all dependencies are in `api/requirements.txt`

**Function Errors**
- Check Vercel logs
- Verify API structure
- Test locally first

**CORS Issues**
- Headers are configured in `vercel.json`
- Check route configuration
- Verify frontend API calls

**Deployment Fails**
- Check Vercel logs
- Verify repository structure
- Ensure all files are committed

## **📱 Monitoring**

### **Vercel Analytics**
- Function execution logs
- Performance metrics
- Error tracking

### **Custom Monitoring**
- Add logging to Python functions
- Implement health checks
- Set up alerts

---

## **🎉 Quick Start**

1. **Push changes to GitHub**
2. **Deploy to Vercel** (5-10 minutes)
3. **Test functionality** (5 minutes)
4. **Share your app!** 🚀

---

**🎉 Your Neuro-Symbolic Leadership AI is now ready for Vercel deployment as a monorepo!**

The application will run entirely on Vercel's infrastructure with both frontend and backend components working together seamlessly.
