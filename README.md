# NOVA - AI Personal Assistant

A modern AI-powered personal assistant with self-thinking capabilities, voice commands, and a professional neural network interface.

## Features

- 🧠 **Self-Thinking AI**: See step-by-step reasoning process
- 🎤 **Voice Commands**: AssemblyAI-powered speech recognition
- 🔢 **Smart Calculations**: WolframAlpha & Google Search integration
- 💬 **Natural Language**: Advanced NLP with intent detection
- 🎨 **Professional UI**: Glassmorphism design with Lottie animations
- 🌐 **Easy Deployment**: Ready for PythonAnywhere, Heroku, or Render

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys in `.env`**
   ```bash
   ASSEMBLYAI_API_KEY=your_key
   WOLFRAM_ALPHA_APP_ID=your_key
   GOOGLE_API_KEY=your_key
   GOOGLE_SEARCH_ENGINE_ID=your_key
   ```

3. **Run the app**
   ```bash
   python run.py
   ```

4. **Open browser**: http://localhost:5000

## Deploy to PythonAnywhere

1. **Sign up**: Create account at https://www.pythonanywhere.com/
2. **Upload files**: Use "Files" tab or git clone
3. **Create virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 nova-env
   pip install -r requirements.txt
   ```
4. **Configure Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code: `/home/yourusername/NOVA`
   - Set working directory: `/home/yourusername/NOVA`
   - Edit WSGI file to point to `wsgi.py`
   - Set virtualenv path: `/home/yourusername/.virtualenvs/nova-env`
5. **Set environment variables**:
   - Go to "Web" tab → scroll to "Environment variables"
   - Add all API keys from `.env` file
6. **Reload** web app and visit your URL!

## Tech Stack

- **Backend**: Python 3.12, Flask 3.0, spaCy 3.7
- **Speech**: AssemblyAI 0.44, pyttsx3 2.90
- **APIs**: WolframAlpha 5.0, Google Custom Search
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript ES6+

## API Keys

- **AssemblyAI**: https://www.assemblyai.com/
- **WolframAlpha**: https://products.wolframalpha.com/api/
- **Google Search**: https://console.cloud.google.com/apis/credentials

## License

MIT License - see LICENSE file

---

**Made with ❤️ for AdihaOne Interview**
