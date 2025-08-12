# AI Chatbot Integration for Fitness Club Management System

This document explains how to integrate and use the AI chatbot in your fitness club management system.

## 🚀 Features

- **Multi-Provider Support**: Choose between Groq, Ollama (local), and OpenAI
- **Fitness-Specific Context**: AI trained to help with fitness club inquiries
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Session Management**: Chat history preserved during user sessions
- **Responsive Design**: Mobile-friendly interface
- **Provider Switching**: Change AI providers on the fly

## 📋 Prerequisites

- Python 3.7+
- Flask application running
- Internet connection (for Groq/OpenAI) or local Ollama installation

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Quick Setup (Recommended)

Run the automated setup script:

```bash
python setup_chatbot.py
```

This will guide you through:
- Choosing your AI provider
- Configuring API keys
- Setting up local Ollama (if selected)

### 3. Manual Setup

If you prefer manual configuration, create a `config.env` file:

```env
# AI Chatbot Configuration
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Ollama Configuration (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Chatbot Settings
CHATBOT_PROVIDER=groq  # Options: groq, ollama, openai
MAX_TOKENS=1000
TEMPERATURE=0.7
```

## 🔑 API Key Setup

### Groq
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up and create an API key
3. Add to `config.env`: `GROQ_API_KEY=your_key_here`

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to `config.env`: `OPENAI_API_KEY=your_key_here`

### Ollama (Local)
1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama3.2:3b`
3. Start Ollama service
4. No API key needed

## 🏃‍♂️ Running the Chatbot

### 1. Start Your Flask App

```bash
python run.py
```

### 2. Access the Chatbot

- Navigate to `/chat` in your browser
- Or click "AI Chat" in the navigation menu (requires login)

## 🎯 Usage

### Chat Interface
- **Send Messages**: Type in the input field and press Enter or click Send
- **Clear Chat**: Click "Clear Chat" to reset conversation history
- **Switch Providers**: Use the dropdown to change AI providers
- **Character Limit**: 500 characters per message

### Supported Topics
The AI is trained to help with:
- Fitness advice and workout recommendations
- Class scheduling and information
- Membership questions
- General fitness club inquiries
- Health and wellness tips

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHATBOT_PROVIDER` | AI provider (groq/ollama/openai) | `groq` |
| `MAX_TOKENS` | Maximum response length | `1000` |
| `TEMPERATURE` | Response creativity (0.0-1.0) | `0.7` |
| `GROQ_API_KEY` | Groq API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2:3b` |

### Provider-Specific Settings

#### Groq
- Fast and cost-effective
- Good for real-time responses
- Requires internet connection

#### Ollama
- Completely local and free
- No internet required
- Requires local installation and setup
- Slower than cloud providers

#### OpenAI
- Highest quality responses
- Most expensive option
- Requires internet connection

## 🏗️ Architecture

```
app/
├── ai_chatbot.py          # AI service layer
├── chatbot/               # Chatbot blueprint
│   ├── __init__.py
│   └── routes.py         # API endpoints
└── templates/
    └── chatbot/
        └── chat.html     # Chat interface
```

### Key Components

1. **AIChatbotService**: Handles communication with AI providers
2. **Chatbot Routes**: Flask endpoints for chat functionality
3. **Chat Interface**: Modern, responsive chat UI
4. **Session Management**: Preserves chat history

## 🧪 Testing

### Test the Chatbot

1. Start your Flask application
2. Navigate to `/chat`
3. Send a test message like "What fitness classes do you offer?"
4. Verify the AI responds appropriately

### Test Different Providers

1. Use the provider dropdown to switch between AI services
2. Test each provider with the same question
3. Compare response quality and speed

## 🐛 Troubleshooting

### Common Issues

#### "GROQ_API_KEY not configured"
- Check your `config.env` file
- Ensure the API key is correct
- Restart your Flask application

#### "Could not connect to Ollama"
- Ensure Ollama is installed and running
- Check if the service is accessible at the configured URL
- Verify the model is downloaded: `ollama list`

#### "OpenAI API error"
- Verify your API key is valid
- Check your OpenAI account balance
- Ensure you have access to the selected model

#### Chat not working
- Check browser console for JavaScript errors
- Verify all routes are properly registered
- Check Flask application logs

### Debug Mode

Enable Flask debug mode for detailed error messages:

```python
app.run(debug=True)
```

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **User Authentication**: Chatbot requires user login
- **Rate Limiting**: Consider implementing rate limits for production
- **Input Validation**: Messages are validated before processing

## 📈 Performance Optimization

### For Production

1. **Caching**: Implement response caching for common queries
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Load Balancing**: Use multiple AI provider instances
4. **Monitoring**: Add logging and performance metrics

### For Development

1. **Local Ollama**: Use Ollama for development to avoid API costs
2. **Mock Responses**: Create mock AI responses for testing
3. **Environment Switching**: Use different configs for dev/prod

## 🚀 Deployment

### Environment Setup

1. Set production environment variables
2. Use production-grade AI providers
3. Implement proper logging and monitoring
4. Set up health checks for AI services

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

## 📚 Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [Ollama Documentation](https://ollama.ai/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

To improve the chatbot:

1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Add tests
5. Submit a pull request

## 📄 License

This chatbot integration is part of your fitness club management system.

---

**Need Help?** Check the troubleshooting section or create an issue in your repository. 