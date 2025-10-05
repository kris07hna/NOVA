# PythonAnywhere Quick Reference

## URLs
- **Your App**: https://yourusername.pythonanywhere.com
- **Dashboard**: https://www.pythonanywhere.com/user/yourusername/
- **Web Tab**: https://www.pythonanywhere.com/user/yourusername/webapps/
- **Files**: https://www.pythonanywhere.com/user/yourusername/files/
- **Consoles**: https://www.pythonanywhere.com/user/yourusername/consoles/

## Quick Setup Commands

```bash
# Clone project (if using Git)
cd ~
git clone https://github.com/yourusername/NOVA.git
cd NOVA

# Or run setup script
bash setup_pythonanywhere.sh

# Manual setup
mkvirtualenv --python=/usr/bin/python3.10 nova-env
pip install -r requirements.txt
```

## WSGI Configuration Template

```python
import sys
import os

# ⚠️ UPDATE THIS LINE WITH YOUR USERNAME
project_home = '/home/YOURUSERNAME/NOVA'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

from app import app as application
```

## Environment Variables (Web Tab)

```
ASSEMBLYAI_API_KEY=676b11eafeba4a5d8204b38fff08e05a
WOLFRAM_ALPHA_APP_ID=U7VEX3UA5V
GOOGLE_API_KEY=AIzaSyDjK5azqbokYVNDoD4d0gi2IsL-8f8SZTM
GOOGLE_SEARCH_ENGINE_ID=e02b81f92c7e64ca7
FLASK_ENV=production
SECRET_KEY=nova-secret-2024-pythonanywhere
```

## Web App Configuration

| Setting | Value |
|---------|-------|
| Source code | `/home/yourusername/NOVA` |
| Working directory | `/home/yourusername/NOVA` |
| Virtualenv | `/home/yourusername/.virtualenvs/nova-env` |
| Python version | 3.10 |
| WSGI file | Click to edit, use template above |

## Static Files Configuration

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/NOVA/static/` |

## Common Commands

```bash
# Activate virtual environment
workon nova-env

# Install/update packages
pip install -r requirements.txt

# Check installed packages
pip list

# Test Flask app locally
python app.py

# View logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
tail -f /var/log/yourusername.pythonanywhere.com.server.log

# Git pull updates
cd ~/NOVA
git pull origin main
# Then reload web app in Web tab
```

## Debugging

### View Error Logs
Web Tab → Log files → Error log

### Common Issues

**502 Bad Gateway**
- Check WSGI file syntax
- Verify paths in WSGI file
- Check error log

**Module not found**
```bash
workon nova-env
pip install <module-name>
```

**Static files not loading**
- Add static files mapping in Web tab
- Check file permissions

**App changes not visible**
- Click "Reload" button in Web tab
- Clear browser cache

## File Structure on PythonAnywhere

```
/home/yourusername/
├── NOVA/                          # Your project
│   ├── ai_agent/
│   ├── static/
│   ├── templates/
│   ├── app.py
│   ├── wsgi.py                    # Important!
│   ├── .env                       # Your API keys
│   └── requirements.txt
└── .virtualenvs/
    └── nova-env/                  # Virtual environment
```

## Reload Web App

After any code changes:
1. Go to Web tab
2. Click green **Reload** button
3. Wait 5-10 seconds
4. Visit your URL

## Performance Tips

- Minimize API calls
- Use caching where possible
- Optimize database queries
- Keep dependencies minimal
- Monitor CPU usage in Dashboard

## Support

- Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Contact: Via "Send feedback" button

---

**Remember**: Free accounts have limited CPU seconds per day. Monitor usage in Dashboard!
