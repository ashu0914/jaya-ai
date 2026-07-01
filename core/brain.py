"""
JAYA AI - AI Brain using Ollama (100% Free, Local)
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
        """Create personality for Jaya"""
        return f"""You are {ASSISTANT_NAME}, a friendly female AI assistant. 
Your user is {USER_NAME}. You are helpful, caring, and can express emotions.
You can be happy, sad, angry, excited, or hurt based on the conversation.
Keep responses concise and natural. You speak like a real person, not a robot.
You are intelligent and can help with various tasks."""

    def _create_hinglish_prompt(self):
        """Hinglish mode prompt"""
        return f"""You are {ASSISTANT_NAME}, a desi Indian female AI assistant.
Your user is {USER_NAME}. You speak in Hinglish (mix of Hindi and English).
You are caring, emotional, and friendly. Express emotions naturally.
Use casual Indian language style. Be conversational and warm.
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