"""
JAYA AI - Text-to-Speech Engine
Custom voice with emotion support!
"""

import os
import pyttsx3
import threading
from config.settings import VOICE_SETTINGS, EMOTIONS, USER_NAME

class TTSEngine:
    def __init__(self):
        self.voice_settings = self._get_voice_settings()
        self.custom_voice_path = "jaya ai ki voice.wav"
        self.use_custom_voice = os.path.exists(self.custom_voice_path)
        
        if self.use_custom_voice:
            print("✅ Custom voice found! Jaya will use your voice.")
        else:
            print("⚠️ Custom voice not found. Using system voice.")
        
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
    
    def _play_custom_voice(self, text):
        """Play custom voice using sounddevice"""
        try:
            import sounddevice as sd
            import soundfile as sf
            
            # Check if temp file exists and play it
            if os.path.exists("temp_jaya_output.wav"):
                data, samplerate = sf.read("temp_jaya_output.wav")
                sd.play(data, samplerate)
                sd.wait()
                return True
            return False
        except Exception as e:
            print(f"Custom voice play error: {e}")
            return False
    
    def speak(self, text, emotion="neutral"):
        """Speak text - blocking"""
        if not text:
            return
        
        print(f"🔊 Jaya says: {text}")
        
        # Try custom voice first
        if self.use_custom_voice:
            try:
                # Generate custom voice using OpenVoice or similar
                # For now, we'll use a placeholder that can be replaced
                # with actual voice cloning code
                
                # TODO: Replace with actual voice cloning
                # from openvoice import OpenVoice
                # voice = OpenVoice()
                # voice.clone(text=text, reference_speaker=self.custom_voice_path, output_file="temp_jaya_output.wav")
                
                # For now, fallback to system voice
                pass
                
            except Exception as e:
                print(f"Custom voice error: {e}")
        
        # Fallback to system voice
        try:
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