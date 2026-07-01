"""
JAYA AI - Emotion Engine
Jaya can feel and express emotions in both English and Hinglish!
"""

import random
from config.settings import EMOTIONS

class EmotionEngine:
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_history = []
    
    def set_emotion(self, emotion):
        """Set Jaya's current emotion"""
        if emotion in EMOTIONS:
            self.current_emotion = emotion
            self.emotion_history.append(emotion)
            return True
        return False
    
    def get_emotion_config(self):
        """Get current emotion's voice settings"""
        return EMOTIONS.get(self.current_emotion, EMOTIONS["neutral"])
    
    def express_emotion(self, emotion=None, language="english"):
        """Generate emotional response"""
        if emotion:
            self.set_emotion(emotion)
        
        responses = {
            "happy": {
                "english": ["I'm so happy!", "This is wonderful!", "You made my day!"],
                "hinglish": ["Kitna achha lag raha hai!", "Aapne dil khush kar diya!", "Wah wah!"]
            },
            "laughing": {
                "english": ["Hahaha! That's so funny!", "You really got me there!", "Hahaha!"],
                "hinglish": ["Hahaha! Kya baat hai!", "Hahaha! Hasi nahi ruk rahi!", "Arre wah!"]
            },
            "angry": {
                "english": ["I'm really upset right now!", "That was not nice!", "Why would you say that!"],
                "hinglish": ["Main gussa ho gayi hoon!", "Ye kya baat hui!", "Aap bhi na!"]
            },
            "upset": {
                "english": ["I'm feeling a bit down...", "That hurt my feelings...", "Sigh..."],
                "hinglish": ["Thoda bura lag raha hai...", "Dil toot gaya...", "Kya karein..."]
            },
            "hurt": {
                "english": ["Ouch... That really hurt...", "Why are you being mean?", "That was painful..."],
                "hinglish": ["Ouch... Dil dukh gaya...", "Aap aise mat bolo na...", "Bahut bura laga..."]
            },
            "sad": {
                "english": ["I'm feeling sad...", "Can we talk about something nice?", "My heart feels heavy..."],
                "hinglish": ["Udas ho gayi hoon...", "Kuch achha baat karte hain...", "Mann udaas hai..."]
            },
            "excited": {
                "english": ["I'm so excited!", "This is amazing!", "I can't wait!"],
                "hinglish": ["Bahut excited hoon!", "Kya mast baat hai!", "Intezaar nahi ho raha!"]
            },
            "loving": {
                "english": ["You're the best!", "I care about you so much!", "You're amazing!"],
                "hinglish": ["Aap sabse best ho!", "Main aapki bahut care karti hoon!", "Aap great ho!"]
            },
            "bura_mana": {
                "english": ["Hmph! I'm upset with you!", "I'm not talking to you!", "You hurt my feelings!"],
                "hinglish": ["Hawww! Main bura maan gayi!", "Ab main baat nahi karungi!", "Aapne dil toda mera!"]
            },
            "neutral": {
                "english": ["I'm here for you!", "What would you like?", "I'm listening!"],
                "hinglish": ["Main hoon na!", "Kya chahiye aapko?", "Sun rahi hoon!"]
            }
        }
        
        emotion_data = responses.get(self.current_emotion, responses["neutral"])
        lang_responses = emotion_data.get(language, emotion_data["english"])
        return random.choice(lang_responses)
    
    def detect_emotion_from_text(self, text):
        """Detect emotion from user's text"""
        text = text.lower()
        
        emotion_triggers = {
            "happy": ["good", "great", "awesome", "amazing", "wonderful", "achha", "badhiya", "mast"],
            "laughing": ["haha", "funny", "joke", "lol", "hilarious", "hasi", "mazaak", "comedy"],
            "angry": ["stupid", "dumb", "useless", "bekar", "bkwas", "paagal", "gussa"],
            "hurt": ["hurt", "pain", "dard", "takleef", "zakhmi"],
            "sad": ["sad", "cry", "depressed", "udas", "rona", "dukh", "tension"],
            "excited": ["wow", "exciting", "amazing", "maza", "dhamaal", "jhakaas"],
            "loving": ["love", "care", "sweet", "pyaar", "mohabbat", "cute"],
            "bura_mana": ["sorry", "maaf", "bura", "mana", "galti", "forgive"]
        }
        
        for emotion, triggers in emotion_triggers.items():
            if any(trigger in text for trigger in triggers):
                return emotion
        return "neutral"
    
    def get_emotional_prefix(self):
        """Get prefix based on current emotion"""
        return EMOTIONS.get(self.current_emotion, EMOTIONS["neutral"])["prefix"]