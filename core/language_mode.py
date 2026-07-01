"""
JAYA AI - Language Mode Manager
English (Default) & Hinglish modes
"""

from config.settings import HINGLISH_WAKE_WORDS, DEFAULT_LANGUAGE

class LanguageModeManager:
    def __init__(self):
        self.current_mode = DEFAULT_LANGUAGE  # "english" or "hinglish"
        self.previous_mode = DEFAULT_LANGUAGE
    
    def get_current_mode(self):
        return self.current_mode
    
    def switch_to_hinglish(self):
        """Switch to Hinglish mode"""
        self.previous_mode = self.current_mode
        self.current_mode = "hinglish"
        return "hinglish"
    
    def switch_to_english(self):
        """Switch to English mode"""
        self.previous_mode = self.current_mode
        self.current_mode = "english"
        return "english"
    
    def toggle_mode(self):
        """Toggle between English and Hinglish"""
        if self.current_mode == "english":
            return self.switch_to_hinglish()
        return self.switch_to_english()
    
    def check_wake_word_for_hinglish(self, text):
        """Check if Hinglish wake word was spoken"""
        text_lower = text.lower()
        return any(wake in text_lower for wake in HINGLISH_WAKE_WORDS)
    
    def check_switch_to_english(self, text):
        """Check if user wants to switch back to English"""
        text_lower = text.lower()
        english_triggers = ["english mode", "switch to english", "angrezi", "english mein"]
        return any(trigger in text_lower for trigger in english_triggers)
    
    def process_text(self, text):
        """Process text and check for language switches"""
        if self.check_wake_word_for_hinglish(text):
            self.switch_to_hinglish()
            return True, "hinglish"
        
        if self.check_switch_to_english(text):
            self.switch_to_english()
            return True, "english"
        
        return False, self.current_mode