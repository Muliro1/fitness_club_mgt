# Ollama Setup Guide

Ollama is a local AI service that runs on your machine, providing free AI capabilities without internet dependency.

## 🚀 Quick Installation

### Ubuntu/Debian
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Download from: https://ollama.ai/download

## 🔧 Setup Steps

1. **Start Ollama service:**
   ```bash
   ollama serve
   ```

2. **Download a model (in another terminal):**
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Test if it's working:**
   ```bash
   ollama run llama3.2:3b "Hello, how are you?"
   ```

## 🧪 Test Connection

Run the test script to verify Ollama is working:
```bash
python3 test_groq.py
```

## 💡 Benefits of Ollama

- **Free**: No API costs
- **Local**: Works offline
- **Private**: Data stays on your machine
- **Customizable**: Can use different models

## 🔄 Switching to Ollama

1. In your Flask app, go to `/chat`
2. Use the provider dropdown to select "Ollama"
3. Start chatting!

## 🐛 Troubleshooting

### "Connection refused"
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is available

### "Model not found"
- Download the model: `ollama pull llama3.2:3b`
- Check available models: `ollama list`

### Performance issues
- Use smaller models for faster responses
- Ensure you have enough RAM (at least 4GB for 3B models) 