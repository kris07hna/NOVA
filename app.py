from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Import AI agent modules
from ai_agent.nlp_processor import NLPProcessor
from ai_agent.commands import CommandHandler
from ai_agent.speech_handler import SpeechHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize AI components
nlp_processor = NLPProcessor()
command_handler = CommandHandler()
speech_handler = SpeechHandler()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_command():
    """Process text commands from the user"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Processing command: {user_input}")
        
        # Process the command using NLP
        intent = nlp_processor.detect_intent(user_input)
        logger.info(f"Detected intent: {intent}")
        
        # Handle the command based on intent (now returns dict with thinking process)
        result = command_handler.handle_command(intent, user_input)
        
        # Handle both old string format and new dict format for compatibility
        if isinstance(result, dict):
            return jsonify({
                'response': result.get('answer', ''),
                'thinking': result.get('thinking', ''),
                'intent': result.get('intent', intent)
            })
        else:
            # Fallback for old string format
            return jsonify({
                'response': result,
                'intent': intent
            })
    
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({'error': f'Error processing command: {str(e)}'}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text using AssemblyAI"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Use AssemblyAI for better accuracy
        text = speech_handler.audio_to_text_assemblyai(audio_file)
        
        # Fallback to old method if AssemblyAI fails
        if not text:
            logger.warning("AssemblyAI failed, trying fallback method")
            text = speech_handler.audio_to_text(audio_file)
        
        if text:
            logger.info(f"Transcribed: {text}")
            return jsonify({'text': text, 'success': True})
        else:
            return jsonify({'error': 'Could not understand audio'}), 400
    
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        return jsonify({'error': f'Error processing audio: {str(e)}'}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate speech from text
        audio_data = speech_handler.text_to_audio(text)
        
        if audio_data:
            return jsonify({
                'success': True,
                'message': 'Text-to-speech generated successfully'
            })
        else:
            return jsonify({'error': 'Could not generate speech'}), 500
    
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        return jsonify({'error': f'Error generating speech: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Personal Assistant is running'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
