"""
JAYA AI - Application Control
"""

import os
import subprocess
import webbrowser
from config.settings import APP_PATHS
import getpass

class AppController:
    def __init__(self):
        self.running_apps = []
    
    def open_application(self, app_name):
        """Open any application"""
        app_name = app_name.lower().strip()
        
        # Common app mappings
        app_map = {
            "chrome": ["chrome", "google chrome", "browser"],
            "firefox": ["firefox", "mozilla"],
            "edge": ["edge", "microsoft edge"],
            "notepad": ["notepad", "text editor", "note pad"],
            "calculator": ["calculator", "calc"],
            "spotify": ["spotify", "music"],
            "vlc": ["vlc", "media player", "video player"],
            "explorer": ["explorer", "file explorer", "files"],
            "cmd": ["cmd", "command prompt", "terminal"],
            "powershell": ["powershell", "power shell"],
            "task manager": ["task manager", "taskmanager"],
            "settings": ["settings", "control panel"],
            "paint": ["paint", "mspaint"],
            "word": ["word", "msword", "microsoft word"],
            "excel": ["excel", "msexcel", "microsoft excel"],
            "powerpoint": ["powerpoint", "mspowerpoint", "ppt"],
        }
        
        # Find actual app name
        actual_app = None
        for key, aliases in app_map.items():
            if app_name in aliases or app_name == key:
                actual_app = key
                break
        
        if not actual_app:
            actual_app = app_name
        
        # Try to open
        try:
            # SPOTIFY FIX - Exact path se open karo
            if actual_app == "spotify":
                try:
                    # Exact Spotify path
                    spotify_path = r"C:\Users\jindr\AppData\Local\Microsoft\WindowsApps\Spotify.exe"
                    if os.path.exists(spotify_path):
                        subprocess.Popen(spotify_path)
                        self.running_apps.append(actual_app)
                        return "Opening Spotify..."
                    else:
                        os.startfile("spotify")
                        self.running_apps.append(actual_app)
                        return "Opening Spotify..."
                except:
                    webbrowser.open("https://open.spotify.com")
                    return "Opening Spotify web..."
            
            elif actual_app in ["chrome", "google chrome"]:
                os.startfile("chrome")
            elif actual_app == "firefox":
                os.startfile("firefox")
            elif actual_app == "edge":
                os.startfile("msedge")
            elif actual_app == "notepad":
                os.startfile("notepad")
            elif actual_app == "calculator":
                os.startfile("calc")
            elif actual_app == "explorer":
                os.startfile("explorer")
            elif actual_app == "cmd":
                os.startfile("cmd")
            elif actual_app == "task manager":
                os.startfile("taskmgr")
            elif actual_app == "settings":
                os.startfile("ms-settings:")
            elif actual_app == "paint":
                os.startfile("mspaint")
            elif actual_app in APP_PATHS:
                path = APP_PATHS[actual_app]
                if "{}" in path:
                    path = path.format(getpass.getuser())
                subprocess.Popen(path)
            else:
                # Try direct execution
                subprocess.Popen(actual_app, shell=True)
            
            self.running_apps.append(actual_app)
            return f"Opening {actual_app}..."
            
        except Exception as e:
            # Fallback for Spotify
            if actual_app == "spotify":
                webbrowser.open("https://open.spotify.com")
                return "Opening Spotify web..."
            return f"Sorry, I couldn't open {app_name}. Error: {str(e)}"
    
    def close_application(self, app_name):
        """Close an application"""
        app_name = app_name.lower().strip()
        
        # Process name mappings
        process_map = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "notepad": "notepad.exe",
            "spotify": "spotify.exe",
            "vlc": "vlc.exe",
            "explorer": "explorer.exe",
        }
        
        process_name = process_map.get(app_name, f"{app_name}.exe")
        
        try:
            subprocess.run(f"taskkill /f /im {process_name}", shell=True, capture_output=True)
            if app_name in self.running_apps:
                self.running_apps.remove(app_name)
            return f"Closed {app_name}"
        except Exception as e:
            return f"Couldn't close {app_name}: {str(e)}"
    
    def open_website(self, site):
        """Open a website"""
        site = site.lower().strip()
        
        # Remove common prefixes
        site = site.replace("open ", "").replace("go to ", "").replace("visit ", "")
        
        # Add https if not present
        if not site.startswith(('http://', 'https://')):
            if '.' not in site:
                # It's a search query
                webbrowser.open(f"https://www.google.com/search?q={site}")
                return f"Searching for {site}..."
            site = f"https://{site}"
        
        webbrowser.open(site)
        return f"Opening {site}..."