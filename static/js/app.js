// Configuration
const API_BASE_URL = window.location.origin;

// State
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];
let recognition = null;
let useAssemblyAI = true;  // Use AssemblyAI for better accuracy

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const voiceButton = document.getElementById('voice-button');
const themeToggle = document.getElementById('theme-toggle');
const inputStatus = document.getElementById('input-status');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeSpeechRecognition();
    attachEventListeners();
    checkServerHealth();
    showWelcomeGreeting();
});

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Event Listeners
function attachEventListeners() {
    sendButton.addEventListener('click', handleSendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    voiceButton.addEventListener('click', handleVoiceInput);
    themeToggle.addEventListener('click', toggleTheme);
}

// Speech Recognition (Browser API)
function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;  // Keep listening
        recognition.interimResults = true;  // Show words as you speak
        recognition.lang = 'en-US';
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isRecording = true;
            voiceButton.classList.add('recording');
            messageInput.classList.add('listening');
            voiceButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="6" height="6"></rect></svg>';
            setStatus('🎤 Listening... (Click again to stop)');
            messageInput.placeholder = 'Speak now...';
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Display interim results (words being spoken)
            if (interimTranscript) {
                messageInput.value = (finalTranscript + interimTranscript).trim();
                setStatus(`🎤 Listening: "${interimTranscript.trim()}"`);
            }

            // When final result is received
            if (finalTranscript) {
                messageInput.value = finalTranscript.trim();
                setStatus('✅ Recognized! Processing...');
                recognition.stop();
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            let errorMessage = 'Speech recognition error';
            
            switch(event.error) {
                case 'no-speech':
                    errorMessage = 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMessage = 'No microphone found. Please check your microphone.';
                    break;
                case 'not-allowed':
                    errorMessage = 'Microphone access denied. Please allow microphone access.';
                    break;
                case 'network':
                    errorMessage = 'Network error. Please check your internet connection.';
                    break;
                default:
                    errorMessage = `Error: ${event.error}`;
            }
            
            setStatus(errorMessage, true);
            isRecording = false;
            voiceButton.classList.remove('recording');
            messageInput.classList.remove('listening');
            voiceButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>';
            messageInput.placeholder = 'Type your message...';
        };

        recognition.onend = () => {
            isRecording = false;
            voiceButton.classList.remove('recording');
            messageInput.classList.remove('listening');
            voiceButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>';
            messageInput.placeholder = 'Type your message...';
            
            if (messageInput.value.trim()) {
                setStatus('');
                // Auto-send after recognition ends
                setTimeout(() => {
                    handleSendMessage();
                }, 500);
            } else {
                setStatus('');
            }
        };
    } else {
        console.log('Speech recognition not supported');
        voiceButton.disabled = true;
        voiceButton.title = 'Speech recognition not supported in this browser';
    }
}

// Handle Voice Input
function handleVoiceInput() {
    if (useAssemblyAI) {
        // Use AssemblyAI method (record and send)
        handleAssemblyAIRecording();
    } else {
        // Use browser Web Speech API (fallback)
        handleBrowserSpeechRecognition();
    }
}

// AssemblyAI Recording Method
async function handleAssemblyAIRecording() {
    if (isRecording) {
        // Stop recording
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        setStatus('Processing audio...');
    } else {
        // Start recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    channelCount: 1,
                    sampleRate: 16000,
                    echoCancellation: true,
                    noiseSuppression: true
                } 
            });
            
            audioChunks = [];
            
            // Try to use specific MIME type for better compatibility
            const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
                ? 'audio/webm;codecs=opus'
                : 'audio/webm';
            
            mediaRecorder = new MediaRecorder(stream, { mimeType });
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                isRecording = false;
                voiceButton.classList.remove('recording');
                messageInput.classList.remove('listening');
                voiceButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>';
                messageInput.placeholder = 'Type your message...';
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
                
                // Create audio blob with correct MIME type
                const audioBlob = new Blob(audioChunks, { type: mimeType });
                
                // Send to server for transcription
                await transcribeAudio(audioBlob);
            };
            
            mediaRecorder.start();
            isRecording = true;
            voiceButton.classList.add('recording');
            messageInput.classList.add('listening');
            voiceButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="6" height="6"></rect></svg>';
            setStatus('🎤 Recording... (Click again to stop)');
            messageInput.placeholder = 'Recording...';
            
        } catch (error) {
            console.error('Error accessing microphone:', error);
            setStatus('❌ Microphone access denied. Please allow microphone access.', true);
        }
    }
}

// Send audio to server for transcription
async function transcribeAudio(audioBlob) {
    try {
        setStatus('🔄 Transcribing with AssemblyAI...');
        
        const formData = new FormData();
        // Use .webm extension to match the actual format
        const filename = audioBlob.type.includes('webm') ? 'recording.webm' : 'recording.wav';
        formData.append('audio', audioBlob, filename);
        
        const response = await fetch(`${API_BASE_URL}/api/speech-to-text`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.text) {
            messageInput.value = data.text;
            setStatus('✅ Transcription complete!');
            
            // Auto-send after short delay
            setTimeout(() => {
                setStatus('');
                handleSendMessage();
            }, 500);
        } else {
            setStatus('❌ Could not understand audio. Please try again.', true);
        }
        
    } catch (error) {
        console.error('Transcription error:', error);
        setStatus('❌ Transcription failed. Please try again.', true);
    }
}

// Browser Speech Recognition (Fallback)
function handleBrowserSpeechRecognition() {
    if (!recognition) {
        setStatus('Voice input not supported in this browser', true);
        return;
    }

    if (isRecording) {
        recognition.stop();
        setStatus('Stopping...');
    } else {
        try {
            messageInput.value = ''; // Clear input
            recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            setStatus('Error starting voice input. Please try again.', true);
        }
    }
}

// Handle Send Message
async function handleSendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;

    // Clear input
    messageInput.value = '';
    messageInput.focus();

    // Hide welcome message with fade out
    const welcomeMessage = document.getElementById('welcome-message');
    if (welcomeMessage) {
        welcomeMessage.style.opacity = '0';
        welcomeMessage.style.transition = 'opacity 0.5s ease-out';
        setTimeout(() => {
            welcomeMessage.remove();
        }, 500);
    }

    // Add user message to chat
    addMessage(message, 'user');

    // Show typing indicator
    const typingId = addTypingIndicator();

    // Disable input while processing
    setInputState(false);

    try {
        // Send message to API
        const response = await fetch(`${API_BASE_URL}/api/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Show thinking process if available
        if (data.thinking) {
            addThinkingMessage(data.thinking);
            // Small delay before showing answer
            await new Promise(resolve => setTimeout(resolve, 800));
        }

        // Parse response for image data
        let responseText = data.response;
        let imageData = null;
        
        try {
            // Try to parse as JSON (for image search results)
            const parsedResponse = JSON.parse(data.response);
            if (parsedResponse.text) {
                responseText = parsedResponse.text;
                imageData = parsedResponse;
            }
        } catch (e) {
            // Not JSON, use as plain text
        }

        // Add assistant response
        if (imageData && imageData.image) {
            addMessageWithImage(responseText, 'assistant', imageData);
        } else {
            addMessage(responseText, 'assistant');
        }

        // Automatically speak the response
        speakText(responseText);

    } catch (error) {
        console.error('Error processing message:', error);
        removeTypingIndicator(typingId);
        addMessage('Sorry, I encountered an error processing your request. Please try again.', 'assistant', true);
    } finally {
        setInputState(true);
    }
}

// Add Thinking Process Message
function addThinkingMessage(thinkingText) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant thinking-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🧠';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content thinking-content';

    const headerDiv = document.createElement('div');
    headerDiv.className = 'thinking-header';
    headerDiv.innerHTML = '<strong>💭 Thinking Process</strong>';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text thinking-text';
    
    // Split thinking steps and animate them
    const steps = thinkingText.split('\n').filter(step => step.trim());
    steps.forEach((step, index) => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'thinking-step';
        stepDiv.textContent = step;
        stepDiv.style.opacity = '0';
        stepDiv.style.animation = `fadeInStep 0.3s ease-out ${index * 0.15}s forwards`;
        textDiv.appendChild(stepDiv);
    });

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    contentDiv.appendChild(headerDiv);
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    scrollToBottom();

    // Show thinking indicator in header
    const thinkingIndicator = document.getElementById('thinking-indicator');
    if (thinkingIndicator) {
        thinkingIndicator.classList.add('active');
        setTimeout(() => {
            thinkingIndicator.classList.remove('active');
        }, steps.length * 150 + 500);
    }
}

// Add Message to Chat
function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    if (isError) contentDiv.style.borderColor = '#ef4444';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add Message with Image (for search results)
function addMessageWithImage(text, sender, imageData) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    // Add image if available
    if (imageData.image) {
        const imageContainer = document.createElement('div');
        imageContainer.className = 'message-image-container';
        
        const img = document.createElement('img');
        img.src = imageData.image;
        img.alt = imageData.query || 'Search result image';
        img.className = 'message-image';
        img.loading = 'lazy';
        
        // Add click to open in new tab
        img.onclick = () => {
            window.open(imageData.link || imageData.image, '_blank');
        };
        
        // Handle image load error
        img.onerror = () => {
            imageContainer.style.display = 'none';
        };
        
        imageContainer.appendChild(img);
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(imageContainer);
    } else {
        contentDiv.appendChild(textDiv);
    }

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add Typing Indicator
function addTypingIndicator() {
    const id = `typing-${Date.now()}`;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = id;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    contentDiv.appendChild(typingDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    scrollToBottom();

    return id;
}

// Remove Typing Indicator
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

// Scroll to Bottom
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Set Input State
function setInputState(enabled) {
    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;
    if (enabled) {
        messageInput.focus();
    }
}

// Set Status Message
function setStatus(message, isError = false) {
    inputStatus.textContent = message;
    inputStatus.style.color = isError ? '#ef4444' : 'var(--color-text-secondary)';
}

// Text to Speech (Improved)
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        // Clean text for speaking (remove URLs and special formatting)
        let cleanText = text
            .replace(/https?:\/\/[^\s]+/g, '') // Remove URLs
            .replace(/📌|🔗|🕐|🔢|🔍|⏰/g, '') // Remove emojis
            .replace(/\n\n/g, '. ') // Replace double newlines with period
            .replace(/\n/g, ' '); // Replace single newlines with space

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 1.0; // Normal speed
        utterance.pitch = 1.0; // Normal pitch
        utterance.volume = 0.9; // Slightly lower volume
        utterance.lang = 'en-US';

        // Try to use a natural voice
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            // Prefer female or natural-sounding voices
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Female') || 
                voice.name.includes('Zira') ||
                voice.name.includes('Samantha') ||
                voice.name.includes('Google')
            ) || voices[0];
            
            utterance.voice = preferredVoice;
        }

        utterance.onstart = () => {
            console.log('Started speaking');
        };

        utterance.onend = () => {
            console.log('Finished speaking');
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
        };

        // Small delay to ensure previous speech is cancelled
        setTimeout(() => {
            window.speechSynthesis.speak(utterance);
        }, 100);
    }
}

// Check Server Health
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            console.log('Server is healthy');
        }
    } catch (error) {
        console.error('Server health check failed:', error);
        setStatus('Warning: Unable to connect to server', true);
    }
}

// Utility: Format Time
function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show Welcome Greeting with Time-based Greeting
function showWelcomeGreeting() {
    const greetingText = document.getElementById('greeting-text');
    const greetingSubtext = document.getElementById('greeting-subtext');
    const introAnimation = document.getElementById('intro-animation');
    
    if (!greetingText) return;
    
    // Get current hour
    const hour = new Date().getHours();
    let greeting = 'Hello!';
    let icon = '👋';
    
    if (hour < 12) {
        greeting = 'Good Morning!';
        icon = '🌅';
    } else if (hour < 17) {
        greeting = 'Good Afternoon!';
        icon = '☀️';
    } else if (hour < 21) {
        greeting = 'Good Evening!';
        icon = '🌆';
    } else {
        greeting = 'Good Night!';
        icon = '🌙';
    }
    
    // Update greeting
    greetingText.textContent = `${icon} ${greeting}`;
    
    // Animate intro text
    if (introAnimation) {
        const messages = [
            "I'm here to assist you with various tasks...",
            "Ask me anything - I'm powered by advanced AI...",
            "Let's make your day more productive together!",
            "Ready to help with searches, calculations, and more..."
        ];
        
        let currentIndex = 0;
        
        function updateIntroText() {
            const introLine = introAnimation.querySelector('.intro-line');
            if (introLine) {
                introLine.style.animation = 'none';
                setTimeout(() => {
                    introLine.textContent = messages[currentIndex];
                    introLine.style.animation = 'typing 2s steps(40, end)';
                    currentIndex = (currentIndex + 1) % messages.length;
                }, 50);
            }
        }
        
        // Change message every 4 seconds
        setInterval(updateIntroText, 4000);
    }
}
