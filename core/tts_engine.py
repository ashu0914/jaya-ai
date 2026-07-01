"""
JAYA AI - Text-to-Speech Engine
Female voice with emotion support!
"""

import pyttsx3
import threading
from config.settings import VOICE_SETTINGS, EMOTIONS, USER_NAME
from core.emotions import EmotionEngine

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.emotion_engine = EmotionEngine()
        self.speaking = False
        self._setup_voice()
    
    def _setup_voice(self):
        """Configure female voice"""
        voices = self.engine.getProperty('voices')
        
        # Print all voices for debugging
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")
        
        # Try to find a female voice
        female_voice = None
        for i, voice in enumerate(voices):
            voice_name = voice.name.lower()
            if any(keyword in voice_name for keyword in ['female', 'woman', 'girl', 'zira', 'eva', 'tina', 'hazel', 'susan', 'linda']):
                female_voice = voice.id
                print(f"Selected female voice: {voice.name}")
                break
        
        # Fallback to first voice if no female found
        if not female_voice and voices:
            female_voice = voices[0].id
            print(f"Fallback voice: {voices[0].name}")
        
        if female_voice:
            self.engine.setProperty('voice', female_voice)
        
        self.engine.setProperty('rate', VOICE_SETTINGS['rate'])
        self.engine.setProperty('volume', VOICE_SETTINGS['volume'])
    
    def set_emotion_voice(self, emotion):
        """Adjust voice properties based on emotion"""
        config = EMOTIONS.get(emotion, EMOTIONS['neutral'])
        
        base_rate = VOICE_SETTINGS['rate']
        base_volume = VOICE_SETTINGS['volume']
        
        # Adjust rate based on emotion
        new_rate = int(base_rate * config['speed'])
        self.engine.setProperty('rate', new_rate)
        
        # Adjust volume slightly
        new_volume = min(1.0, base_volume * config['pitch'])
        self.engine.setProperty('volume', new_volume)
    
    def speak(self, text, emotion="neutral"):
        """Speak text with emotion"""
        if not text:
            return
            
        self.speaking = True
        
        # Get emotional prefix
        self.emotion_engine.set_emotion(emotion)
        prefix = self.emotion_engine.get_emotional_prefix()
        full_text = prefix + text
        
        print(f"🔊 Jaya says: {full_text}")
        
        try:
            # Adjust voice for emotion
            self.set_emotion_voice(emotion)
            
            # Speak
            self.engine.say(full_text)
            self.engine.runAndWait()
            
            # Reset to neutral
            self.set_emotion_voice("neutral")
        except Exception as e:
            print(f"❌ TTS Error: {e}")
        
        self.speaking = False
    
    def speak_async(self, text, emotion="neutral"):
        """Speak without blocking"""
        if not text:
            return None
        thread = threading.Thread(target=self.speak, args=(text, emotion))
        thread.start()
        return thread
    
    def stop(self):
        """Stop speaking"""
        try:
            self.engine.stop()
        except:
            pass
        self.speaking = False
    
    def greet(self, language="english"):
        """Greeting message"""
        from config.settings import GREETINGS
        greeting = GREETINGS.get(language, GREETINGS['english'])
        self.speak(greeting, emotion="happy")
    
    def say_goodbye(self, language="english"):
        """Goodbye message"""
        goodbyes = {
            "english": f"Goodbye {USER_NAME}! Take care!",
            "hinglish": f"Bye {USER_NAME} bhaiya! Khush raho!"
        }
        self.speak(goodbyes.get(language, goodbyes['english']), emotion="loving")