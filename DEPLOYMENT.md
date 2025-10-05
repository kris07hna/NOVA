# PythonAnywhere Deployment Guide

## Step-by-Step Instructions

### 1. Sign Up
- Go to https://www.pythonanywhere.com/
- Create a free account (or paid for better resources)

### 2. Upload Your Code

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/yourusername/NOVA.git
cd NOVA
```

**Option B: Manual Upload**
- Use "Files" tab to create `/home/yourusername/NOVA` folder
- Upload all files except `venv/` and `__pycache__/`

### 3. Create Virtual Environment
Open a Bash console and run:
```bash
cd NOVA
mkvirtualenv --python=/usr/bin/python3.10 nova-env
pip install -r requirements.txt
```

Note: PythonAnywhere free tier supports Python 3.10. If you have paid account, use Python 3.12.

### 4. Configure Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose your domain: `yourusername.pythonanywhere.com`
4. Select **Manual configuration**
5. Choose **Python 3.10**

### 5. Set Up WSGI File

1. Click on **WSGI configuration file** link
2. Replace contents with:

```python
import sys
import os

# Update with YOUR username
project_home = '/home/yourusername/NOVA'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

from app import app as application
```

### 6. Configure Paths

In the **Web** tab, set:

- **Source code**: `/home/yourusername/NOVA`
- **Working directory**: `/home/yourusername/NOVA`
- **Virtualenv**: `/home/yourusername/.virtualenvs/nova-env`

### 7. Set Environment Variables

Scroll to **Environment variables** section and add:

```
ASSEMBLYAI_API_KEY=676b11eafeba4a5d8204b38fff08e05a
WOLFRAM_ALPHA_APP_ID=U7VEX3UA5V
GOOGLE_API_KEY=AIzaSyDjK5azqbokYVNDoD4d0gi2IsL-8f8SZTM
GOOGLE_SEARCH_ENGINE_ID=e02b81f92c7e64ca7
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 8. Create .env File (Alternative)

Or upload `.env` file via Files tab with above variables.

### 9. Reload Web App

Click the green **Reload** button at the top of the Web tab.

### 10. Visit Your App

Go to: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Error: No module named 'X'
```bash
workon nova-env
pip install -r requirements.txt
```

### Error: Can't find .env file
- Ensure `.env` exists in `/home/yourusername/NOVA/`
- Or set environment variables in Web tab

### Error: 502 Bad Gateway
- Check error logs in Web tab
- Verify WSGI file has correct paths
- Ensure app imports correctly: `from app import app`

### spaCy Model Not Found
```bash
workon nova-env
python -m spacy download en_core_web_sm
```

### Static Files Not Loading
- Go to Web tab → Static files section
- Add: URL `/static/` → Directory `/home/yourusername/NOVA/static/`

## Free Tier Limitations

- **CPU**: Limited seconds per day
- **Storage**: 512 MB
- **Always-on**: No (app sleeps after inactivity)
- **HTTPS**: Included
- **Custom domain**: Not available

## Upgrade Benefits

- More CPU time
- More storage
- Always-on apps
- Custom domains
- More consoles

## Performance Tips

1. **Minimize API calls**: Cache results when possible
2. **Optimize imports**: Only import what you need
3. **Use CDN**: For large static files
4. **Database**: Use MySQL/PostgreSQL instead of in-memory storage
5. **Scheduled tasks**: Use PythonAnywhere's scheduled tasks

## Alternative: Use Heroku/Render

If you need better performance:
- **Heroku**: Use `Procfile` (already included)
- **Render**: Use `requirements.txt` (already included)

Both support automatic deployments from Git.

## Support

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Documentation: https://help.pythonanywhere.com/

---

Good luck with your deployment! 🚀
