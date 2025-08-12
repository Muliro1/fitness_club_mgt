from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from app.ai_chatbot import AIChatbotService
import json
import os

chatbot = Blueprint('chatbot', __name__)

# Initialize chatbot service
chatbot_service = AIChatbotService(provider=os.getenv('CHATBOT_PROVIDER', 'groq'))

@chatbot.route("/chat")
@login_required
def chat_page():
    """Render the chat interface page"""
    available_providers = chatbot_service.get_available_providers()
    current_provider = chatbot_service.provider
    
    return render_template(
        'chatbot/chat.html', 
        title='AI Chatbot',
        available_providers=available_providers,
        current_provider=current_provider
    )

@chatbot.route("/api/chat", methods=['POST'])
@login_required
def chat_api():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get conversation history from session
        conversation_history = session.get('chat_history', [])
        
        # Get AI response
        response = chatbot_service.chat(message, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": response})
        
        # Keep only last 10 messages to prevent session bloat
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        session['chat_history'] = conversation_history
        
        return jsonify({
            'response': response,
            'provider': chatbot_service.provider,
            'timestamp': request.json.get('timestamp')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot.route("/api/chat/clear", methods=['POST'])
@login_required
def clear_chat():
    """Clear chat history"""
    session.pop('chat_history', None)
    return jsonify({'message': 'Chat history cleared'})

@chatbot.route("/api/chat/provider", methods=['POST'])
@login_required
def change_provider():
    """Change AI provider"""
    try:
        data = request.get_json()
        new_provider = data.get('provider', 'groq')
        
        if new_provider not in ['groq', 'ollama', 'openai']:
            return jsonify({'error': 'Invalid provider'}), 400
        
        # Update provider
        global chatbot_service
        chatbot_service = AIChatbotService(provider=new_provider)
        
        # Clear chat history when changing providers
        session.pop('chat_history', None)
        
        return jsonify({
            'message': f'Provider changed to {new_provider}',
            'provider': new_provider
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot.route("/api/chat/providers")
@login_required
def get_providers():
    """Get available AI providers"""
    available_providers = chatbot_service.get_available_providers()
    return jsonify({
        'available_providers': available_providers,
        'current_provider': chatbot_service.provider
    })

@chatbot.route("/api/chat/status")
@login_required
def chat_status():
    """Get chatbot status and configuration"""
    return jsonify({
        'provider': chatbot_service.provider,
        'available_providers': chatbot_service.get_available_providers(),
        'max_tokens': chatbot_service.config['max_tokens'],
        'temperature': chatbot_service.config['temperature']
    }) 