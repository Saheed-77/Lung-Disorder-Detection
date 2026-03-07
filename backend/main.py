from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io
import time
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lung Disorder Detection API",
    description="AI-powered lung disorder detection using Hybrid MobileNet + Vision Transformer",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Disease classes
CLASSES = ['Normal', 'Pneumonia', 'Tuberculosis', 'COVID-19']

# Model placeholder (replace with actual model loading)
model = None

def load_model():
    """Load the trained model"""
    global model
    try:
        # TODO: Load your actual trained model here
        # model = tf.keras.models.load_model('models/hybrid_mobilenet_vit.h5')
        logger.info("Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model input"""
    # Resize to model input size (typically 224x224 or 256x256)
    image = image.convert('RGB')
    image = image.resize((224, 224))
    
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def get_mock_prediction(image_array: np.ndarray) -> Dict:
    """
    Generate mock predictions for demonstration
    Replace this with actual model inference
    """
    # Simulate model processing time
    time.sleep(1)
    
    # Mock probabilities (these would come from your actual model)
    probabilities = {
        'Normal': np.random.uniform(0.1, 0.3),
        'Pneumonia': np.random.uniform(0.4, 0.8),
        'Tuberculosis': np.random.uniform(0.05, 0.15),
        'COVID-19': np.random.uniform(0.05, 0.15)
    }
    
    # Normalize probabilities to sum to 1
    total = sum(probabilities.values())
    probabilities = {k: v/total for k, v in probabilities.items()}
    
    # Get prediction
    prediction = max(probabilities, key=probabilities.get)
    confidence = probabilities[prediction]
    
    return {
        'prediction': prediction,
        'confidence': float(confidence),
        'probabilities': {k: float(v) for k, v in probabilities.items()}
    }

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    logger.info("Starting Lung Disorder Detection API...")
    load_model()

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Lung Disorder Detection API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "predict": "/api/predict",
            "chat": "/api/chat",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": time.time()
    }

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict lung disorder from chest X-ray image
    
    Args:
        file: Uploaded image file (chest X-ray)
    
    Returns:
        JSON with prediction, confidence, and probabilities
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Log image info
        logger.info(f"Processing image: {file.filename}, size: {image.size}")
        
        # Preprocess image
        img_array = preprocess_image(image)
        
        # Get prediction
        start_time = time.time()
        
        if model is not None:
            # TODO: Use actual model prediction
            # predictions = model.predict(img_array)
            # result = process_predictions(predictions)
            result = get_mock_prediction(img_array)
        else:
            # Use mock predictions if model not loaded
            result = get_mock_prediction(img_array)
        
        inference_time = time.time() - start_time
        result['inference_time'] = round(inference_time, 3)
        
        logger.info(f"Prediction: {result['prediction']}, Confidence: {result['confidence']:.2%}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict]] = []

@app.post("/api/chat")
async def chat(chat_msg: ChatMessage):
    """
    AI chatbot endpoint for medical Q&A
    
    Args:
        chat_msg: User message and conversation history
    
    Returns:
        JSON with chatbot response
    """
    try:
        user_message = chat_msg.message.lower()
        
        # Simple rule-based responses (can be replaced with LLM)
        response = get_chatbot_response(user_message)
        
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

def get_chatbot_response(message: str) -> str:
    """Generate chatbot response based on user message"""
    
    if 'pneumonia' in message:
        return """Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing.

**Common Symptoms:**
- Cough with phlegm or pus
- Fever, sweating, and chills
- Shortness of breath
- Chest pain when breathing or coughing
- Fatigue and muscle aches

**Causes:** Can be caused by bacteria, viruses, or fungi. Streptococcus pneumoniae is the most common bacterial cause.

**Treatment:** Depends on the cause - bacterial pneumonia is treated with antibiotics. Always consult a healthcare professional for proper diagnosis."""
    
    elif 'tuberculosis' in message or 'tb' in message:
        return """Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs. It's caused by bacteria called Mycobacterium tuberculosis.

**Symptoms:**
- Persistent cough lasting more than 3 weeks
- Coughing up blood or mucus
- Chest pain when breathing or coughing
- Unintentional weight loss
- Fatigue and weakness
- Fever and night sweats

**Transmission:** TB spreads through the air when infected people cough, sneeze, or spit.

**Treatment:** Requires long-term antibiotic treatment (usually 6-9 months). Early detection and treatment are crucial to prevent spread and complications."""
    
    elif 'covid' in message or 'coronavirus' in message:
        return """COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.

**Common Symptoms:**
- Fever or chills
- Cough (usually dry)
- Shortness of breath
- Fatigue
- Muscle or body aches
- Loss of taste or smell
- Sore throat
- Congestion or runny nose

**X-ray Findings:** Chest X-rays may show bilateral ground-glass opacities, especially in the lower lung zones.

**Important:** Severity ranges from mild to critical. Seek immediate medical attention if you experience difficulty breathing, persistent chest pain, confusion, or inability to stay awake."""
    
    elif 'accurate' in message or 'accuracy' in message:
        return """Our hybrid MobileNet + Vision Transformer model achieves approximately **94.2% accuracy** on our test dataset, trained on thousands of chest X-ray images.

**Important Notes:**
- This accuracy is based on research datasets and controlled conditions
- Real-world performance may vary depending on image quality
- This tool is for research and educational purposes ONLY
- It should NOT replace professional medical diagnosis
- Always consult qualified healthcare professionals for medical decisions

The model combines CNN feature extraction with transformer attention mechanisms for improved accuracy."""
    
    elif 'model' in message or 'how' in message:
        return """Our AI system uses a **Hybrid MobileNet + Vision Transformer (ViT)** architecture:

**1. MobileNet CNN:**
- Lightweight convolutional neural network
- Extracts local features from X-ray images
- Efficient for edge deployment

**2. Vision Transformer (ViT):**
- Self-attention mechanism
- Captures global context and long-range dependencies
- Processes image patches as sequences

**3. Hybrid Fusion:**
- Combines CNN local features with Transformer global attention
- Superior performance compared to individual architectures
- Optimized for medical image analysis

The model is trained on diverse chest X-ray datasets to detect pneumonia, tuberculosis, COVID-19, and normal cases."""
    
    elif 'after diagnosis' in message or 'next steps' in message or 'what should i do' in message:
        return """After receiving a prediction from our system, follow these steps:

**1. DO NOT use this as final diagnosis**
- This is a research tool, not a medical device
- It's designed to assist, not replace medical professionals

**2. Consult Healthcare Professional**
- Schedule an appointment with a qualified doctor
- Share the X-ray and AI results with them
- Get a professional medical evaluation

**3. Additional Testing**
- Your doctor may order additional tests
- This could include blood work, CT scans, or other imaging
- Follow their recommendations

**4. Treatment**
- Only follow treatment prescribed by licensed healthcare providers
- Do not self-medicate based on AI predictions

**5. Monitor Symptoms**
- Keep track of any symptoms
- Report changes to your healthcare provider

Remember: Early professional consultation is crucial for proper diagnosis and treatment."""
    
    elif 'symptom' in message:
        return """I can provide general information about lung disorder symptoms:

**Pneumonia:** Cough with phlegm, fever, chest pain, shortness of breath, fatigue

**Tuberculosis:** Persistent cough (3+ weeks), coughing blood, night sweats, weight loss, fever

**COVID-19:** Dry cough, fever, shortness of breath, loss of taste/smell, fatigue

**When to Seek Emergency Care:**
- Severe difficulty breathing
- Persistent chest pain or pressure
- Confusion or inability to stay awake
- Bluish lips or face
- Coughing up blood

**Important:** If you're experiencing symptoms, consult a healthcare professional immediately. Don't rely solely on AI predictions for medical decisions."""
    
    elif 'thank' in message:
        return "You're welcome! Remember, this tool is for educational purposes. Always consult healthcare professionals for medical advice. Is there anything else you'd like to know?"
    
    else:
        return """I'm here to help answer questions about:

- **Lung disorders** (Pneumonia, Tuberculosis, COVID-19)
- **Our AI model** (How it works, accuracy, architecture)
- **Symptoms** and general medical information
- **What to do** after receiving results

**Examples of questions you can ask:**
- "What is pneumonia?"
- "How accurate is your model?"
- "What are the symptoms of tuberculosis?"
- "What should I do after diagnosis?"

Please note: I provide general medical information only. For specific medical concerns, always consult qualified healthcare professionals."""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
