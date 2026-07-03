#!/usr/bin/env python3
"""
JAYA AI - Your Personal Female Voice Assistant
Created for Ashu
"""

import sys
import time
import threading
from datetime import datetime

# Core modules
from core.speech_recognition import SpeechRecognizer
from core.tts_engine import TTSEngine
from core.brain import AIBrain
from core.emotions import EmotionEngine
from core.language_mode import LanguageModeManager
from core.wake_word import WakeWordDetector

# Skills
from skills.app_control import AppController
from skills.media_control import MediaController
from skills.web_search import WebSearcher
from core.system_commands import SystemCommands

# Config
from config.settings import USER_NAME, ASSISTANT_NAME, GREETINGS


class JayaAI:
    def __init__(self):
        print("Initializing Jaya AI...")
        self.speech = SpeechRecognizer()
        self.tts = TTSEngine()
        self.brain = AIBrain()
        self.emotions = EmotionEngine()
        self.language = LanguageModeManager()
        self.wake = WakeWordDetector()
        self.apps = AppController()
        self.media = MediaController()
        self.web = WebSearcher()
        self.system = SystemCommands()
        self.running = True
        self.listening = False
        print("Jaya AI Initialized!")

    def greet_user(self):
        current_lang = self.language.get_current_mode()  # ✅ FIXED
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = f"Good morning, {USER_NAME}!"
        elif 12 <= current_hour < 17:
            greeting = f"Good afternoon, {USER_NAME}!"
        elif 17 <= current_hour < 22:
            greeting = f"Good evening, {USER_NAME}!"
        else:
            greeting = f"Hello, {USER_NAME}! Working late?"
        main_greeting = GREETINGS.get(current_lang, GREETINGS.get("english"))  # ✅ FIXED
        self.tts.speak(f"{greeting} {main_greeting}", emotion="happy", language=current_lang)

    def process_command(self, command):
        command = command.lower().strip()
        current_lang = self.language.get_current_mode()
        print(f"Processing: {command} | Language: {current_lang}")
        
        switched, new_lang = self.language.process_text(command)
        if switched:
            if new_lang == "hinglish":
                self.tts.speak("Hinglish mode activated!", emotion="excited", language=current_lang)
            else:
                self.tts.speak("English mode activated!", emotion="happy", language=current_lang)
            return
        
        if any(word in command for word in ["bye", "goodbye", "exit", "quit", "band karo", "stop"]):
            self.tts.speak(f"Goodbye {USER_NAME}!", emotion="loving", language=current_lang)
            self.running = False
            return
        
        detected_emotion = self.emotions.detect_emotion_from_text(command)
        if detected_emotion != "neutral":
            self.emotions.set_emotion(detected_emotion)
        
        # App Control
        if any(word in command for word in ["open", "start", "launch", "kholo"]):
            app_name = command.replace("open ", "").replace("start ", "").replace("launch ", "").replace("kholo ", "").strip()
            result = self.apps.open_application(app_name)
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        
        if any(word in command for word in ["close", "stop", "band karo", "quit"]):
            app_name = command.replace("close ", "").replace("stop ", "").replace("band karo ", "").strip()
            result = self.apps.close_application(app_name)
            self.tts.speak(result, emotion="neutral", language=current_lang)
            return
        
        # Web Search
        if any(word in command for word in ["search google", "google search", "google pe search", "search for"]):
            query = command.split("search", 1)[-1].split("for", 1)[-1].strip()
            result = self.web.search_google(query)
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        
        if any(word in command for word in ["search youtube", "youtube search", "youtube pe"]):
            query = command.split("youtube", 1)[-1].replace("search", "").strip()
            result = self.web.search_youtube(query)
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        
        # SONG SEARCH
        if any(word in command for word in ["search song", "song search", "gaana search", "play song", "gana bajao", "song sunao"]) or "song" in command:
            song_name = command
            for remove_word in ["search song", "song search", "gaana search", "play song", "gana bajao", "song sunao", "jaya", "search", "play"]:
                song_name = song_name.replace(remove_word, "").strip()
            
            if song_name:
                import webbrowser
                search_url = f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}"
                webbrowser.open(search_url)
                reply = f"Searching Spotify for {song_name}!"
                print(f"🔊 Jaya says: {reply}")
                self.tts.speak_async(reply, "excited", language=current_lang)
            else:
                reply = "Which song should I search?"
                print(f"🔊 Jaya says: {reply}")
                self.tts.speak_async(reply, "happy", language=current_lang)
            return
        
        # Media Control
        if any(word in command for word in ["play", "pause", "resume"]):
            result = self.media.play_pause()
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        
        if any(word in command for word in ["next", "skip", "agla", "next song"]):
            result = self.media.next_track()
            self.tts.speak("Skipping to next track!", emotion="excited", language=current_lang)
            return
        
        if any(word in command for word in ["previous", "back", "pehla", "last song"]):
            result = self.media.previous_track()
            self.tts.speak("Going back!", emotion="neutral", language=current_lang)
            return
        
        # Volume Control
        if "volume up" in command or "volume badhao" in command or "awaz badhao" in command:
            result = self.media.volume_up(0.1)
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        
        if "volume down" in command or "volume kam karo" in command or "awaz kam karo" in command:
            result = self.media.volume_down(0.1)
            self.tts.speak(result, emotion="neutral", language=current_lang)
            return
        if "mute" in command or "silent" in command:
            result = self.media.mute()
            self.tts.speak("Muted!", emotion="neutral", language=current_lang)
            return
        if "unmute" in command:
            result = self.media.unmute()
            self.tts.speak("Unmuted!", emotion="happy", language=current_lang)
            return
        # System Commands
        if "screenshot" in command or "screen shot" in command:
            result = self.system.take_screenshot()
            self.tts.speak(result, emotion="happy", language=current_lang)
            return
        # Emotions
        if any(word in command for word in ["how are you", "kya haal hai", "sab badhiya"]):
            emotion = self.emotions.express_emotion("happy", current_lang)
            self.tts.speak(emotion, emotion="happy", language=current_lang)
            return
        if any(word in command for word in ["i love you", "love you", "pyaar", "i like you"]):
            emotion = self.emotions.express_emotion("loving", current_lang)
            self.tts.speak(emotion, emotion="loving", language=current_lang)
            return
        if any(word in command for word in ["sorry", "maaf karo", "galti ho gayi"]):
            emotion = self.emotions.express_emotion("happy", current_lang)
            self.tts.speak("It's okay! I forgive you!", emotion="happy", language=current_lang)
            return
        if "bura maan" in command or "hurt" in command:
            emotion = self.emotions.express_emotion("bura_mana", current_lang)
            self.tts.speak(emotion, emotion="bura_mana", language=current_lang)
            return
        # AI Brain Response
        emotion_context = self.emotions.current_emotion
        response = self.brain.think(command, language=current_lang, emotion_context=emotion_context)
        print(f"DEBUG: Response = {response}")
        self.tts.speak(response, emotion=emotion_context, language=current_lang)
    
    def run(self):
        print(f"\n{'='*50}")
        print(f"JAYA AI is now running!")
        print(f"User: {USER_NAME}")
        print(f"Say 'Jaya' to wake me up!")
        print(f"{'='*50}\n")
        self.greet_user()
        while self.running:
            try:
                print("\nListening...")
                command = self.speech.listen_and_recognize()
                if command:
                    if self.wake.is_wake_word(command) or self.listening:
                        self.listening = True
                        for wake in ["jaya", "hey jaya", "ok jaya", "hi jaya"]:
                            command = command.replace(wake, "").strip()
                        if command:
                            self.process_command(command)
                        self.listening = False
            except KeyboardInterrupt:
                print("\nGoodbye!")
                current_lang = self.language.get_current_mode()  # ✅ FIXED
                self.tts.speak(f"Goodbye {USER_NAME}!", emotion="sad", language=current_lang)
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
        print("Jaya AI stopped.")

def main():
    jaya = JayaAI()
    jaya.run()

if __name__ == "__main__":
    main()