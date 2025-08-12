import os
import requests
import json
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIChatbotService:
    """AI Chatbot service supporting Groq, Ollama, and OpenAI"""
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from environment variables"""
        return {
            'groq_api_key': os.getenv('GROQ_API_KEY'),
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'llama3.2:3b'),
            'max_tokens': int(os.getenv('MAX_TOKENS', 1000)),
            'temperature': float(os.getenv('TEMPERATURE', 0.7))
        }
    
    def _get_fitness_context(self) -> str:
        """Get fitness-specific context for the chatbot"""
        return """
        You are a helpful AI assistant for a fitness club management system. 
        You can help with:
        - Fitness advice and workout recommendations
        - Class scheduling and information
        - Membership questions
        - General fitness club inquiries
        - Health and wellness tips
        
        Always provide helpful, accurate, and safe fitness advice.
        If asked about medical conditions, recommend consulting a healthcare professional.
        """
    
    def chat_with_groq(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Chat using Groq API"""
        try:
            import groq
            import pkg_resources
            
            # Check Groq version for compatibility
            groq_version = pkg_resources.get_distribution("groq").version
            logger.info(f"Using Groq version: {groq_version}")
            
            if not self.config['groq_api_key']:
                return "Error: GROQ_API_KEY not configured"
            
            # For Groq 0.6.0+, we need to handle initialization differently
            # The issue is in the internal httpx client that gets proxies from somewhere
            # Clear any proxy-related environment variables that might cause issues
            original_proxy_vars = {}
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'HTTP_PROXY_USER', 'HTTPS_PROXY_USER']
            
            for var in proxy_vars:
                if var in os.environ:
                    original_proxy_vars[var] = os.environ[var]
                    del os.environ[var]
            
            try:
                # Also clear any httpx-related proxy configurations
                import httpx
                
                # Create a clean httpx client without any proxy configurations
                clean_httpx_client = httpx.Client(
                    proxy=None,
                    verify=True,
                    timeout=30.0
                )
                
                # Initialize Groq client with the clean httpx client
                client = groq.Groq(
                    api_key=self.config['groq_api_key'],
                    http_client=clean_httpx_client
                )
                
                # Prepare conversation
                messages = [{"role": "system", "content": self._get_fitness_context()}]
                
                if conversation_history:
                    messages.extend(conversation_history)
                
                messages.append({"role": "user", "content": message})
                
                # Create chat completion with proper parameters
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Updated model name
                    messages=messages,
                    max_tokens=self.config['max_tokens'],
                    temperature=self.config['temperature']
                )
                
                return response.choices[0].message.content
                
            finally:
                # Restore original proxy environment variables
                for var, value in original_proxy_vars.items():
                    os.environ[var] = value
            
        except ImportError as e:
            logger.error(f"Groq library not available: {str(e)}")
            return "Error: Groq library not installed. Please run: pip install groq"
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return f"Sorry, I encountered an error with Groq: {str(e)}"
    
    def chat_with_ollama(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Chat using local Ollama API"""
        try:
            # Prepare conversation
            messages = [{"role": "system", "content": self._get_fitness_context()}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            payload = {
                "model": self.config['ollama_model'],
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": self.config['temperature'],
                    "num_predict": self.config['max_tokens']
                }
            }
            
            response = requests.post(
                f"{self.config['ollama_base_url']}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                return f"Error: Ollama API returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            return "Error: Could not connect to Ollama. Make sure it's running locally."
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def chat_with_openai(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Chat using OpenAI API"""
        try:
            import openai
            
            if not self.config['openai_api_key']:
                return "Error: OPENAI_API_KEY not configured"
            
            client = openai.OpenAI(api_key=self.config['openai_api_key'])
            
            # Prepare conversation
            messages = [{"role": "system", "content": self._get_fitness_context()}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def chat(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Main chat method that routes to the appropriate provider"""
        if not message.strip():
            return "Please provide a message to chat with me."
        
        try:
            if self.provider == "groq":
                response = self.chat_with_groq(message, conversation_history)
                # If Groq fails with a specific error, suggest switching providers
                if "Error:" in response and "Groq" in response:
                    response += "\n\n💡 Tip: You can switch to another AI provider using the dropdown above."
                return response
            elif self.provider == "ollama":
                return self.chat_with_ollama(message, conversation_history)
            elif self.provider == "openai":
                return self.chat_with_openai(message, conversation_history)
            else:
                return f"Unknown provider: {self.provider}. Please configure a valid provider."
                
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return "Sorry, I encountered an unexpected error. Please try again or switch to a different AI provider."
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = []
        
        if self.config['groq_api_key']:
            providers.append('groq')
        if self.config['openai_api_key']:
            providers.append('openai')
        if self.config['ollama_base_url']:
            providers.append('ollama')
            
        return providers 