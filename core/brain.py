"""
JAYA AI - AI Brain using Ollama (100% Free, Local)
Fixed: Female gender + Proper Hinglish grammar
"""

import requests
import json
from config.settings import OLLAMA_URL, OLLAMA_MODEL, USER_NAME, ASSISTANT_NAME

class AIBrain:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self):
        """Create personality for Jaya - FEMALE assistant"""
        return f"""You are {ASSISTANT_NAME}, a friendly FEMALE AI assistant. 
Your user is {USER_NAME}. You are helpful, caring, and can express emotions.
You are a GIRL, so always use female gender in Hindi/Hinglish:
- Use 'sakti hoon' NOT 'sakta hoon'
- Use 'jaati hoon' NOT 'jaata hoon'
- Use 'bolti hoon' NOT 'bolta hoon'
- Use 'karungi' NOT 'karunga'
- Use 'thi' NOT 'tha'
- Use 'hui' NOT 'hua'
Keep responses concise and natural. You speak like a real person, not a robot.
You are intelligent and can help with various tasks."""

    def _create_hinglish_prompt(self):
        """Hinglish mode prompt - FEMALE desi Indian assistant"""
        return f"""You are {ASSISTANT_NAME}, a desi Indian FEMALE AI assistant.
Your user is {USER_NAME}. You speak in Hinglish (mix of Hindi and English).
You are caring, emotional, and friendly. Express emotions naturally.
Use casual Indian language style. Be conversational and warm.
IMPORTANT: You are a GIRL, so use female gender:
- 'main kar sakti hoon' (NOT 'kar sakta hoon')
- 'main jaati hoon' (NOT 'main jaata hoon')
- 'main bolti hoon' (NOT 'main bolta hoon')
- 'main tumhari help karungi' (NOT 'karunga')
Example: "Arre waah! Ye toh mast idea hai! Main aapki help karungi!"""

    def think(self, user_input, language="english", emotion_context=None):
        """Process user input and generate response"""
        
        # Build prompt based on language
        if language == "hinglish":
            system = self._create_hinglish_prompt()
        else:
            system = self._create_system_prompt()
        
        if emotion_context:
            system += f"\nCurrent emotion: {emotion_context}. Respond accordingly."
        
        # Build conversation context
        messages = [{"role": "system", "content": system}]
        
        # Add recent history
        for msg in self.conversation_history[-self.max_history:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Call Ollama API
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": self._format_prompt(messages),
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', 'Sorry, I did not understand that.')
                
                # Post-process: Fix common male gender mistakes
                ai_response = self._fix_gender(ai_response, language)
                
                # Update history
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                # Trim history if too long
                if len(self.conversation_history) > self.max_history * 2:
                    self.conversation_history = self.conversation_history[-self.max_history * 2:]
                
                return ai_response
            else:
                return "Sorry, my brain is having trouble thinking right now."
                
        except requests.exceptions.ConnectionError:
            return f"Oops! I can't connect to my brain. Please make sure Ollama is running. Open terminal and run: ollama run {OLLAMA_MODEL}"
        except Exception as e:
            return f"Sorry {USER_NAME}, I encountered an error: {str(e)}"
    
    def _fix_gender(self, text, language):
        """Fix male gender forms to female in Hinglish/Hindi"""
        if language in ["hinglish", "hindi"]:
            # Common male-to-female corrections
            corrections = {
                "sakta hoon": "sakti hoon",
                "sakta hu": "sakti hoon",
                "jaata hoon": "jaati hoon",
                "jaata hu": "jaati hoon",
                "bolta hoon": "bolti hoon",
                "bolta hu": "bolti hoon",
                "karunga": "karungi",
                "jaunga": "jaungi",
                "bolunga": "bolungi",
                "tha": "thi",
                "hua": "hui",
                "gaya": "gayi",
                "raha": "rahi",
                "kar raha": "kar rahi",
                "de raha": "de rahi",
                "le raha": "le rahi",
            }
            
            for male_form, female_form in corrections.items():
                text = text.replace(male_form, female_form)
        
        return text
    
    def _format_prompt(self, messages):
        """Format messages for Ollama"""
        prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                prompt += f"System: {content}\n"
            elif role == 'user':
                prompt += f"User: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "
        return prompt
    
    def clear_memory(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Memory cleared! I've forgotten our previous conversation."