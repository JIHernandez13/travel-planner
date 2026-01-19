# GitHub Setup Instructions

This folder contains automated scripts to push your Travel Planner project to GitHub.

## Quick Start

### For Mac/Linux Users:

1. **Open Terminal** and navigate to the project folder:
   ```bash
   cd travel-planner
   ```

2. **Make the script executable:**
   ```bash
   chmod +x setup-github.sh
   ```

3. **Run the script:**
   ```bash
   ./setup-github.sh
   ```

### For Windows Users:

1. **Open Command Prompt** and navigate to the project folder:
   ```cmd
   cd travel-planner
   ```

2. **Run the script:**
   ```cmd
   setup-github.bat
   ```

## What the Script Does

1. ✅ Checks if Git is installed
2. ✅ Initializes Git repository
3. ✅ Creates/verifies .gitignore
4. ✅ Adds all project files
5. ✅ Creates initial commit
6. ⏸️  Pauses and asks you to create a GitHub repository
7. ✅ Adds your GitHub repository as remote
8. ✅ Pushes code to GitHub

## Before Running the Script

### First Time Git User?

If you haven't used Git before, set your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Need GitHub Authentication?

You'll need to authenticate with GitHub. Choose one option:

**Option 1: GitHub CLI (Recommended)**
```bash
# Install GitHub CLI: https://cli.github.com
gh auth login
```

**Option 2: Personal Access Token**
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic) with 'repo' scope
3. Use the token as your password when pushing

**Option 3: SSH Key**
1. Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
2. Use SSH URL format: `git@github.com:username/travel-planner.git`

## Step-by-Step Manual Process

If you prefer to do it manually:

### 1. Create Repository on GitHub
- Go to https://github.com/new
- Name: `travel-planner`
- Description: "Modern travel planning web app with FastAPI and React"
- **IMPORTANT**: Don't initialize with README, .gitignore, or license
- Click "Create repository"

### 2. Initialize Local Repository
```bash
cd travel-planner
git init
git add .
git commit -m "Initial commit: Travel planner foundation"
```

### 3. Connect to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/travel-planner.git
git branch -M main
git push -u origin main
```

## Troubleshooting

### "Permission denied"
- You need to authenticate (see authentication options above)
- Check if you have write access to the repository

### "Repository not found"
- Make sure you created the repository on GitHub first
- Verify the repository URL is correct
- Check you're logged into the right GitHub account

### "Failed to push"
- Make sure you created an empty repository (no README)
- Try pulling first: `git pull origin main --allow-unrelated-histories`
- Then push: `git push -u origin main`

### Script won't run (Mac/Linux)
- Make sure it's executable: `chmod +x setup-github.sh`
- Try running with bash: `bash setup-github.sh`

## After Successful Push

Once pushed, you'll see your project on GitHub! Next steps:

1. **Enable GitHub Pages** (optional) for hosting documentation
2. **Set up branch protection** for the main branch
3. **Add collaborators** if working with a team
4. **Create issues** for features from the roadmap
5. **Start development!**

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- GitHub CLI: https://cli.github.com

---

**Ready?** Just run the script and follow the prompts! 🚀
