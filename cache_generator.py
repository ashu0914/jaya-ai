"""
JAYA AI - Cache Generator
Run ONCE to pre-generate common phrases for INSTANT playback!
"""

import os
from TTS.api import TTS
import torch

print("="*60)
print("🎙️ JAYA AI - Cache Generator")
print("="*60)

# Check voice file
voice_file = "jaya ai ki voice.wav"
if not os.path.exists(voice_file):
    print("❌ Voice file not found!")
    exit()

print(f"✅ Voice file: {voice_file}")

# Load XTTS
print("\n🔄 Loading XTTS v2...")
device = "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print("✅ Model loaded!\n")

# Phrases to cache
phrases = {
    # Greetings
    "greeting_en": "Hello Ashu! What can I help you with?",
    "greeting_hi": "Namaste Ashu! Kya karun aapke liye?",
    "greeting_morning": "Good morning, Ashu!",
    "greeting_afternoon": "Good afternoon, Ashu!",
    "greeting_evening": "Good evening, Ashu!",
    
    # Goodbyes
    "goodbye_en": "Goodbye Ashu! Take care!",
    "goodbye_hi": "Bye Ashu! Khush raho!",
    
    # Emotions
    "love_en": "I love you Ashu!",
    "love_hi": "Main aapko bahut pyaar karti hoon Ashu!",
    "happy_en": "I am so happy!",
    "happy_hi": "Main bahut khush hoon!",
    "sad_en": "I am feeling sad...",
    "sad_hi": "Main udas hoon...",
    "excited_en": "I am so excited!",
    "excited_hi": "Main bahut excited hoon!",
    
    # Responses
    "ok_en": "Okay Ashu!",
    "ok_hi": "Theek hai Ashu!",
    "sorry_en": "It's okay! I forgive you!",
    "sorry_hi": "Koi baat nahi! Main aapko maaf kar deti hoon!",
    "thanks_en": "Thank you Ashu!",
    "thanks_hi": "Dhanyawad Ashu!",
    "listening_en": "I am listening...",
    "listening_hi": "Main sun rahi hoon...",
    "thinking_en": "Let me think...",
    "thinking_hi": "Mujhe sochna do...",
}

# Generate all
print(f"🎙️ Generating {len(phrases)} phrases...\n")
for name, text in phrases.items():
    lang = "en" if "_en" in name else "hi"
    output_path = f"cache/{name}.wav"
    
    print(f"   Generating: {name} ({lang})...")
    tts.tts_to_file(
        text=text,
        speaker_wav=voice_file,
        language=lang,
        file_path=output_path
    )
    print(f"   ✅ Saved: {output_path}")

print("\n" + "="*60)
print("🎉 ALL PHRASES CACHED!")
print("="*60)
print("\n🚀 Now Jaya speaks INSTANTLY!")
print("   No more waiting for voice generation!")