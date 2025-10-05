import re
import logging

logger = logging.getLogger(__name__)

try:
    import spacy
    # Try to load spaCy model
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
        logger.info("spaCy loaded successfully")
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
        SPACY_AVAILABLE = False
        nlp_spacy = None
except ImportError:
    logger.warning("spaCy not installed")
    SPACY_AVAILABLE = False
    nlp_spacy = None

class NLPProcessor:
    """
    Natural Language Processing for intent detection
    Uses spaCy for text processing and pattern matching for command classification
    """
    
    def __init__(self):
        self.spacy_nlp = nlp_spacy
        self.spacy_available = SPACY_AVAILABLE
        
        # Define intent patterns with improved natural language understanding
        self.intent_patterns = {
            'time': [
                r'\b(what|tell|give|show).*time\b',
                r'\btime\s+(is\s+)?it\b',
                r'\bcurrent\s+time\b',
                r'\bwhat.*clock\b',
                r'\bwhat.*hour\b',
                r'\bhow\s+late\s+is\s+it\b',
                r'\bdo\s+you\s+know\s+the\s+time\b',
                r'\bcan\s+you\s+tell.*time\b'
            ],
            'date': [
                r'\b(what|tell|give|show).*date\b',
                r'\bdate\s+(is\s+)?it\b',
                r'\bcurrent\s+date\b',
                r'\btoday.*date\b',
                r'\bwhat.*today\b',
                r'\bwhat.*day.*today\b',
                r'\btoday\'?s\s+date\b',
                r'\btell.*today\b',
                r'\bwhat\'?s\s+today\b'
            ],
            'math': [
                r'\b(calculate|compute|solve|what\s+is|how\s+much)\b.*[\d\+\-\*/\(\)]+',
                r'\d+\s*[\+\-\*/]\s*\d+',
                r'\bmathematical\b',
                r'\bequals?\b',
                r'\bplus|minus|times|divided|multiply|divide|add|subtract\b',
                r'\bsum\s+of\b',
                r'\bdifference\s+between\b',
                r'\bproduct\s+of\b',
                r'\bquotient\s+of\b'
            ],
            'search': [
                r'\b(search|find|google|look\s+up|look\s+for|show\s+me)\b',
                r'\btell\s+me\s+(about|more\s+about)\b',
                r'\bwhat\s+(is|are|was|were)\b.*(?!time|date)',
                r'\blatest\s+(news|info|information|updates?)\b',
                r'\bwho\s+(is|are|was|were)\b',
                r'\bwhere\s+(is|are|can\s+i\s+find)\b',
                r'\bwhen\s+(is|are|did|was)\b',
                r'\bhow\s+to\b',
                r'\bexplain\b',
                r'\binformation\s+about\b',
                r'\bdetails\s+about\b',
                r'\bcan\s+you\s+(find|search|look)\b'
            ],
            'reminder': [
                r'\b(remind|reminder|remember|don\'t\s+forget)\b',
                r'\bset\s+(a\s+)?reminder\b',
                r'\balert\s+me\b',
                r'\bmake\s+a\s+note\b',
                r'\bnote\s+to\s+self\b',
                r'\bkeep\s+in\s+mind\b'
            ],
            'weather': [
                r'\b(weather|temperature|forecast)\b',
                r'\bhow.*hot|cold|warm\b',
                r'\braining|sunny|cloudy\b',
                r'\bclimate\b',
                r'\bwhat.*weather\b'
            ],
            'greeting': [
                r'\b(hello|hi|hey|greetings|good\s+(morning|afternoon|evening)|howdy|yo)\b',
                r'\bhow\s+are\s+you\b',
                r'\bwhat\'?s\s+up\b',
                r'\bhow\s+is\s+it\s+going\b',
                r'\bhow\s+do\s+you\s+do\b',
                r'^(hi|hey|hello)$'
            ],
            'help': [
                r'\b(help|assist|what\s+can\s+you\s+do|commands|capabilities)\b',
                r'\bshow\s+me\b.*\bcommands?\b',
                r'\bwhat\s+are\s+you\s+capable\b',
                r'\blist.*features\b',
                r'\bwhat\s+do\s+you\s+do\b'
            ]
        }
    
    def preprocess_text_with_spacy(self, text):
        """
        Preprocess text using spaCy for better understanding
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Processed text information including tokens, lemmas, entities, POS tags
        """
        if not self.spacy_available or not self.spacy_nlp:
            return None
        
        try:
            doc = self.spacy_nlp(text)
            
            return {
                'tokens': [token.text for token in doc],
                'lemmas': [token.lemma_ for token in doc],
                'pos_tags': [token.pos_ for token in doc],
                'entities': [(ent.text, ent.label_) for ent in doc.ents],
                'noun_chunks': [chunk.text for chunk in doc.noun_chunks]
            }
        except Exception as e:
            logger.error(f"spaCy preprocessing error: {str(e)}")
            return None
    
    def detect_intent(self, text):
        """
        Detect the intent from user input text using pattern matching
        Enhanced with spaCy text processing when available
        
        Args:
            text (str): User input text
            
        Returns:
            str: Detected intent
        """
        # Use spaCy for text preprocessing if available
        if self.spacy_available:
            spacy_info = self.preprocess_text_with_spacy(text)
            if spacy_info:
                logger.info(f"spaCy analysis - Entities: {spacy_info['entities']}, POS: {spacy_info['pos_tags']}")
        
        text_lower = text.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    logger.info(f"Matched intent '{intent}' with pattern '{pattern}'")
                    return intent
        
        # Default to unknown if no pattern matches
        logger.info("No intent matched, defaulting to 'unknown'")
        return 'unknown'
    
    def extract_entities(self, text, intent):
        """
        Extract entities from text based on intent
        Uses spaCy for enhanced entity recognition when available
        
        Args:
            text (str): User input text
            intent (str): Detected intent
            
        Returns:
            dict: Extracted entities
        """
        entities = {}
        
        # Use spaCy for entity extraction if available
        if self.spacy_available:
            spacy_info = self.preprocess_text_with_spacy(text)
            if spacy_info and spacy_info['entities']:
                entities['spacy_entities'] = spacy_info['entities']
                logger.info(f"spaCy extracted entities: {spacy_info['entities']}")
        
        if intent == 'math':
            # Extract mathematical expression
            math_match = re.search(r'[\d\+\-\*/\(\)\.\s]+', text)
            if math_match:
                entities['expression'] = math_match.group(0).strip()
        
        elif intent == 'search':
            # Extract search query
            search_patterns = [
                r'(?:search|find|google|look\s+(?:up|for))\s+(.+)',
                r'tell\s+me\s+about\s+(.+)',
                r'what\s+is\s+(.+)',
                r'latest\s+(?:news|info)\s+(?:on|about)\s+(.+)'
            ]
            for pattern in search_patterns:
                match = re.search(pattern, text.lower())
                if match:
                    entities['query'] = match.group(1).strip()
                    break
            
            # If no pattern matched, use the whole text as query
            if 'query' not in entities:
                entities['query'] = text
        
        elif intent == 'reminder':
            # Extract reminder text
            reminder_patterns = [
                r'(?:remind|reminder)\s+(?:me\s+)?(?:to\s+)?(?:about\s+)?(.+)',
                r'set\s+(?:a\s+)?reminder\s+(?:for\s+)?(.+)',
                r'don\'t\s+forget\s+(?:to\s+)?(.+)'
            ]
            for pattern in reminder_patterns:
                match = re.search(pattern, text.lower())
                if match:
                    entities['reminder_text'] = match.group(1).strip()
                    break
            
            # Extract time if present
            time_match = re.search(r'(\d{1,2})\s*(?::|\.)\s*(\d{2})\s*(am|pm)?', text.lower())
            if time_match:
                entities['time'] = time_match.group(0)
        
        return entities
