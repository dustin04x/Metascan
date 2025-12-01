# GitHub Pages Setup Instructions

## How It Works

Your MetaScan frontend will be automatically deployed to GitHub Pages. The workflow will:
1. Trigger on every push to the `main` branch
2. Create a `gh-pages` branch automatically
3. Deploy your frontend to that branch
4. Make it live at: `https://dustin04x.github.io/Metascan/`

## Setup Steps (One-time)

### Step 1: Go to Repository Settings
1. Open: https://github.com/dustin04x/Metascan
2. Click **Settings** (top navigation)
3. Scroll down to find **Pages** section

### Step 2: Configure GitHub Pages
1. Under "Source", select:
   - **Deploy from a branch**
2. Select:
   - **Branch:** `gh-pages` (will be created automatically)
   - **Folder:** `/ (root)`
3. Click **Save**

**Note:** The `gh-pages` branch doesn't exist yet - it will be created automatically by the GitHub Actions workflow on first deployment.

### Step 3: Trigger the Workflow
The workflow has already been set up. It will:
- Run automatically when you push to `main`
- Create the `gh-pages` branch
- Deploy the frontend

### Step 4: Monitor Deployment
1. Go to your repository
2. Click **Actions** tab
3. Look for "Deploy to GitHub Pages" workflow
4. Wait for it to complete (green checkmark)

### Step 5: Access Your App
Once deployment completes, visit:
```
https://dustin04x.github.io/Metascan/
```

## Automatic Workflow

After the initial setup, every push to `main` will:
- ✅ Automatically trigger the workflow
- ✅ Build the frontend
- ✅ Deploy to GitHub Pages
- ✅ Update your live site

## Troubleshooting

### No `gh-pages` branch showing
- This is normal! The workflow creates it on first run
- After the workflow completes, the branch will appear
- You can see it in the branches dropdown

### Workflow still failing
1. Check **Actions** tab for error details
2. Verify GitHub Pages settings (Source: `gh-pages` / Root)
3. Make sure you saved the Pages settings

### Site not updating
- Wait 1-2 minutes for workflow to complete
- Refresh browser (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
- Check browser cache if still seeing old version

## Backend Setup

To use the full MetaScan app, you also need to run the backend:

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then visit your GitHub Pages URL and start uploading images to analyze!

---

**All set! The workflow is ready to deploy your app to GitHub Pages.**
