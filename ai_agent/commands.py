import datetime
import re
import requests
from bs4 import BeautifulSoup
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class CommandHandler:
    """
    Handles different types of commands and generates responses
    """
    
    def __init__(self):
        self.wolfram_app_id = os.getenv('WOLFRAM_ALPHA_APP_ID')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.reminders = []  # Simple in-memory storage for reminders
    
    def generate_thinking_process(self, intent, user_input):
        """
        Generate a step-by-step thinking process for the AI
        
        Args:
            intent (str): Detected intent
            user_input (str): Original user input
            
        Returns:
            str: Thinking process explanation
        """
        thinking_steps = {
            'time': [
                "🤔 Analyzing your request...",
                "📍 Identifying that you want to know the current time",
                "⏰ Accessing system time information",
                "✅ Formatting time in a readable format"
            ],
            'date': [
                "🤔 Processing your query...",
                "📅 Detecting that you're asking about the date",
                "🔍 Retrieving current date information",
                "✅ Preparing date response with day of the week"
            ],
            'math': [
                "🤔 Analyzing mathematical expression...",
                "🔢 Breaking down the calculation steps",
                "🧮 Checking if I need WolframAlpha for complex math",
                "💡 Computing the result with precision",
                "✅ Verifying the answer"
            ],
            'search': [
                "🤔 Understanding your search query...",
                "🔍 Identifying key search terms",
                "🌐 Preparing to search across the web",
                "📊 Using Google Custom Search API for best results",
                "✅ Compiling relevant information"
            ],
            'reminder': [
                "🤔 Processing your reminder request...",
                "📝 Extracting reminder details and timing",
                "💾 Storing reminder in memory",
                "✅ Setting up reminder notification"
            ],
            'weather': [
                "🤔 Analyzing weather request...",
                "🌍 Detecting location information",
                "☁️ Preparing to fetch weather data",
                "✅ Compiling weather information"
            ],
            'greeting': [
                "🤔 Recognizing a friendly greeting!",
                "😊 Determining appropriate response tone",
                "✅ Preparing a warm response"
            ],
            'unknown': [
                "🤔 Analyzing your request...",
                "🔍 Trying to understand the context",
                "💭 Considering best way to assist you",
                "✅ Preparing helpful response"
            ]
        }
        
        steps = thinking_steps.get(intent, thinking_steps['unknown'])
        return "\n".join(steps)
    
    def handle_command(self, intent, user_input):
        """
        Main command handler that routes to specific handlers
        
        Args:
            intent (str): Detected intent
            user_input (str): Original user input
            
        Returns:
            dict: Response with thinking process and answer
        """
        # Generate thinking process
        thinking = self.generate_thinking_process(intent, user_input)
        
        handlers = {
            'time': self.handle_time,
            'date': self.handle_date,
            'math': self.handle_math,
            'search': self.handle_search,
            'reminder': self.handle_reminder,
            'weather': self.handle_weather,
            'greeting': self.handle_greeting,
            'help': self.handle_help,
            'unknown': self.handle_unknown
        }
        
        handler = handlers.get(intent, self.handle_unknown)
        answer = handler(user_input)
        
        return {
            'thinking': thinking,
            'answer': answer,
            'intent': intent
        }
    
    def handle_time(self, user_input):
        """Handle time-related queries"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}."
    
    def handle_date(self, user_input):
        """Handle date-related queries"""
        now = datetime.datetime.now()
        date_str = now.strftime("%B %d, %Y")
        day_name = now.strftime("%A")
        return f"Today is {day_name}, {date_str}."
    
    def handle_math(self, user_input):
        """Handle mathematical calculations"""
        try:
            # Extract the mathematical expression
            # Clean the input
            user_input_lower = user_input.lower()
            
            # Replace word operators with symbols
            replacements = {
                'plus': '+',
                'minus': '-',
                'times': '*',
                'multiplied by': '*',
                'divided by': '/',
                'x': '*',
                'to the power of': '**',
                'squared': '**2',
                'cubed': '**3'
            }
            
            expression = user_input_lower
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Extract numeric expression
            match = re.search(r'[\d\+\-\*/\(\)\.\s\*]+', expression)
            if match:
                expression = match.group(0).strip()
                
                # Safely evaluate the expression
                # Remove any potentially dangerous characters
                safe_expression = re.sub(r'[^0-9\+\-\*/\(\)\.\s\*]', '', expression)
                
                if safe_expression:
                    try:
                        result = eval(safe_expression)
                        return f"The result is {result}."
                    except:
                        pass
            
            # Try WolframAlpha if available
            if self.wolfram_app_id and self.wolfram_app_id != 'your_wolfram_alpha_app_id_here':
                try:
                    import wolframalpha
                    client = wolframalpha.Client(self.wolfram_app_id)
                    res = client.query(user_input)
                    answer = next(res.results).text
                    return f"The answer is {answer}."
                except Exception as e:
                    logger.error(f"WolframAlpha error: {str(e)}")
            
            return "I couldn't solve that mathematical problem. Please try rephrasing it as a simple calculation."
        
        except Exception as e:
            logger.error(f"Math error: {str(e)}")
            return "I encountered an error while trying to calculate that. Please try again."
    
    def handle_search(self, user_input):
        """Handle web search queries using Google Custom Search API with image support"""
        try:
            # Extract search query with more patterns
            search_patterns = [
                r'(?:search|find|google|look\s+(?:up|for)|show\s+me)\s+(.+)',
                r'tell\s+me\s+(?:about|more\s+about)\s+(.+)',
                r'what\s+(?:is|are|was|were)\s+(.+)',
                r'who\s+(?:is|are|was|were)\s+(.+)',
                r'where\s+(?:is|are|can\s+i\s+find)\s+(.+)',
                r'when\s+(?:is|are|did|was)\s+(.+)',
                r'how\s+to\s+(.+)',
                r'latest\s+(?:news|info|information|updates?)\s+(?:on|about)?\s*(.+)',
                r'information\s+(?:about|on)\s+(.+)',
                r'details\s+(?:about|on)\s+(.+)',
                r'explain\s+(.+)'
            ]
            
            query = None
            for pattern in search_patterns:
                match = re.search(pattern, user_input.lower())
                if match:
                    query = match.group(1).strip()
                    break
            
            if not query:
                query = user_input
            
            # Try Google Custom Search API first (if configured)
            if self.google_api_key and self.google_api_key != 'your_google_api_key_here' and \
               self.google_search_engine_id and self.google_search_engine_id != 'your_search_engine_id_here':
                try:
                    search_url = "https://www.googleapis.com/customsearch/v1"
                    params = {
                        'key': self.google_api_key,
                        'cx': self.google_search_engine_id,
                        'q': query,
                        'num': 3  # Get top 3 results
                    }
                    
                    response = requests.get(search_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'items' in data and len(data['items']) > 0:
                            # Get the first result
                            result = data['items'][0]
                            title = result.get('title', '')
                            snippet = result.get('snippet', '')
                            link = result.get('link', '')
                            
                            # Try to get image if available
                            image_url = None
                            if 'pagemap' in result:
                                if 'cse_image' in result['pagemap']:
                                    image_url = result['pagemap']['cse_image'][0].get('src')
                                elif 'metatags' in result['pagemap'] and len(result['pagemap']['metatags']) > 0:
                                    metatags = result['pagemap']['metatags'][0]
                                    image_url = metatags.get('og:image') or metatags.get('twitter:image')
                            
                            # Build response with special format for images
                            response_data = {
                                'text': f"Here's what I found about '{query}':\n\n📌 {title}\n{snippet}\n\n🔗 Source: {link}",
                                'image': image_url,
                                'query': query,
                                'link': link
                            }
                            
                            # Return formatted response that frontend can parse
                            import json
                            return json.dumps(response_data)
                        else:
                            return f"I couldn't find any results for '{query}'. Try rephrasing your search."
                    else:
                        logger.error(f"Google API error: {response.status_code}")
                
                except Exception as e:
                    logger.error(f"Google Custom Search API error: {str(e)}")
                    # Fall through to web scraping method
            
            # Fallback to web scraping (less reliable)
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                search_url = f"https://www.google.com/search?q={query}"
                response = requests.get(search_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Try to extract featured snippet
                    featured = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
                    if featured:
                        snippet = featured.get_text()
                        return f"Here's what I found about '{query}': {snippet}"
                    
                    # Extract search results
                    search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
                    if search_results:
                        result_text = search_results[0].get_text()
                        return f"I found this about '{query}': {result_text}"
            except Exception as scrape_error:
                logger.error(f"Web scraping error: {str(scrape_error)}")
            
            return f"I can search for '{query}', but I need a Google API key to retrieve results. Visit: https://www.google.com/search?q={query.replace(' ', '+')}"
        
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return f"I can help you search for that. Try visiting Google with your query: {user_input}"
    
    def handle_reminder(self, user_input):
        """Handle reminder creation"""
        try:
            # Extract reminder text
            reminder_patterns = [
                r'(?:remind|reminder)\s+(?:me\s+)?(?:to\s+)?(?:about\s+)?(.+)',
                r'set\s+(?:a\s+)?reminder\s+(?:for\s+)?(.+)',
                r'don\'t\s+forget\s+(?:to\s+)?(.+)'
            ]
            
            reminder_text = None
            for pattern in reminder_patterns:
                match = re.search(pattern, user_input.lower())
                if match:
                    reminder_text = match.group(1).strip()
                    break
            
            if not reminder_text:
                reminder_text = user_input
            
            # Extract time if present
            time_match = re.search(r'(\d{1,2})\s*(?::|\.)\s*(\d{2})\s*(am|pm)?', user_input.lower())
            time_str = ""
            if time_match:
                time_str = f" at {time_match.group(0)}"
            
            # Store reminder
            reminder = {
                'text': reminder_text,
                'time': time_str,
                'created': datetime.datetime.now().isoformat()
            }
            self.reminders.append(reminder)
            
            return f"I'll remind you{time_str}: {reminder_text}"
        
        except Exception as e:
            logger.error(f"Reminder error: {str(e)}")
            return "I couldn't set that reminder. Please try again."
    
    def handle_weather(self, user_input):
        """Handle weather queries"""
        return "I don't have access to weather data at the moment. You can check weather.com or your local weather service for current conditions."
    
    def handle_greeting(self, user_input):
        """Handle greeting messages"""
        now = datetime.datetime.now()
        hour = now.hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        responses = [
            f"{greeting}! How can I assist you today?",
            f"Hello! I'm your AI personal assistant. What can I do for you?",
            f"{greeting}! I'm here to help. What do you need?"
        ]
        
        import random
        return random.choice(responses)
    
    def handle_help(self, user_input):
        """Handle help requests"""
        help_text = """I'm your AI personal assistant! Here's what I can do:

🕐 **Time & Date**: Ask me "What time is it?" or "What's today's date?"

🔢 **Math**: Ask me to calculate things like "What is 25 times 4?"

🔍 **Search**: Ask me to "Search for latest AI news" or "Tell me about Python programming"

⏰ **Reminders**: Tell me to "Remind me to call John at 3 PM"

👋 **Chat**: Just say hi and chat with me!

Try asking me anything from the list above!"""
        
        return help_text
    
    def handle_unknown(self, user_input):
        """Handle unknown intents"""
        return "I'm not sure I understood that. Try asking me about the time, to do a calculation, search for something, or set a reminder. Say 'help' to see what I can do!"
