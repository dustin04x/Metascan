# GitHub Pages Setup Instructions

## Fix the Permission Error

The workflow was failing because GitHub Pages deploy action needed proper permissions. This has been fixed.

## Manual Setup Required (One-time)

Follow these steps to enable GitHub Pages in your repository:

### Step 1: Go to Repository Settings
1. Open: https://github.com/dustin04x/Metascan
2. Click **Settings** (top navigation)
3. Scroll down to find **Pages** section

### Step 2: Enable GitHub Pages
1. Under "Source", select:
   - **Deploy from a branch**
2. Select:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
3. Click **Save**

### Step 3: Wait for Initial Deployment
- GitHub will run the workflow and create the `gh-pages` branch
- This may take 1-2 minutes
- Check the **Actions** tab to monitor progress

### Step 4: Access Your Deployed App
Once deployment completes, your app will be available at:
```
https://dustin04x.github.io/Metascan/
```

## What Changed in the Workflow

The updated `.github/workflows/deploy.yml` now:
- ✅ Includes proper permissions block
- ✅ Uses official GitHub Pages deployment action
- ✅ Configures environment for GitHub Pages
- ✅ Should deploy successfully without permission errors

## If You Still See Errors

1. **Check Actions Tab**
   - Go to: https://github.com/dustin04x/Metascan/actions
   - Click the latest workflow run
   - Check for error messages

2. **Verify Settings**
   - Settings → Pages
   - Make sure source is set to `gh-pages` branch
   - Folder should be `/ (root)`

3. **Check Branch Exists**
   - Go to Code tab
   - Switch to `gh-pages` branch
   - Should have frontend files

## Next Steps

1. Enable GitHub Pages following Step 1-3 above
2. Wait for the workflow to complete
3. Visit your GitHub Pages URL
4. Run backend locally to test the full app

---

**The workflow fix has been pushed to your repository!**
