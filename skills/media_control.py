"""
JAYA AI - Media Control Skills
Play, pause, skip, volume control
"""

import pyautogui
import subprocess
import platform
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class MediaController:
    def __init__(self):
        self.system = platform.system()
        self._setup_volume_control()
    
    def _setup_volume_control(self):
        """Setup volume control interface"""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        except:
            self.volume = None
    
    def play_pause(self):
        """Play or pause media"""
        pyautogui.press('playpause')
        return "Play/Pause toggled"
    
    def next_track(self):
        """Skip to next track"""
        pyautogui.press('nexttrack')
        return "Skipped to next track"
    
    def previous_track(self):
        """Go to previous track"""
        pyautogui.press('prevtrack')
        return "Previous track"
    
    def stop_media(self):
        """Stop media"""
        pyautogui.press('stop')
        return "Media stopped"
    
    def volume_up(self, amount=0.1):
        """Increase volume"""
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_vol = min(1.0, current + amount)
            self.volume.SetMasterVolumeLevelScalar(new_vol, None)
            return f"Volume increased to {int(new_vol * 100)}%"
        else:
            # Fallback using keyboard
            for _ in range(int(amount * 10)):
                pyautogui.press('volumeup')
            return "Volume increased"
    
    def volume_down(self, amount=0.1):
        """Decrease volume"""
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_vol = max(0.0, current - amount)
            self.volume.SetMasterVolumeLevelScalar(new_vol, None)
            return f"Volume decreased to {int(new_vol * 100)}%"
        else:
            for _ in range(int(amount * 10)):
                pyautogui.press('volumedown')
            return "Volume decreased"
    
    def set_volume(self, level):
        """Set volume to specific level (0-100)"""
        level = max(0, min(100, level))
        if self.volume:
            self.volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"Volume set to {level}%"
        return "Volume control not available"
    
    def mute(self):
        """Mute audio"""
        if self.volume:
            self.volume.SetMute(1, None)
            return "Muted"
        pyautogui.press('volumemute')
        return "Muted"
    
    def unmute(self):
        """Unmute audio"""
        if self.volume:
            self.volume.SetMute(0, None)
            return "Unmuted"
        return "Unmuted"
    
    def play_youtube(self, query):
        """Search and play on YouTube"""
        import webbrowser
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching YouTube for: {query}"
    
    def play_spotify(self, query=None):
        """Open Spotify"""
        import subprocess
        try:
            subprocess.Popen("spotify.exe", shell=True)
            if query:
                return f"Opening Spotify. Search for {query} manually please."
            return "Opening Spotify..."
        except:
            webbrowser.open("https://open.spotify.com")
            return "Opening Spotify web..."