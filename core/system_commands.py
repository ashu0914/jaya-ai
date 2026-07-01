"""
JAYA AI - System Commands Handler
"""

import os
import subprocess
import platform
import webbrowser
import pyautogui
import time

class SystemCommands:
    def __init__(self):
        self.system = platform.system()
    
    def open_app(self, app_name):
        """Open an application"""
        from config.settings import APP_PATHS
        
        # Try to find app in configured paths
        app_path = APP_PATHS.get(app_name.lower())
        
        if app_path:
            try:
                if "{}" in app_path:
                    # Need to format with username
                    import getpass
                    app_path = app_path.format(getpass.getuser())
                
                subprocess.Popen(app_path, shell=True)
                return f"Opening {app_name}..."
            except Exception as e:
                return f"Sorry, couldn't open {app_name}: {str(e)}"
        
        # Try to open using system command
        try:
            if self.system == "Windows":
                os.startfile(app_name)
            else:
                subprocess.Popen([app_name])
            return f"Opening {app_name}..."
        except:
            return f"Sorry, I couldn't find {app_name}. Can you check the app name?"
    
    def close_app(self, app_name):
        """Close an application"""
        try:
            if self.system == "Windows":
                subprocess.run(f"taskkill /f /im {app_name}.exe", shell=True, capture_output=True)
            else:
                subprocess.run(f"pkill -f {app_name}", shell=True, capture_output=True)
            return f"Closing {app_name}..."
        except Exception as e:
            return f"Couldn't close {app_name}: {str(e)}"
    
    def search_google(self, query):
        """Search on Google"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching Google for: {query}"
    
    def open_website(self, url):
        """Open a website"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        return f"Opening {url}..."
    
    def type_text(self, text):
        """Type text using keyboard"""
        pyautogui.typewrite(text, interval=0.01)
        return f"Typed: {text}"
    
    def press_key(self, key):
        """Press a keyboard key"""
        pyautogui.press(key)
        return f"Pressed {key}"
    
    def take_screenshot(self):
        """Take a screenshot"""
        screenshot = pyautogui.screenshot()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        return f"Screenshot saved as {filename}"
    
    def get_system_info(self):
        """Get system information"""
        info = {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        return f"System: {info['platform']} {info['release']}, {info['machine']}"
    