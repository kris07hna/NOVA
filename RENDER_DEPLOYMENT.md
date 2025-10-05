# 🚀 Render Deployment Guide - NOVA AI Assistant

## Quick Deploy Steps

### 1. Sign Up / Login to Render
- Go to https://render.com/
- Sign in with GitHub (recommended)

### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `kris07hna/NOVA`
3. Click **"Connect"** next to your NOVA repo

### 3. Configure Service

**Basic Settings:**
- **Name**: `nova-ai-assistant` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `master`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```
  pip install --upgrade pip && pip install --prefer-binary -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

**Instance Type:**
- Select **"Free"** (or paid for better performance)

### 4. Add Environment Variables ⚠️ CRITICAL

Click **"Advanced"** → **"Add Environment Variable"** and add these:

```
ASSEMBLYAI_API_KEY=676b11eafeba4a5d8204b38fff08e05a
WOLFRAM_ALPHA_APP_ID=U7VEX3UA5V
GOOGLE_API_KEY=AIzaSyDjK5azqbokYVNDoD4d0gi2IsL-8f8SZTM
GOOGLE_SEARCH_ENGINE_ID=e02b81f92c7e64ca7
FLASK_ENV=production
SECRET_KEY=nova-secret-key-2024-render-deployment
PYTHON_VERSION=3.10.12
```

**Important:** Make sure each variable is entered exactly as shown above!

### 5. Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

### 6. Test Your Deployment

Once deployed, your app will be at: `https://nova-ai-assistant.onrender.com`

Test:
- ✅ Homepage loads
- ✅ Text input works
- ✅ Voice recording works (important: needs environment variables!)
- ✅ Math calculations work
- ✅ Search queries work

## 🔧 Troubleshooting

### Error: "Authentication error, API token missing/invalid"
**Problem:** ASSEMBLYAI_API_KEY not set in Render environment variables

**Solution:**
1. Go to your Render dashboard
2. Click on your service → **Environment** tab
3. Add/update: `ASSEMBLYAI_API_KEY=676b11eafeba4a5d8204b38fff08e05a`
4. Click **"Save Changes"** → Service will auto-redeploy

### Error: "Failed building wheel for blis"
**Solution:** Already fixed in `requirements.txt` with `blis==0.7.11`

### Service won't start / 502 Error
**Check:**
1. Build logs for errors
2. All environment variables are set correctly
3. No typos in variable names
4. Start command is `gunicorn app:app` (not `run.py`)

### Voice recording not working
**Check:**
1. Browser permissions (allow microphone)
2. HTTPS connection (Render provides this)
3. ASSEMBLYAI_API_KEY is set in environment

## 📊 Current Deployment Status

**Your deployed URL:** https://nova-1-78xi.onrender.com/

**Environment Variables Status:**
- ❓ ASSEMBLYAI_API_KEY - **NEEDS TO BE SET**
- ❓ WOLFRAM_ALPHA_APP_ID - Check if set
- ❓ GOOGLE_API_KEY - Check if set
- ❓ GOOGLE_SEARCH_ENGINE_ID - Check if set

## 🔐 Setting Environment Variables

### Method 1: Render Dashboard (Recommended)
1. Go to https://dashboard.render.com/
2. Click your service: **nova-1-78xi**
3. Go to **"Environment"** tab on the left
4. Click **"Add Environment Variable"**
5. Add each variable:
   - Key: `ASSEMBLYAI_API_KEY`
   - Value: `676b11eafeba4a5d8204b38fff08e05a`
6. Click **"Save Changes"**
7. Service will automatically redeploy

### Method 2: Via render.yaml (Already configured)
The `render.yaml` file is already set up, but you need to:
1. Go to Environment tab
2. Set values for variables marked as `sync: false`

## 📱 After Deployment

### Update Your Local Git
```bash
git add -A
git commit -m "Fix speech recognition and deployment configuration"
git push origin master
```

### Monitor Logs
1. Go to Render dashboard
2. Click your service
3. View **"Logs"** tab
4. Watch for errors in real-time

## 🎯 Quick Fix for Current Issue

**The speech recognition is failing because ASSEMBLYAI_API_KEY is not set on Render.**

**Fix NOW:**
1. Go to: https://dashboard.render.com/
2. Find your service: **nova-1-78xi** (or similar name)
3. Click on it
4. Go to **Environment** tab (left sidebar)
5. Add environment variable:
   - **Key:** `ASSEMBLYAI_API_KEY`
   - **Value:** `676b11eafeba4a5d8204b38fff08e05a`
6. Click **"Save Changes"**
7. Wait 2-3 minutes for auto-redeploy
8. Test voice recording again!

## ✅ Verification Checklist

After setting environment variables:
- [ ] Service redeployed successfully
- [ ] Homepage loads without errors
- [ ] Text chat works
- [ ] Voice button appears
- [ ] Voice recording works
- [ ] Transcription completes
- [ ] Math queries work
- [ ] Search queries work
- [ ] Self-thinking process displays

## 🆘 Need Help?

**Render Support:**
- Community: https://community.render.com/
- Docs: https://render.com/docs
- Status: https://status.render.com/

**Your Current Issue:**
The error `{"error": "Authentication error, API token missing/invalid"}` means the AssemblyAI API key is not reaching your deployed application. Follow the "Quick Fix" section above to resolve this immediately.

---

**Made with ❤️ for AdihaOne Interview**
