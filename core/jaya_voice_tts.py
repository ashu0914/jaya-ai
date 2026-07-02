"""
JAYA AI - Custom Voice TTS
"""

import os
from openvoice import OpenVoice
import sounddevice as sd
import soundfile as sf

class JayaVoiceTTS:
    def __init__(self):
        print("Loading Jaya voice...")
        self.voice = OpenVoice()
        self.speaker_wav = "jaya ai ki voice.wav"
        
        if not os.path.exists(self.speaker_wav):
            raise FileNotFoundError("Voice sample not found!")
        
        print("Jaya voice loaded!")
    
    def speak(self, text, emotion="neutral"):
        if not text:
            return
        
        print(f"Jaya: {text}")
        
        try:
            self.voice.clone(
                text=text,
                reference_speaker=self.speaker_wav,
                output_file="temp_output.wav"
            )
            
            data, samplerate = sf.read("temp_output.wav")
            sd.play(data, samplerate)
            sd.wait()
            
        except Exception as e:
            print(f"Error: {e}")