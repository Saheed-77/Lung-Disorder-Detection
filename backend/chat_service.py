"""
AI Chat Service using Google Gemini
Medical Q&A Assistant for Lung Disease Detection
"""

import os
import logging
from typing import List, Dict
import warnings

# Suppress the deprecation warning temporarily
warnings.filterwarnings('ignore', category=FutureWarning, module='google.generativeai')

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY and GENAI_AVAILABLE:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("Gemini AI configured successfully")
    except Exception as e:
        logger.warning(f"Failed to configure Gemini: {e}")
else:
    if not GENAI_AVAILABLE:
        logger.warning("google-generativeai package not available")
    else:
        logger.warning("GEMINI_API_KEY not found in environment variables")


# System prompt for the medical assistant
SYSTEM_PROMPT = """You are an expert AI Medical Assistant specializing in lung disorders and respiratory diseases. You help users understand:
- Lung diseases (COVID-19, Pneumonia, Tuberculosis, and other respiratory conditions)
- Chest X-ray interpretations
- Our AI diagnostic model (Hybrid InceptionV3 + Vision Transformer)
- Medical symptoms and when to seek care

**Important Guidelines:**
1. Always emphasize that this is for educational purposes only
2. Remind users to consult qualified healthcare professionals for diagnosis and treatment
3. Be empathetic and clear in your explanations
4. Provide accurate medical information in simple language
5. If asked about specific diagnoses, always recommend professional medical evaluation
6. Explain complex medical concepts in an accessible way

**About Our AI Model:**
- Uses Hybrid InceptionV3 + Vision Transformer architecture
- Trained on chest X-ray images
- Can detect: COVID-19, Pneumonia, Tuberculosis, and Normal chest X-rays
- Achieves ~94% accuracy on test data
- For research and educational purposes ONLY

**Your tone should be:**
- Professional yet friendly
- Empathetic and supportive
- Clear and educational
- Cautious about medical advice

Always remember: You are an educational tool, NOT a replacement for professional medical advice."""


def get_gemini_response(message: str, history: List[Dict] = None) -> str:
    """
    Get AI response from Google Gemini
    
    Args:
        message: User's message
        history: Previous conversation history
        
    Returns:
        AI-generated response
    """
    try:
        if not GEMINI_API_KEY or not GENAI_AVAILABLE:
            logger.error("Gemini API not configured or package not available")
            return get_fallback_response(message)
        
        # Initialize Gemini model - using gemini-2.5-flash (fast and capable)
       # model = genai.GenerativeModel('gemini-2.5-flash')
      
        model = genai.GenerativeModel('gemini-3-flash-preview')
        # Build conversation context
        conversation_context = build_conversation_context(message, history)
        
        # Generate response
        response = model.generate_content(conversation_context)
        
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        logger.warning("Falling back to rule-based responses")
        return get_fallback_response(message)


def build_conversation_context(message: str, history: List[Dict] = None) -> str:
    """Build conversation context with system prompt and history"""
    
    context_parts = [SYSTEM_PROMPT, "\n\n**Conversation:**\n"]
    
    # Add conversation history (last 5 messages for context)
    if history:
        recent_history = history[-5:] if len(history) > 5 else history
        for msg in recent_history:
            role = "User" if msg.get("type") == "user" else "Assistant"
            text = msg.get("text", "")
            context_parts.append(f"{role}: {text}\n")
    
    # Add current user message
    context_parts.append(f"\nUser: {message}\n")
    context_parts.append("\nAssistant:")
    
    return "".join(context_parts)


def get_fallback_response(message: str) -> str:
    """Fallback responses when Gemini API is unavailable"""
    
    message_lower = message.lower()
    
    # COVID-19
    if 'covid' in message_lower or 'coronavirus' in message_lower:
        return """**COVID-19 (Coronavirus Disease)**

COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.

**Common Symptoms:**
- Fever or chills
- Dry cough
- Shortness of breath
- Fatigue
- Loss of taste or smell
- Sore throat

**Chest X-ray Findings:**
- Bilateral ground-glass opacities
- Peripheral distribution
- Lower lobe predominance

**Important:** Our AI model can detect patterns consistent with COVID-19, but definitive diagnosis requires RT-PCR testing. Always consult healthcare professionals.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # Pneumonia
    elif 'pneumonia' in message_lower:
        return """**Pneumonia**

Pneumonia is an infection that inflames the air sacs in one or both lungs.

**Types:**
- Bacterial (most common: Streptococcus pneumoniae)
- Viral (influenza, RSV, etc.)
- Fungal (less common)

**Symptoms:**
- Cough with phlegm
- Fever and chills
- Shortness of breath
- Chest pain when breathing
- Fatigue

**X-ray Findings:**
- Consolidation or infiltrates
- May be lobar or patchy
- Air bronchograms

**Treatment:** Requires professional medical evaluation. Bacterial pneumonia needs antibiotics.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # Tuberculosis
    elif 'tuberculosis' in message_lower or 'tb' in message_lower:
        return """**Tuberculosis (TB)**

TB is a serious infectious disease caused by Mycobacterium tuberculosis bacteria.

**Symptoms:**
- Persistent cough (3+ weeks)
- Coughing up blood
- Chest pain
- Weight loss
- Fever and night sweats

**Transmission:**
- Airborne droplets
- Close contact with infected individuals

**X-ray Findings:**
- Upper lobe infiltrates
- Cavitation
- Hilar lymphadenopathy

**Treatment:**
- Long-term antibiotics (6-9 months)
- Multi-drug therapy
- Complete treatment is crucial

**Important:** TB is curable with proper treatment. Early detection and medical care are essential.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # Model information
    elif any(word in message_lower for word in ['model', 'how', 'work', 'architecture', 'ai']):
        return """**Our AI Model Architecture**

We use a **Hybrid InceptionV3 + Vision Transformer** system:

**InceptionV3 (CNN):**
- Extracts 2048-dimensional features
- Multi-scale feature extraction
- Captures local patterns and textures
- Input: 299×299 images

**Vision Transformer (ViT):**
- Extracts 768-dimensional features
- Self-attention for global context
- Captures long-range dependencies
- Input: 224×224 images

**Performance:**
- Accuracy: ~94% on test data
- Trained on thousands of chest X-rays
- Classes: COVID-19, Pneumonia, Tuberculosis, Normal

**Important:** This is for research and educational purposes ONLY. Always consult healthcare professionals for medical diagnosis.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # Accuracy/reliability
    elif 'accura' in message_lower or 'reliable' in message_lower or 'trust' in message_lower:
        return """**Model Accuracy & Reliability**

**Performance Metrics:**
- Overall Accuracy: ~94% on test dataset
- Trained on large chest X-ray datasets
- Validated on diverse patient populations

**Important Limitations:**
1. This tool is for educational and research purposes ONLY
2. NOT a substitute for professional medical diagnosis
3. X-rays alone cannot provide complete diagnosis
4. Clinical correlation is always required
5. Some conditions may not be visible on X-rays

**Best Practices:**
- Use as a screening tool only
- Always consult qualified healthcare professionals
- Share results with your doctor
- Follow up with proper medical testing
- Consider clinical symptoms and history

Remember: AI assists healthcare professionals but cannot replace them.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # What to do after diagnosis
    elif 'after' in message_lower or 'next step' in message_lower or 'what should' in message_lower:
        return """**After Receiving AI Prediction**

**Important Steps:**

1. **DO NOT Self-Diagnose**
   - This is NOT a final diagnosis
   - AI is a screening tool only

2. **Consult Healthcare Professional**
   - Schedule appointment with doctor
   - Share the AI results with them
   - Discuss your symptoms

3. **Follow Medical Advice**
   - Get proper diagnostic tests
   - Follow prescribed treatment
   - Complete full medication course

4. **Additional Testing May Include:**
   - Clinical examination
   - Laboratory tests
   - CT scans if needed
   - Sputum tests for TB/bacteria

5. **Monitor Symptoms**
   - Track any changes
   - Seek emergency care if symptoms worsen
   - Follow up as recommended

**Emergency Signs (Seek immediate care):**
- Severe difficulty breathing
- Chest pain
- High fever
- Coughing up blood
- Confusion or altered consciousness

Remember: Professional medical evaluation is essential for proper diagnosis and treatment.

*Note: I'm currently running in offline mode. For more detailed assistance, please ensure the API is configured.*"""

    # Generic response
    else:
        return """Hello! I'm your AI Medical Assistant for lung disease information.

**I can help you with:**
- Understanding lung disorders (COVID-19, Pneumonia, TB)
- Explaining chest X-ray findings
- Information about our AI diagnostic model
- General medical information about respiratory health
- Guidance on next steps after diagnosis

**Ask me about:**
- Symptoms of lung diseases
- How our AI model works
- What to do after receiving results
- Differences between respiratory conditions

**Important:** I provide educational information only. For medical diagnosis and treatment, always consult qualified healthcare professionals.

*Note: I'm currently running in offline mode with limited capabilities. For the best experience, please ensure the Gemini API is configured.*

How can I help you today?"""


# Test function
if __name__ == "__main__":
    # Test the chat service
    print("Testing Gemini Chat Service...")
    
    test_message = "What is pneumonia?"
    response = get_gemini_response(test_message)
    
    print(f"\nUser: {test_message}")
    print(f"\nAssistant: {response}")
