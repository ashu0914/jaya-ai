"""
JAYA AI - Wake Word Detection
Uses sounddevice instead of PyAudio
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
from config.settings import WAKE_WORDS

class WakeWordDetector:
    def __init__(self):
        self.wake_words = WAKE_WORDS
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
    
    def record_audio(self, duration=3):
        """Record audio using sounddevice"""
        print("👂 Listening for wake word...")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        return temp_file.name
    
    def listen_for_wake_word(self):
        """Listen for wake word"""
        try:
            audio_file = self.record_audio(duration=3)
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            os.unlink(audio_file)
            
            try:
                text = self.recognizer.recognize_google(audio, language="en-IN").lower()
                print(f"Heard: {text}")
                
                for wake in self.wake_words:
                    if wake in text:
                        return True, text
                return False, text
            except sr.UnknownValueError:
                return False, ""
            except sr.RequestError:
                return False, ""
                
        except Exception as e:
            print(f"Error: {e}")
            return False, ""
    
    def is_wake_word(self, text):
        """Check if text contains wake word"""
        text = text.lower()
        return any(wake in text for wake in self.wake_words)