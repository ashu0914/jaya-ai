"""
JAYA AI - Text-to-Speech Engine
Custom voice with emotion support using Coqui XTTS v2!
"""

import os
import threading
import sounddevice as sd
import soundfile as sf
from config.settings import VOICE_SETTINGS, EMOTIONS, USER_NAME

class TTSEngine:
    def __init__(self):
        self.voice_settings = VOICE_SETTINGS
        self.custom_voice_path = "jaya ai ki voice.wav"
        self.use_custom_voice = os.path.exists(self.custom_voice_path)
        self.xtts_model = None
        self.model_loaded = False
        
        # Accept Coqui terms automatically
        os.environ['COQUI_TOS_AGREED'] = '1'
        
        if self.use_custom_voice:
            print("✅ Custom voice found! Loading XTTS v2...")
            self._load_xtts_model()
        else:
            print("⚠️ Custom voice not found. Using fallback system voice.")
        
        print("✅ TTS Engine ready!")
    
    def _load_xtts_model(self):
        try:
            from TTS.api import TTS
            import torch
            
            print("🔄 Loading XTTS v2 model...")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"   Using device: {device.upper()}")
            
            self.xtts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            self.model_loaded = True
            print("✅ XTTS v2 model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading XTTS: {e}")
            self.model_loaded = False
    
    def _generate_custom_voice(self, text, emotion="neutral", language="en"):
        if not self.model_loaded or not self.xtts_model:
            return False
        
        try:
            config = EMOTIONS.get(emotion, EMOTIONS['neutral'])
            speed = config.get('speed', 1.0)
            
            lang_map = {"english": "en", "hinglish": "hi", "hindi": "hi"}
            lang = lang_map.get(language.lower(), "en")
            
            output_path = "temp_jaya_output.wav"
            
            self.xtts_model.tts_to_file(
                text=text,
                speaker_wav=self.custom_voice_path,
                language=lang,
                file_path=output_path,
                speed=speed
            )
            
            if os.path.exists(output_path):
                data, samplerate = sf.read(output_path)
                sd.play(data, samplerate)
                sd.wait()
                return True
                
        except Exception as e:
            print(f"Custom voice error: {e}")
        
        return False
    
    def _play_with_pyttsx3(self, text, emotion="neutral"):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            female_voice = None
            for voice in voices:
                if any(x in voice.name.lower() for x in ['female', 'woman', 'zira', 'hazel']):
                    female_voice = voice.id
                    break
            if female_voice:
                engine.setProperty('voice', female_voice)
            
            config = EMOTIONS.get(emotion, EMOTIONS['neutral'])
            rate = int(VOICE_SETTINGS['rate'] * config.get('speed', 1.0))
            volume = min(1.0, VOICE_SETTINGS['volume'] * config.get('pitch', 1.0))
            
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            engine.say(config.get('prefix', '') + text)
            engine.runAndWait()
            engine.stop()
            del engine
        except Exception as e:
            print(f"❌ pyttsx3 Error: {e}")
            print(f"📝 Jaya (text): {text}")
    
    def speak(self, text, emotion="neutral", language="english"):
        if not text:
            return
        print(f"🔊 Jaya says: {text}")
        
        if self.use_custom_voice and self.model_loaded:
            success = self._generate_custom_voice(text, emotion, language)
            if success:
                return
            print("⚠️ Custom voice failed, falling back...")
        
        self._play_with_pyttsx3(text, emotion)
    
    def speak_async(self, text, emotion="neutral", language="english"):
        if not text:
            return None
        thread = threading.Thread(target=self.speak, args=(text, emotion, language))
        thread.start()
        return thread
    
    def stop(self):
        try:
            sd.stop()
        except:
            pass
    
    def greet(self, language="english"):
        from config.settings import GREETINGS
        self.speak(GREETINGS.get(language, GREETINGS['english']), emotion="happy", language=language)
    
    def say_goodbye(self, language="english"):
        goodbyes = {
            "english": f"Goodbye {USER_NAME}! Take care!",
            "hinglish": f"Bye {USER_NAME} bhaiya! Khush raho!"
        }
        self.speak(goodbyes.get(language, goodbyes['english']), emotion="loving", language=language)