import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Send, 
  Bot, 
  User, 
  Loader2,
  Sparkles,
  MessageSquare,
  Brain
} from 'lucide-react'
import toast from 'react-hot-toast'
import axios from 'axios'

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm your AI Medical Assistant. I can help you understand lung disorders, our diagnostic model, and interpret results. How can I assist you today?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const suggestedQuestions = [
    "What is pneumonia?",
    "How accurate is this model?",
    "What are the symptoms of tuberculosis?",
    "How does the AI model work?",
    "What should I do after diagnosis?",
    "Difference between COVID-19 and pneumonia?",
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (text = input) => {
    if (!text.trim()) {
      toast.error('Please enter a message')
      return
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: text.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/chat', {
        message: text.trim(),
        history: messages.slice(-5) // Send last 5 messages for context
      })

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: response.data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      
      // Fallback response if API fails
      const fallbackResponse = getFallbackResponse(text.trim())
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: fallbackResponse,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, botMessage])
    } finally {
      setLoading(false)
    }
  }

  const getFallbackResponse = (question) => {
    const q = question.toLowerCase()
    
    if (q.includes('pneumonia')) {
      return "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing. Common symptoms include chest pain when breathing or coughing, confusion or changes in mental awareness, cough, fatigue, fever, and nausea."
    }
    
    if (q.includes('tuberculosis') || q.includes('tb')) {
      return "Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs. It's caused by bacteria called Mycobacterium tuberculosis. Symptoms include persistent cough lasting more than 3 weeks, chest pain, coughing up blood, fatigue, fever, night sweats, and weight loss. TB requires long-term antibiotic treatment."
    }
    
    if (q.includes('covid') || q.includes('coronavirus')) {
      return "COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. Common symptoms include fever, cough, shortness of breath, fatigue, muscle aches, loss of taste or smell, sore throat, and congestion. On chest X-rays, COVID-19 can show bilateral ground-glass opacities. The severity ranges from mild to critical."
    }
    
    if (q.includes('accurate') || q.includes('accuracy')) {
      return "Our hybrid MobileNet + Vision Transformer model has been trained on thousands of chest X-ray images and achieves approximately 94.2% accuracy on our test dataset. However, please note that this tool is for research and educational purposes only and should NOT replace professional medical diagnosis. Always consult with qualified healthcare professionals."
    }
    
    if (q.includes('how') && (q.includes('work') || q.includes('model'))) {
      return "Our AI model uses a hybrid architecture combining MobileNet (a lightweight CNN) for efficient feature extraction and Vision Transformer (ViT) for capturing global context through self-attention. The MobileNet extracts local features from the X-ray image, while the ViT processes these features to understand long-range dependencies. This combination provides both efficiency and high accuracy in detecting lung disorders."
    }
    
    if (q.includes('after diagnosis') || q.includes('next steps')) {
      return "After receiving a prediction from our system:\n\n1. DO NOT use this as a final diagnosis\n2. Consult with a qualified healthcare professional immediately\n3. Share these results with your doctor\n4. Follow up with proper medical testing (additional imaging, lab tests, etc.)\n5. Follow your doctor's treatment recommendations\n\nRemember: This AI tool is for research and educational purposes only. It's designed to assist, not replace, medical professionals."
    }
    
    return "I'm here to help answer questions about lung disorders, our AI diagnostic model, and general medical information. However, I'm not a replacement for professional medical advice. For specific medical concerns, please consult with a qualified healthcare provider. Feel free to ask me about pneumonia, tuberculosis, COVID-19, how our model works, or what to do after receiving results."
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center space-x-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full mb-4">
            <Brain className="w-5 h-5" />
            <span className="text-sm font-semibold">AI Medical Assistant</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Chat with AI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get answers about lung disorders, understand your results, and learn about our AI model
          </p>
        </motion.div>

        {/* Chat Container */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card overflow-hidden"
        >
          {/* Messages */}
          <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
            <AnimatePresence initial={false}>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex items-start space-x-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                      message.type === 'bot' 
                        ? 'bg-gradient-to-br from-primary-500 to-primary-700' 
                        : 'bg-gradient-to-br from-gray-700 to-gray-900'
                    }`}>
                      {message.type === 'bot' ? (
                        <Bot className="w-6 h-6 text-white" />
                      ) : (
                        <User className="w-6 h-6 text-white" />
                      )}
                    </div>
                    
                    <div className={`rounded-2xl px-4 py-3 ${
                      message.type === 'bot'
                        ? 'bg-white shadow-md'
                        : 'bg-primary-600 text-white'
                    }`}>
                      <p className={`text-sm whitespace-pre-wrap ${
                        message.type === 'bot' ? 'text-gray-800' : 'text-white'
                      }`}>
                        {message.text}
                      </p>
                      <p className={`text-xs mt-2 ${
                        message.type === 'bot' ? 'text-gray-500' : 'text-primary-100'
                      }`}>
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {loading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start"
              >
                <div className="flex items-start space-x-3 max-w-[80%]">
                  <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
                    <Bot className="w-6 h-6 text-white" />
                  </div>
                  <div className="bg-white rounded-2xl px-4 py-3 shadow-md">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="w-4 h-4 text-primary-600 animate-spin" />
                      <span className="text-sm text-gray-600">Thinking...</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Questions */}
          {messages.length <= 1 && (
            <div className="p-6 border-t border-gray-200 bg-white">
              <p className="text-sm font-semibold text-gray-700 mb-3">Suggested questions:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleSend(question)}
                    className="text-left px-4 py-2 bg-primary-50 hover:bg-primary-100 text-primary-700 rounded-lg text-sm transition-colors"
                  >
                    <Sparkles className="w-3 h-3 inline mr-2" />
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="p-6 border-t border-gray-200 bg-white">
            <div className="flex items-end space-x-3">
              <div className="flex-1">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about lung disorders or the diagnosis..."
                  rows="2"
                  disabled={loading}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200 resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                />
              </div>
              <button
                onClick={() => handleSend()}
                disabled={loading || !input.trim()}
                className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            
            <p className="text-xs text-gray-500 mt-3 flex items-center">
              <MessageSquare className="w-3 h-3 mr-1" />
              This AI assistant provides general information only. Not a substitute for medical advice.
            </p>
          </div>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="card p-6 mt-6 bg-yellow-50 border border-yellow-200"
        >
          <h3 className="font-semibold text-yellow-900 mb-2">Important Notice</h3>
          <p className="text-sm text-yellow-800">
            This AI chatbot provides general medical information and explanations about lung disorders 
            and our diagnostic system. It is NOT a substitute for professional medical advice, diagnosis, 
            or treatment. Always seek the advice of your physician or other qualified health provider 
            with any questions you may have regarding a medical condition.
          </p>
        </motion.div>
      </div>
    </div>
  )
}

export default ChatbotPage
