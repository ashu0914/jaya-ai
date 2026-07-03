"""
JAYA AI - Voice Test + Cache Pre-generation Script
Run this to:
1. Check if custom voice works
2. Pre-generate common phrases for INSTANT playback!
"""

import os

print("="*60)
print("🎙️ JAYA AI - Custom Voice Test + Cache Generator")
print("="*60)

# Check 1: Voice file exists?
voice_file = "jaya ai ki voice.wav"
if os.path.exists(voice_file):
    print(f"✅ Voice file found: {voice_file}")
else:
    print(f"❌ Voice file NOT found: {voice_file}")
    print("   Make sure it's in the same folder as this script!")
    exit()

# Check 2: Coqui TTS installed?
try:
    from TTS.api import TTS
    print("✅ Coqui TTS installed")
except ImportError:
    print("❌ Coqui TTS NOT installed")
    print("   Run: pip install coqui-tts")
    exit()

# Check 3: PyTorch
try:
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"✅ PyTorch loaded | Device: {device.upper()}")
except ImportError:
    print("❌ PyTorch NOT installed")
    exit()

# Check 4: Terms accepted
if os.environ.get('COQUI_TOS_AGREED') == '1':
    print("✅ Coqui terms accepted")
else:
    print("⚠️ Run: setx COQUI_TOS_AGREED 1, then RESTART terminal")

print("\n" + "="*60)
print("🔄 Loading XTTS v2 model... (First time: ~2GB download)")
print("="*60)

try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    print("✅ Model loaded!\n")
    
    # Test 1: English
    print("🗣️ Test 1: English")
    tts.tts_to_file(text="Hello Ashu! I am Jaya!", speaker_wav=voice_file, language="en", file_path="test_english.wav")
    print("   ✅ Saved: test_english.wav")
    
    # Test 2: Hindi
    print("\n🗣️ Test 2: Hindi")
    tts.tts_to_file(text="Namaste Ashu! Main Jaya hoon!", speaker_wav=voice_file, language="hi", file_path="test_hindi.wav")
    print("   ✅ Saved: test_hindi.wav")
    
    # ============================================
    # 🎉 PRE-GENERATE CACHE FOR INSTANT PLAYBACK!
    # ============================================
    print("\n" + "="*60)
    print("🎙️ Pre-generating cached phrases for INSTANT playback...")
    print("="*60)
    
    # Create cache folder
    os.makedirs("cache", exist_ok=True)
    
    # Common phrases to pre-generate (NO "bhaiya"!)
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
        
        # Common
        "listening_en": "I am listening...",
        "listening_hi": "Main sun rahi hoon...",
        "thinking_en": "Let me think...",
        "thinking_hi": "Mujhe sochna do...",
    }
    
    # Generate all phrases
    for name, text in phrases.items():
        lang = "en" if "_en" in name else "hi"
        output_path = f"cache/{name}.wav"
        
        print(f"   🎙️ Generating: {name}...")
        tts.tts_to_file(
            text=text,
            speaker_wav=voice_file,
            language=lang,
            file_path=output_path
        )
        print(f"   ✅ Saved: {output_path}")
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED + CACHE GENERATED!")
    print("="*60)
    print("\n📁 Generated files:")
    print("   • test_english.wav")
    print("   • test_hindi.wav")
    print("   • cache/ folder with 20+ pre-generated phrases!")
    print("\n🚀 Now Jaya will speak INSTANTLY using cached phrases!")
    print("   (No more waiting for voice generation!)")

except Exception as e:
    print(f"\n❌ Error: {e}")