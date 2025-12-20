# 🚀 Deploying to Streamlit Cloud

This guide will walk you through deploying your Activity Data Dashboard to Streamlit Cloud so anyone can access it online!

## Prerequisites

- A GitHub account
- Your code pushed to a GitHub repository
- A Streamlit Cloud account (free - sign up at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

1. **Ensure your code is on GitHub**
   ```bash
   git add .
   git commit -m "Add file upload feature"
   git push origin main
   ```

2. **Verify these files exist in your repo:**
   - `app.py` (main application file)
   - `requirements.txt` (Python dependencies)
   - `src/` folder with all your modules

## Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with your GitHub account**

3. **Click "New app"**

4. **Fill in the deployment form:**
   - **Repository**: Select `roast-my-activity-data` (or your repo name)
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom name (e.g., `roast-my-activity`)

5. **Click "Deploy!"**

The app will take 2-3 minutes to deploy. Streamlit Cloud will automatically:
- Install all dependencies from `requirements.txt`
- Start your app
- Give you a public URL like `https://your-app-name.streamlit.app`

## Step 3: Share Your App

Once deployed, you can share the URL with anyone! They can:
- Upload their own Strava CSV files
- See their activity analytics without any setup
- No need to install Python or any dependencies

## Features Available After Deployment

✅ **CSV File Upload**: Users can upload their own Strava data
✅ **No Setup Required**: Everything runs in the cloud
✅ **Always Available**: App is live 24/7
✅ **Free Hosting**: Streamlit Community Cloud is free for public apps
✅ **Automatic Updates**: When you push to GitHub, the app auto-updates

## Configuration Options

### Environment Variables
If you need to add any secrets or environment variables:
1. Go to your app dashboard on Streamlit Cloud
2. Click "⚙️ Settings"
3. Go to "Secrets" section
4. Add your secrets in TOML format

### Resource Limits (Free Tier)
- 1 GB RAM
- 1 CPU core
- Sufficient for most use cases

### Private Apps
To make your app private (only accessible to you):
1. Go to app settings
2. Set "Sharing" to "Private"
3. Invite specific users if needed

## Troubleshooting

### App Won't Deploy
- Check that `requirements.txt` is complete
- Verify all imports in your code are available packages
- Check the deployment logs for specific errors

### App Crashes
- Check the logs in your Streamlit Cloud dashboard
- Verify your code works locally first
- Look for memory issues (reduce data size if needed)

### Slow Performance
- The default file is loaded from the repo
- Uploaded files are processed in memory (faster)
- Consider adding data size limits for large CSVs

## Next Steps

Want to enhance your deployed app?
- Add authentication for private data
- Connect to Strava API for live data
- Add more sports/activity types
- Create custom themes
- Add export functionality for reports

## Support

- 📚 [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- 💬 [Streamlit Community Forum](https://discuss.streamlit.io/)
- 🐛 Found a bug? Open an issue on GitHub

---

**Your app is now live! 🎉** Share it with friends and let them roast their activity data too!
