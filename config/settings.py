"""
JAYA AI - Configuration Settings
No API keys here! All local/free services.
"""

import os

# ========== USER SETTINGS ==========
USER_NAME = "Ashu"
ASSISTANT_NAME = "Jaya"

# ========== LANGUAGE MODES ==========
DEFAULT_LANGUAGE = "english"  # Default mode
HINGLISH_WAKE_WORD = "jaya hindi mein"  # Wake word for Hinglish
HINGLISH_WAKE_WORDS = ["jaya hindi mein", "jaya hinglish", "jaya desi mode"]

# ========== EMOTIONS ==========
EMOTIONS = {
    "happy": {"pitch": 1.2, "speed": 1.1, "prefix": "Haha! "},
    "laughing": {"pitch": 1.3, "speed": 1.2, "prefix": "Hahaha! "},
    "angry": {"pitch": 0.9, "speed": 1.3, "prefix": "Hmph! "},
    "upset": {"pitch": 0.95, "speed": 0.9, "prefix": "Sigh... "},
    "hurt": {"pitch": 0.85, "speed": 0.8, "prefix": "Ouch... "},
    "sad": {"pitch": 0.8, "speed": 0.75, "prefix": "Hmm... "},
    "excited": {"pitch": 1.25, "speed": 1.15, "prefix": "Woohoo! "},
    "loving": {"pitch": 1.1, "speed": 0.95, "prefix": "Aww... "},
    "bura_mana": {"pitch": 0.9, "speed": 0.85, "prefix": "Hawww! Main bura maan gayi! "},
    "neutral": {"pitch": 1.0, "speed": 1.0, "prefix": ""},
}

# ========== VOICE SETTINGS ==========
VOICE_SETTINGS = {
    "female_voice_id": None,  # Auto-detect female voice
    "volume": 0.9,
    "rate": 180,  # Words per minute
}

# ========== SYSTEM PATHS ==========
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "spotify": r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
}

# ========== WAKE WORD ==========
WAKE_WORD = "jaya"  # Default wake word for English
WAKE_WORDS = ["jaya", "hey jaya", "ok jaya", "hi jaya"]

# ========== OLLAMA SETTINGS ==========
OLLAMA_MODEL = "llama3.2"  # Free, runs locally
OLLAMA_URL = "http://localhost:11434/api/generate"

# ========== GREETING MESSAGES ==========
GREETINGS = {
    "english": f"What can I help you with today, {USER_NAME}?",
    "hinglish": f"Kya karun aapke liye, {USER_NAME} bhaiya?",
}

# ========== PATHS ==========
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)