"""
JAYA AI - Speech Recognition Engine
Uses sounddevice instead of PyAudio (Python 3.12 compatible!)
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        self.duration = 5

    def record_audio(self, duration=None):
        if duration is None:
            duration = self.duration
        print("🎤 Listening... (Speak now)")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
        print("✅ Recording complete!")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        return temp_file.name

    def listen(self, timeout=5):
        try:
            audio_file = self.record_audio(duration=timeout)
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            os.unlink(audio_file)
            return audio
        except Exception as e:
            print(f"❌ Error recording: {e}")
            return None

    def recognize_google(self, audio, language="en-US"):
        if audio is None:
            return None
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Google API error: {e}")
            return None

    def listen_and_recognize(self):
        audio = self.listen()
        if audio:
            return self.recognize_google(audio, language="en-IN")
        return None