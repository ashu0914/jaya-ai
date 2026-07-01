"""
JAYA AI - Web Search Skills
100% Free - uses DuckDuckGo (no API key needed!)
"""

import webbrowser
import urllib.request
import urllib.parse
import json
import re

class WebSearcher:
    def __init__(self):
        self.search_engines = {
            "google": "https://www.google.com/search?q={}",
            "duckduckgo": "https://duckduckgo.com/?q={}",
            "bing": "https://www.bing.com/search?q={}",
            "youtube": "https://www.youtube.com/results?search_query={}",
        }
    
    def search(self, query, engine="google"):
        """Perform web search"""
        query = urllib.parse.quote(query)
        url = self.search_engines.get(engine, self.search_engines["google"]).format(query)
        webbrowser.open(url)
        return f"Searching {engine} for: {query.replace('+', ' ')}"
    
    def search_google(self, query):
        """Search Google"""
        return self.search(query, "google")
    
    def search_youtube(self, query):
        """Search YouTube"""
        return self.search(query, "youtube")
    
    def search_duckduckgo(self, query):
        """Search DuckDuckGo"""
        return self.search(query, "duckduckgo")
    
    def open_url(self, url):
        """Open any URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        return f"Opening {url}..."
    
    def get_weather(self, city):
        """Get weather info (opens weather website)"""
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}")
        return f"Getting weather for {city}..."
    
    def get_news(self):
        """Open news"""
        webbrowser.open("https://news.google.com")
        return "Opening Google News..."
    
    def get_definition(self, word):
        """Get word definition"""
        webbrowser.open(f"https://www.google.com/search?q=define+{word}")
        return f"Looking up definition of {word}..."