"""
JAYA AI - Windows Startup Integration
Auto-start Jaya when PC boots
"""

import os
import sys
import winreg as reg
import getpass

class StartupManager:
    def __init__(self):
        self.key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        self.app_name = "JayaAI"
    
    def add_to_startup(self, script_path=None):
        """Add Jaya to Windows startup"""
        if script_path is None:
            # Get the main.py path
            script_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "main.py"
            ))
        
        # Create batch file to run Jaya
        python_path = sys.executable
        batch_path = os.path.join(
            os.path.dirname(__file__), "start_jaya.bat"
        )
        
        with open(batch_path, 'w') as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{os.path.dirname(script_path)}"\n')
            f.write(f'"{python_path}" "{script_path}"\n')
        
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.key_path, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, self.app_name, 0, reg.REG_SZ, batch_path)
            reg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error adding to startup: {e}")
            return False
    
    def remove_from_startup(self):
        """Remove Jaya from startup"""
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.key_path, 0, reg.KEY_SET_VALUE)
            reg.DeleteValue(key, self.app_name)
            reg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error removing from startup: {e}")
            return False
    
    def is_in_startup(self):
        """Check if Jaya is in startup"""
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.key_path, 0, reg.KEY_READ)
            value, _ = reg.QueryValueEx(key, self.app_name)
            reg.CloseKey(key)
            return True
        except:
            return False