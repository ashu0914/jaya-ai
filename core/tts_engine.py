"""
JAYA AI - Text-to-Speech Engine
Female voice with emotion support!
"""

import pyttsx3
import threading
from config.settings import VOICE_SETTINGS, EMOTIONS, USER_NAME

class TTSEngine:
    def __init__(self):
        self.voice_settings = self._get_voice_settings()
        print("✅ TTS Engine ready!")
    
    def _get_voice_settings(self):
        """Get voice settings without initializing engine"""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            print("Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name}")
            
            female_voice = None
            for voice in voices:
                name = voice.name.lower()
                if any(x in name for x in ['female', 'woman', 'girl', 'zira', 'hazel', 'susan', 'linda', 'tina', 'eva']):
                    female_voice = voice.id
                    print(f"Selected female voice: {voice.name}")
                    break
            
            if not female_voice and voices:
                female_voice = voices[0].id
                print(f"Fallback voice: {voices[0].name}")
            
            engine.stop()
            del engine
            
            return {
                'voice': female_voice,
                'rate': VOICE_SETTINGS['rate'],
                'volume': VOICE_SETTINGS['volume']
            }
        except Exception as e:
            print(f"❌ TTS Init Error: {e}")
            return None
    
    def speak(self, text, emotion="neutral"):
        """Speak text - blocking"""
        if not text:
            return
        
        print(f"🔊 Jaya says: {text}")
        
        try:
            # Fresh engine instance
            engine = pyttsx3.init()
            
            if self.voice_settings and self.voice_settings['voice']:
                engine.setProperty('voice', self.voice_settings['voice'])
            
            # Emotion settings
            config = EMOTIONS.get(emotion, EMOTIONS['neutral'])
            prefix = config.get('prefix', '')
            full_text = prefix + text
            
            rate = int(VOICE_SETTINGS['rate'] * config.get('speed', 1.0))
            volume = min(1.0, VOICE_SETTINGS['volume'] * config.get('pitch', 1.0))
            
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            engine.say(full_text)
            engine.runAndWait()
            
            engine.stop()
            del engine
            
        except Exception as e:
            print(f"❌ Speak Error: {e}")
            print(f"📝 Jaya (text): {text}")
    
    def speak_async(self, text, emotion="neutral"):
        """Speak without blocking"""
        if not text:
            return None
        thread = threading.Thread(target=self.speak, args=(text, emotion))
        thread.start()
        return thread
    
    def stop(self):
        pass
    
    def greet(self, language="english"):
        from config.settings import GREETINGS
        greeting = GREETINGS.get(language, GREETINGS['english'])
        self.speak(greeting, emotion="happy")
    
    def say_goodbye(self, language="english"):
        goodbyes = {
            "english": f"Goodbye {USER_NAME}! Take care!",
            "hinglish": f"Bye {USER_NAME} bhaiya! Khush raho!"
        }
        self.speak(goodbyes.get(language, goodbyes['english']), emotion="loving")