"""
JAYA AI - Application Control
FIXED: Chrome, YouTube, Google search + Web fallback
"""

import os
import subprocess
import webbrowser
from config.settings import APP_PATHS
import getpass

class AppController:
    def __init__(self):
        self.running_apps = []
        
        # Common Chrome paths
        self.chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe",
        ]
        
        # Common Edge paths
        self.edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
    
    def _find_chrome(self):
        """Find Chrome executable"""
        for path in self.chrome_paths:
            if "{}" in path:
                path = path.format(getpass.getuser())
            if os.path.exists(path):
                return path
        return None
    
    def _find_edge(self):
        """Find Edge executable"""
        for path in self.edge_paths:
            if os.path.exists(path):
                return path
        return None
    
    def open_application(self, app_name):
        """Open any application"""
        app_name = app_name.lower().strip()
        
        # Common app mappings
        app_map = {
            "chrome": ["chrome", "google chrome", "browser", "google"],
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
            "youtube": ["youtube", "yt"],  # ✅ Added YouTube
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
            # ✅ YOUTUBE FIX - Open in browser directly
            if actual_app == "youtube":
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube..."
            
            # ✅ CHROME FIX - Find exact path
            elif actual_app in ["chrome", "google chrome", "google"]:
                chrome_path = self._find_chrome()
                if chrome_path:
                    subprocess.Popen(chrome_path)
                    self.running_apps.append(actual_app)
                    return "Opening Google Chrome..."
                else:
                    # Fallback: open Google in default browser
                    webbrowser.open("https://www.google.com")
                    return "Opening Google in default browser..."
            
            # ✅ EDGE FIX
            elif actual_app == "edge":
                edge_path = self._find_edge()
                if edge_path:
                    subprocess.Popen(edge_path)
                    self.running_apps.append(actual_app)
                    return "Opening Microsoft Edge..."
                else:
                    webbrowser.open("https://www.google.com")
                    return "Opening browser..."
            
            # SPOTIFY FIX
            elif actual_app == "spotify":
                try:
                    spotify_path = r"C:\Users\{}\AppData\Local\Microsoft\WindowsApps\Spotify.exe"
                    spotify_path = spotify_path.format(getpass.getuser())
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
            
            elif actual_app == "firefox":
                os.startfile("firefox")
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
            # ✅ FINAL FALLBACK - Open in browser
            if actual_app in ["chrome", "google chrome", "google", "youtube"]:
                webbrowser.open("https://www.google.com")
                return f"Opening in browser..."
            return f"Sorry, I couldn't open {app_name}. Error: {str(e)}"
    
    def close_application(self, app_name):
        """Close an application"""
        app_name = app_name.lower().strip()
        
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
        if not site.startswith(("http://", "https://")):
            if "." not in site:
                # It's a search query
                webbrowser.open(f"https://www.google.com/search?q={site}")
                return f"Searching for {site}..."
            site = f"https://{site}"
        
        webbrowser.open(site)
        return f"Opening {site}..."