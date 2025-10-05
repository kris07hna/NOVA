import io
import logging
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class SpeechHandler:
    """
    Handles speech-to-text and text-to-speech functionality
    Uses AssemblyAI for high-accuracy speech recognition
    """
    
    def __init__(self):
        self.tts_engine = None
        self.recognizer = None
        self.assemblyai_key = os.getenv('ASSEMBLYAI_API_KEY')
        self._init_tts()
        self._init_speech_recognition()
        self._init_assemblyai()
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            # Set properties
            self.tts_engine.setProperty('rate', 175)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            logger.info("Text-to-speech engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {str(e)}")
            self.tts_engine = None
    
    def _init_speech_recognition(self):
        """Initialize speech recognition (legacy support)"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            logger.info("Speech recognition initialized")
        except Exception as e:
            logger.error(f"Failed to initialize speech recognition: {str(e)}")
            self.recognizer = None
    
    def _init_assemblyai(self):
        """Initialize AssemblyAI"""
        try:
            import assemblyai as aai
            if self.assemblyai_key:
                aai.settings.api_key = self.assemblyai_key
                logger.info("AssemblyAI initialized")
            else:
                logger.warning("AssemblyAI API key not found")
        except Exception as e:
            logger.error(f"Failed to initialize AssemblyAI: {str(e)}")
    
    def audio_to_text(self, audio_file):
        """
        Convert audio file to text
        
        Args:
            audio_file: Audio file object
            
        Returns:
            str: Transcribed text or None
        """
        if not self.recognizer:
            logger.error("Speech recognizer not initialized")
            return None
        
        try:
            import speech_recognition as sr
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                audio_file.save(temp_audio.name)
                temp_path = temp_audio.name
            
            try:
                # Load audio file
                with sr.AudioFile(temp_path) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Record audio
                    audio_data = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                logger.info(f"Transcribed text: {text}")
                return text
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error in audio-to-text: {str(e)}")
            return None
    
    def audio_to_text_assemblyai(self, audio_file):
        """
        Convert audio file to text using AssemblyAI (more accurate)
        
        Args:
            audio_file: Audio file object or path
            
        Returns:
            str: Transcribed text or None
        """
        if not self.assemblyai_key:
            logger.error("AssemblyAI API key not configured")
            return None
        
        try:
            import assemblyai as aai
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                if hasattr(audio_file, 'save'):
                    audio_file.save(temp_audio.name)
                else:
                    # If it's a path
                    with open(audio_file, 'rb') as f:
                        temp_audio.write(f.read())
                temp_path = temp_audio.name
            
            try:
                # Configure transcription
                config = aai.TranscriptionConfig(
                    speech_model=aai.SpeechModel.universal,
                    language_detection=True,
                )
                
                # Transcribe
                logger.info("Transcribing audio with AssemblyAI...")
                transcriber = aai.Transcriber(config=config)
                transcript = transcriber.transcribe(temp_path)
                
                if transcript.status == aai.TranscriptStatus.error:
                    logger.error(f"AssemblyAI transcription failed: {transcript.error}")
                    return None
                
                logger.info(f"Transcribed text: {transcript.text}")
                return transcript.text
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        except Exception as e:
            logger.error(f"Error in AssemblyAI audio-to-text: {str(e)}")
            return None
    
    def text_to_audio(self, text):
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.tts_engine:
            logger.error("TTS engine not initialized")
            return False
        
        try:
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            logger.info(f"Text-to-speech completed for: {text[:50]}...")
            return True
        
        except Exception as e:
            logger.error(f"Error in text-to-audio: {str(e)}")
            return False
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except Exception as e:
                logger.error(f"Error stopping speech: {str(e)}")
