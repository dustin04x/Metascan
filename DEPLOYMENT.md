# MetaScan - GitHub Pages Deployment Guide

## Overview

MetaScan is deployed to GitHub Pages for easy access to the web interface. The **frontend** is hosted on GitHub Pages, while the **backend** needs to be run locally or on your own server.

---

## ✅ Automatic Deployment (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically deploys the frontend whenever you push to the `main` branch.

**Status:** ✅ Configured and ready

The workflow file is located at `.github/workflows/deploy.yml` and will:
1. Install dependencies
2. Run any build scripts
3. Deploy to GitHub Pages automatically

---

## 🚀 Manual GitHub Pages Setup (One-time)

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/dustin04x/Metascan`
2. Click **Settings**
3. Scroll down to **Pages** section
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**

### Step 2: Wait for Deployment

- GitHub will build and deploy automatically
- Check the **Actions** tab to monitor the build
- Your site will be available at: `https://dustin04x.github.io/Metascan/`

### Step 3: Access Your Deployed App

Open your browser and navigate to:
```
https://dustin04x.github.io/Metascan/
```

---

## 🔌 Connecting Frontend to Backend

Since the backend isn't hosted on GitHub Pages, you need to connect the frontend to a backend instance.

### Option 1: Local Backend (Recommended for Testing)

**Best for:** Development, testing, personal use

**Steps:**
1. Clone the repository locally:
   ```bash
   git clone https://github.com/dustin04x/Metascan.git
   cd Metascan
   ```

2. Start the backend locally:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   python -m uvicorn app:app --host 127.0.0.1 --port 8000
   ```

3. Open the frontend in your browser:
   - If running locally: `http://localhost:5173`
   - If using GitHub Pages: `https://dustin04x.github.io/Metascan/`
   
   Note: The local frontend in the repo will automatically connect to `http://localhost:8000` (the default backend URL).
   The GitHub Pages version will also try to connect to `localhost:8000`, so run your backend on the same machine.

### Option 2: Deploy Backend to Server (Advanced)

**Best for:** Production, sharing with others

**Services:** Heroku, AWS, DigitalOcean, PythonAnywhere, etc.

**Steps:**

1. **Deploy Backend to a Service**
   - Choose a service that supports FastAPI (most do)
   - Deploy the `backend/` folder
   - Note the deployed URL (e.g., `https://metascan-api.herokuapp.com`)

2. **Update Frontend API Endpoint**
   - Edit `frontend/app.js`
   - Find the line with `http://localhost:8000/api/inspect`
   - Replace with your deployed backend URL
   - Commit and push changes

3. **Frontend Auto-Deploys**
   - GitHub Actions will detect your push
   - Frontend will be rebuilt with the new API endpoint
   - Your app is now live!

**Important:** Make sure to enable CORS on your backend for the GitHub Pages domain:
```python
# In backend/app.py, modify the CORS origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dustin04x.github.io"],  # Add GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📱 Using the Deployed Frontend

Once you have the frontend deployed and backend running, you can:

1. **Upload Images**
   - Drag and drop images into the upload area
   - Or click to select files from your computer

2. **View Analysis**
   - See basic file information (name, size, format, dimensions)
   - View EXIF data (camera make, model, ISO, etc.)
   - Check file hashes (MD5, SHA1, SHA256)
   - Review entropy and steganography detection

3. **Export Results**
   - Export metadata as JSON
   - Download embedded thumbnails
   - Copy results to clipboard

4. **Check Anomalies**
   - Review forensic findings (GPS, editing, high entropy, etc.)
   - Understand security implications

---

## 🔄 Updating Deployed App

### To Update the Frontend

1. Make changes to files in `frontend/` directory
2. Commit and push to `main` branch
3. GitHub Actions automatically builds and deploys
4. Changes live within ~1 minute

### To Update the Backend

1. Modify `backend/app.py` or other backend files
2. Test locally: `python -m uvicorn app:app --reload`
3. If using Option 2 deployment, redeploy to your service
4. Users running local backend can pull latest and restart

---

## 🛠️ Troubleshooting

### "Failed to fetch" error in browser

**Problem:** Frontend can't reach the backend

**Solutions:**
1. Make sure backend is running on `http://localhost:8000`
2. Check browser console (F12) for CORS errors
3. If using remote backend, verify CORS is configured
4. Check that backend URL in `app.js` is correct

### GitHub Pages shows 404

**Problem:** Frontend not deploying correctly

**Solutions:**
1. Check the **Actions** tab for build errors
2. Verify `.github/workflows/deploy.yml` exists
3. Make sure `main` branch is up to date
4. Try re-running the action manually

### Backend deployment issues

**If using Heroku:**
```bash
# Install Heroku CLI and deploy
heroku login
heroku create metascan-api
git push heroku main
```

**If using other services, follow their documentation**

---

## 📊 Architecture

```
GitHub Pages (Frontend)
     ↓
   CORS
     ↓
Your Backend Server
     ↓
Image Analysis (EXIF, GPS, Hashes, etc.)
```

---

## ✅ Checklist for Full Deployment

- [ ] GitHub Pages enabled in repository settings
- [ ] `.github/workflows/deploy.yml` exists
- [ ] Frontend deployed to `https://dustin04x.github.io/Metascan/`
- [ ] Backend running (local or remote)
- [ ] CORS configured if using remote backend
- [ ] API endpoint URL correct in `frontend/app.js`
- [ ] Can upload images and see analysis results

---

## 🎯 Next Steps

1. **Test Locally First**
   - Run both backend and frontend locally
   - Verify everything works
   - Check console for errors

2. **Deploy Frontend to GitHub Pages**
   - Push to main branch
   - Watch for automatic deployment
   - Verify at your GitHub Pages URL

3. **Deploy Backend (Choose Option)**
   - Option 1: Keep running locally for personal use
   - Option 2: Deploy to production service for sharing

4. **Share Your App**
   - Share GitHub Pages URL with others
   - They can use the frontend
   - They need to run their own backend or use yours

---

## 📞 Support

For issues:
1. Check browser console (F12) for error messages
2. Check terminal where backend is running for server errors
3. Review GitHub Actions logs for deployment errors
4. Check the main README.md for troubleshooting

---

**Version:** 0.1.0  
**Last Updated:** November 28, 2025  
**Status:** ✅ Ready for deployment
