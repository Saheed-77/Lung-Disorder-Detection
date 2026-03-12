# Gemini AI Chatbot Setup Guide

## 🤖 AI Chatbot Integration

Your chatbot is now powered by **Google Gemini AI** for intelligent, context-aware responses about lung diseases and medical information.

## 📋 Setup Instructions

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure the API Key

Create a `.env` file in the `backend` directory:

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file and add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `google-generativeai` package along with other dependencies.

### 4. Run the Backend

```bash
python torch_main.py
```

The API will start on `http://localhost:8001`

## ✨ Features

### With Gemini API Key:
- ✅ **Intelligent AI responses** powered by Google Gemini
- ✅ **Context-aware conversations** remembering chat history
- ✅ **Natural language understanding** for complex medical queries
- ✅ **Detailed explanations** about lung diseases
- ✅ **Interactive Q&A** with follow-up questions

### Without API Key (Fallback Mode):
- ⚡ **Rule-based responses** for common questions
- ⚡ **Pre-defined answers** for:
  - COVID-19 information
  - Pneumonia details
  - Tuberculosis facts
  - Model architecture
  - Diagnosis guidance

## 🔒 Security Notes

- **Never commit** your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Keep your API key confidential
- Google Gemini has free tier limits - monitor your usage

## 💡 Usage Examples

### Frontend (ChatbotPage.jsx)

The chatbot automatically sends messages to the backend:

```javascript
const response = await axios.post('/api/chat', {
  message: userMessage,
  history: previousMessages
})
```

### Backend API Endpoint

```
POST /api/chat
Content-Type: application/json

{
  "message": "What is pneumonia?",
  "history": [
    {"type": "user", "text": "Hello"},
    {"type": "bot", "text": "Hi! How can I help you?"}
  ]
}
```

### Response Format

```json
{
  "response": "Pneumonia is an infection that inflames..."
}
```

## 🧪 Testing

Test the chatbot integration:

```bash
cd backend
python chat_service.py
```

Or test via API:

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is COVID-19?"}'
```

## 📊 API Limits

**Google Gemini Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- Generous free quota for development

If you exceed limits, the system automatically falls back to rule-based responses.

## 🎯 Customization

### Modify the System Prompt

Edit `backend/chat_service.py` to customize the AI's behavior:

```python
SYSTEM_PROMPT = """
You are an expert AI Medical Assistant...
"""
```

### Add Fallback Responses

Update `get_fallback_response()` function in `chat_service.py` to add more rule-based responses.

## 🐛 Troubleshooting

**Issue: "Gemini API key not configured"**
- Solution: Check your `.env` file exists and has the correct API key

**Issue: "Rate limit exceeded"**
- Solution: Wait a few minutes or upgrade to paid tier

**Issue: "Module 'google.generativeai' not found"**
- Solution: Run `pip install google-generativeai`

**Issue: Chatbot not responding**
- Check backend is running on port 8001
- Check browser console for errors
- Verify API endpoint in vite.config.js

## 📚 Resources

- [Google Gemini Documentation](https://ai.google.dev/docs)
- [API Reference](https://ai.google.dev/api/python/google/generativeai)
- [Gemini Models](https://ai.google.dev/models/gemini)

## 🚀 What's Next?

- Add conversation memory storage
- Implement multi-turn conversations
- Add voice input/output
- Integrate with diagnosis results
- Add medical literature citations

---

**Note:** This chatbot is for educational purposes only. Always consult qualified healthcare professionals for medical advice.
