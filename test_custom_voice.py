"""
JAYA AI - Voice Test Script
Run this to check if your custom voice works!
"""

import os

print("="*60)
print("🎙️ JAYA AI - Custom Voice Test")
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
    
    print("🗣️ Test 1: English")
    tts.tts_to_file(text="Hello Ashu! I am Jaya!", speaker_wav=voice_file, language="en", file_path="test_english.wav")
    print("   ✅ Saved: test_english.wav")
    
    print("\n🗣️ Test 2: Hindi")
    tts.tts_to_file(text="Namaste Ashu bhaiya! Main Jaya hoon!", speaker_wav=voice_file, language="hi", file_path="test_hindi.wav")
    print("   ✅ Saved: test_hindi.wav")
    
    print("\n🎉 ALL TESTS PASSED! Listen to the .wav files!")

except Exception as e:
    print(f"\n❌ Error: {e}")