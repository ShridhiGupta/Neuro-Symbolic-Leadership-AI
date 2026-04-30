# 🚀 Vercel Deployment Guide

## **Option 1: Frontend Only (Recommended)**

### **Step 1: Prepare Frontend for Vercel**

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Import from GitHub: `ShridhiGupta/Neuro-Symbolic-Leadership-AI`
   - Select only the `frontend` directory
   - Framework Preset: `Create React App`

3. **Environment Variables**
   - Add: `REACT_APP_API_URL` = `https://your-backend-api.com`
   - (You'll get this from your backend deployment)

### **Step 2: Deploy Backend Separately**

#### **Backend Deployment Options:**

**A) Railway (Easiest)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway up
```

**B) Render**
- Go to [render.com](https://render.com)
- Connect GitHub repo
- Select `backend` folder
- Choose "Web Service"
- Set build command: `pip install -r requirements.txt && pip install -r requirements_minimal.txt`
- Set start command: `python main_simple.py`

**C) Heroku**
```bash
# Create Procfile
echo "web: python main_simple.py" > backend/Procfile

# Deploy
cd backend
heroku create your-app-name
git push heroku main
```

**D) PythonAnywhere (Free)**
- Go to [pythonanywhere.com](https://pythonanywhere.com)
- Create "Web App"
- Upload backend files
- Configure to run `python main_simple.py`

### **Step 3: Update Frontend API URL**

After deploying backend, update the API URL in Vercel:
1. Go to Vercel dashboard
2. Settings → Environment Variables
3. Update `REACT_APP_API_URL` to your backend URL

---

## **Option 2: Full-Stack on Vercel (Advanced)**

### **Using Vercel Serverless Functions**

You can deploy the backend as serverless functions:

1. **Create API Routes** in `frontend/api/`:
```javascript
// frontend/api/assessment.js
export default async function handler(req, res) {
  // Call your backend API
  const response = await fetch('https://your-backend-url.com/api/assessment/evaluate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req.body)
  });
  
  const data = await response.json();
  res.status(200).json(data);
}
```

2. **Update vercel.json**:
```json
{
  "version": 2,
  "functions": {
    "api/*.js": {
      "runtime": "nodejs18.x"
    }
  }
}
```

---

## **🔧 Configuration Files Created**

### **Frontend vercel.json**
- ✅ Static build configuration
- ✅ SPA routing
- ✅ Environment variables

### **Deployment Checklist**

**Before deploying:**
- [ ] Test frontend locally: `npm start`
- [ ] Test backend locally: `python main_simple.py`
- [ ] Update API endpoints if needed
- [ ] Add environment variables

**After deploying:**
- [ ] Test frontend on Vercel URL
- [ ] Test API connectivity
- [ ] Verify all features work

---

## **🌐 Free Hosting Options**

### **Frontend (Vercel)**
- ✅ Free tier available
- ✅ Custom domain
- ✅ HTTPS
- ✅ Automatic deployments

### **Backend (Free Options)**
- ✅ Railway (Free tier)
- ✅ Render (Free tier)
- ✅ PythonAnywhere (Free)
- ✅ Heroku (Free tier)

---

## **📱 What Works After Deployment**

### **✅ Working Features:**
- Dashboard with charts
- Leadership assessment
- Cultural comparison
- Trait development
- File upload (text)
- All UI components

### **⚠️ Limitations:**
- File upload (PDF/DOCX) - needs proper file handling
- Real-time features - need WebSocket setup
- Database persistence - needs cloud database

---

## **🎯 Quick Start**

1. **Deploy Frontend to Vercel** (5 minutes)
2. **Deploy Backend to Railway** (5 minutes)
3. **Update API URL** (2 minutes)
4. **Test Full Application** (5 minutes)

**Total time: ~17 minutes**

---

## **🔗 Links**

- **Vercel**: https://vercel.com
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **PythonAnywhere**: https://pythonanywhere.com

---

**🎉 Your Neuro-Symbolic Leadership AI can be live on Vercel in under 20 minutes!**
