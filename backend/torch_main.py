"""
FastAPI Backend for Lung Disease Detection
InceptionV3 + Vision Transformer Model
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import torch
import torch.nn as nn
from torchvision import transforms
from transformers import ViTModel
from torchvision.models import inception_v3
from PIL import Image
import io
import json
import time
import logging
from typing import Dict, List, Optional
import numpy as np
import os
import cv2
import base64

# Import chat service for Gemini AI integration
from chat_service import get_gemini_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
model = None
device = None
class_mapping = None
idx_to_class = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("Starting Lung Disease Detection API (InceptionV3 + ViT)...")
    load_model()
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Lung Disease Detection API - InceptionV3 + ViT",
    description="AI-powered lung disease detection using InceptionV3 + Vision Transformer",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For Hugging Face, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
device = None
class_mapping = None
idx_to_class = None

# Model Architecture
class MultiStageInceptionViT(nn.Module):
    """
    Hybrid model combining InceptionV3 and Vision Transformer
    - InceptionV3: Extracts 2048-dimensional features
    - ViT: Extracts 768-dimensional features from transformers
    - Combined: 2816-dimensional feature vector
    """
    def __init__(self, num_classes=4):
        super(MultiStageInceptionViT, self).__init__()
        # InceptionV3 backbone
        self.backbone_cnn = inception_v3(pretrained=False, aux_logits=True)
        self.backbone_cnn.AuxLogits = None
        self.backbone_cnn.fc = nn.Identity()  # Remove classifier, keep features

        # Vision Transformer backbone
        self.vit = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

        # Combined classifier
        self.fc = nn.Linear(2048 + self.vit.config.hidden_size, num_classes)

    def forward(self, x):
        # InceptionV3 path (299x299 input)
        cnn_out = self.backbone_cnn(x)
        
        # Handle InceptionOutputs if aux_logits was enabled
        if not torch.is_tensor(cnn_out):
            cnn_out = cnn_out.logits

        # ViT path (resize to 224x224 for ViT)
        vit_input = torch.nn.functional.interpolate(x, size=(224, 224))
        vit_out = self.vit(pixel_values=vit_input).pooler_output

        # Combine features and classify
        combined = torch.cat((cnn_out, vit_out), dim=1)
        return self.fc(combined)


def load_model():
    """Load the trained PyTorch model"""
    global model, device, class_mapping, idx_to_class
    
    try:
        # Set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Build paths relative to script location
        class_mapping_path = os.path.join(script_dir, "inception", "class_mapping (1).json")
        model_path = os.path.join(script_dir, "inception", "inceptionv3_vit_lung.pth")
        
        logger.info(f"Loading class mapping from: {class_mapping_path}")
        
        # Load class mapping
        with open(class_mapping_path, "r") as f:
            class_mapping = json.load(f)
        
        # Create reverse mapping (index to class name)
        idx_to_class = {v: k for k, v in class_mapping.items()}
        logger.info(f"Classes loaded: {class_mapping}")
        
        # Initialize model
        logger.info("Initializing model architecture...")
        model = MultiStageInceptionViT(num_classes=4)
        
        # Load trained weights
        logger.info(f"Loading model weights from: {model_path}")
        checkpoint = torch.load(model_path, map_location=device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        
        model.to(device)
        model.eval()
        
        logger.info("Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        logger.exception(e)
        return False


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Preprocess image for InceptionV3 + ViT model
    - Resize to 299x299 (InceptionV3 input size)
    - Normalize with ImageNet statistics
    """
    transform = transforms.Compose([
        transforms.Resize((299, 299)),  # InceptionV3 uses 299x299
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet mean
            std=[0.229, 0.224, 0.225]     # ImageNet std
        )
    ])
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply transforms and add batch dimension
    img_tensor = transform(image).unsqueeze(0)
    return img_tensor


class GradCAM:
    """Gradient-weighted Class Activation Mapping for visualization"""
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate_cam(self, input_tensor, target_class=None):
        """Generate CAM heatmap"""
        # Forward pass
        output = self.model(input_tensor)
        
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        target = output[0, target_class]
        target.backward()
        
        # Generate CAM
        gradients = self.gradients[0]  # [C, H, W]
        activations = self.activations[0]  # [C, H, W]
        
        # Global average pooling on gradients
        weights = gradients.mean(dim=(1, 2))  # [C]
        
        # Weighted combination of activation maps
        cam = torch.zeros(activations.shape[1:], dtype=torch.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i]
        
        # ReLU and normalize
        cam = torch.relu(cam)
        cam = cam - cam.min()
        if cam.max() > 0:
            cam = cam / cam.max()
        
        return cam.cpu().numpy(), target_class


def generate_gradcam_overlay(image: Image.Image, model, img_tensor, predicted_class):
    """Generate Grad-CAM heatmap overlay on original image"""
    try:
        # Temporarily set model to train mode to enable gradient computation
        was_training = model.training
        model.train()
        
        # Target the last convolutional layer in InceptionV3
        target_layer = model.backbone_cnn.Mixed_7c
        
        # Create GradCAM object
        gradcam = GradCAM(model, target_layer)
        
        # Generate CAM
        cam, _ = gradcam.generate_cam(img_tensor, target_class=predicted_class)
        
        # Restore model mode
        if not was_training:
            model.eval()
        
        # Resize CAM to match original image size
        cam = cv2.resize(cam, (image.width, image.height))
        
        # Convert to heatmap
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # Convert original image to numpy
        image_np = np.array(image.convert('RGB'))
        
        # Resize image if needed
        if image_np.shape[:2] != heatmap.shape[:2]:
            image_np = cv2.resize(image_np, (heatmap.shape[1], heatmap.shape[0]))
        
        # Overlay heatmap on image (40% heatmap, 60% original)
        overlay = cv2.addWeighted(image_np, 0.6, heatmap, 0.4, 0)
        
        # Convert to PIL Image
        overlay_img = Image.fromarray(overlay)
        
        # Convert to base64
        buffered = io.BytesIO()
        overlay_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        logger.info(f"Grad-CAM overlay generated successfully, size: {len(img_str)} bytes")
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        logger.error(f"Error generating Grad-CAM: {str(e)}")
        logger.exception(e)
        return None


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    logger.info("Starting Lung Disease Detection API (InceptionV3 + ViT)...")
    load_model()


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Lung Disease Detection API - InceptionV3 + ViT",
        "version": "2.0.0",
        "model": "InceptionV3 + Vision Transformer",
        "status": "online",
        "classes": list(class_mapping.keys()) if class_mapping else [],
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
        "device": str(device) if device else "not set",
        "model_type": "InceptionV3 + ViT",
        "num_classes": len(class_mapping) if class_mapping else 0,
        "timestamp": time.time()
    }


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict lung disease from chest X-ray image
    
    Args:
        file: Uploaded chest X-ray image (PNG, JPG, JPEG)
    
    Returns:
        JSON with prediction, confidence, and class probabilities
    """
    try:
        # Validate model is loaded
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        original_image = image.copy()  # Keep original for Grad-CAM
        
        logger.info(f"Processing image: {file.filename}, size: {image.size}, mode: {image.mode}")
        
        # Preprocess image
        img_tensor = preprocess_image(image)
        img_tensor = img_tensor.to(device)
        
        # Get prediction (without gradients for speed)
        start_time = time.time()
        
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            probs = probabilities[0].cpu().numpy()
            predicted_idx = outputs.argmax(dim=1).item()
        
        inference_time = time.time() - start_time
        
        # Get predicted class name
        predicted_class = idx_to_class[predicted_idx]
        confidence = float(probs[predicted_idx])
        
        # Create probability dictionary with class names
        prob_dict = {
            idx_to_class[i]: float(probs[i]) 
            for i in range(len(probs))
        }
        
        # Generate Grad-CAM heatmap (requires gradients, so outside no_grad context)
        logger.info("Generating Grad-CAM visualization...")
        try:
            # Create a fresh tensor with gradients enabled for Grad-CAM
            img_tensor_grad = preprocess_image(original_image).to(device)
            img_tensor_grad.requires_grad = True
            
            heatmap_base64 = generate_gradcam_overlay(original_image, model, img_tensor_grad, predicted_idx)
            logger.info(f"Grad-CAM generated: {'Success' if heatmap_base64 else 'Failed'}")
        except Exception as e:
            logger.error(f"Grad-CAM generation failed: {str(e)}")
            heatmap_base64 = None
        
        result = {
            "prediction": predicted_class,
            "confidence": confidence,
            "probabilities": prob_dict,
            "inference_time": round(inference_time, 3),
            "model": "InceptionV3 + ViT",
            "gradcam": heatmap_base64  # Add Grad-CAM heatmap
        }
        
        logger.info(f"Prediction: {predicted_class}, Confidence: {confidence:.2%}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict]] = []


@app.post("/api/chat")
async def chat(chat_msg: ChatMessage):
    """
    AI chatbot endpoint for medical Q&A using Google Gemini
    """
    try:
        user_message = chat_msg.message
        history = chat_msg.history if chat_msg.history else []
        
        # Use Gemini AI for intelligent responses
        response = get_gemini_response(user_message, history)
        
        logger.info(f"Chat request processed successfully")
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


def get_chatbot_response(message: str) -> str:
    """Generate chatbot response based on user message"""
    
    if 'covid' in message or 'coronavirus' in message or 'corona virus' in message:
        return """COVID-19 (Corona Virus Disease) is a respiratory illness caused by the SARS-CoV-2 virus.

**Common Symptoms:**
- Fever or chills
- Dry cough
- Shortness of breath or difficulty breathing
- Fatigue
- Muscle or body aches
- New loss of taste or smell
- Sore throat
- Congestion or runny nose

**Chest X-ray Findings:**
- Bilateral ground-glass opacities
- Peripheral and lower lung zone distribution
- Consolidation in severe cases

**Important:** Our AI model can detect patterns consistent with COVID-19 in chest X-rays, but a definitive diagnosis requires RT-PCR testing and clinical correlation. Always consult healthcare professionals."""

    elif 'pneumonia' in message:
        return """Pneumonia is an infection that inflames the air sacs in one or both lungs.

**Types:**
- **Bacterial Pneumonia**: Caused by bacteria (e.g., Streptococcus pneumoniae)
- **Viral Pneumonia**: Caused by viruses (e.g., influenza, RSV)
- **Fungal Pneumonia**: Less common, affects immunocompromised individuals

**Symptoms:**
- Cough with phlegm or pus
- Fever, sweating, and chills
- Shortness of breath
- Chest pain when breathing or coughing
- Fatigue and muscle aches
- Nausea, vomiting, or diarrhea

**X-ray Findings:**
- Consolidation or infiltrates
- May be lobar or patchy
- Air bronchograms

**Treatment:** Depends on the cause. Bacterial pneumonia requires antibiotics. Always seek professional medical evaluation."""

    elif 'tuberculosis' in message or ' tb ' in message or message.endswith('tb'):
        return """Tuberculosis (TB) is a serious infectious disease caused by Mycobacterium tuberculosis bacteria.

**Symptoms:**
- Persistent cough lasting 3+ weeks
- Coughing up blood or mucus (hemoptysis)
- Chest pain
- Unintentional weight loss
- Fatigue and weakness
- Fever and night sweats
- Loss of appetite

**Transmission:**
- Spreads through airborne droplets
- Close contact with infected individuals
- More common in crowded, poorly ventilated areas

**X-ray Findings:**
- Upper lobe infiltrates
- Cavitation (holes in lungs)
- Hilar lymphadenopathy
- Miliary pattern in disseminated TB

**Treatment:**
- Requires long-term antibiotic therapy (6-9 months)
- Multi-drug treatment (rifampicin, isoniazid, etc.)
- Must complete full course to prevent drug resistance

**Important:** TB is curable with proper treatment. Early detection is crucial."""

    elif 'normal' in message:
        return """A "Normal" chest X-ray classification indicates no obvious signs of the lung diseases our model is trained to detect (COVID-19, Pneumonia, Tuberculosis).

**Characteristics of Normal Chest X-rays:**
- Clear lung fields without infiltrates
- Normal heart size and position
- Clear costophrenic angles
- No masses or lesions
- Normal vascular markings
- No consolidation or ground-glass opacities

**Important Notes:**
- A "Normal" prediction doesn't rule out all possible lung conditions
- Some early-stage diseases may not show on X-rays
- Other conditions not in our training data could be present
- Always correlate with clinical symptoms and history

**If you have symptoms despite a "Normal" reading:**
- Consult a healthcare professional
- Additional tests may be needed (CT scan, lab work)
- Clinical examination is essential"""

    elif 'model' in message or 'how' in message or 'work' in message:
        return """Our AI system uses a **Hybrid InceptionV3 + Vision Transformer** architecture:

**🔬 Model Architecture:**

**1. InceptionV3 (CNN Backbone):**
- Pre-trained on ImageNet
- Extracts 2048-dimensional features
- Multi-scale feature extraction through inception modules
- Captures local patterns and textures
- Input: 299×299 images

**2. Vision Transformer (ViT):**
- Pre-trained google/vit-base-patch16-224
- Extracts 768-dimensional features
- Self-attention mechanism for global context
- Captures long-range dependencies
- Input: 224×224 images (resized internally)

**3. Feature Fusion:**
- Concatenates CNN + ViT features → 2816 dimensions
- Combines local (CNN) and global (Transformer) information
- Best of both architectures

**4. Classification Head:**
- Fully connected layer
- 4 output classes (COVID-19, Normal, Pneumonia, TB)
- Softmax activation for probability distribution

**Training Details:**
- Trained on thousands of chest X-ray images
- Multiple augmentation techniques
- Achieves high accuracy on test data

**Advantages:**
- ✓ Efficient (MobileNet-based InceptionV3)
- ✓ Accurate (Transformer attention)
- ✓ Robust (Hybrid approach)
- ✓ Interpretable (Can generate Grad-CAM heatmaps)"""

    elif 'accurate' in message or 'accuracy' in message or 'performance' in message:
        return """**Model Performance Metrics:**

Our InceptionV3 + Vision Transformer hybrid model demonstrates strong performance:

**Overall Metrics:**
- Model trained on multi-class chest X-ray dataset
- Evaluated using precision, recall, F1-score, and accuracy
- Cross-validated on independent test set

**Per-Class Performance:**
The model analyzes each of the 4 classes:
- Corona Virus Disease (COVID-19)
- Normal
- Pneumonia
- Tuberculosis

**Evaluation Methods:**
- Confusion matrix analysis
- ROC-AUC scores
- Precision-Recall curves
- Classification reports

**Important Disclaimers:**
⚠️ This model is for **research and educational purposes only**
⚠️ **NOT FDA approved** or clinically validated
⚠️ **NOT a substitute** for professional medical diagnosis
⚠️ Performance may vary with different image quality and patient populations
⚠️ Should be used as a **screening tool** only, not for final diagnosis

**Clinical Use:**
- Results must be reviewed by qualified radiologists
- Should be combined with clinical symptoms and history
- May require additional testing for confirmation"""

    elif 'after diagnosis' in message or 'next steps' in message or 'what should i do' in message or 'result' in message:
        return """**What to Do After Receiving AI Results:**

**⚠️ CRITICAL: This is NOT a Medical Diagnosis**

**Immediate Steps:**

**1. Do NOT Self-Diagnose:**
- This AI tool is for research/screening only
- Not validated for clinical use
- Cannot replace medical professionals

**2. Consult Healthcare Professional:**
- Schedule appointment with a doctor immediately
- Bring the X-ray and AI results
- Discuss your symptoms and concerns
- Get professional interpretation

**3. Additional Testing May Be Needed:**
- **For suspected COVID-19**: RT-PCR test required
- **For suspected Pneumonia**: Blood tests, clinical exam
- **For suspected TB**: Sputum test, TB skin test, culture
- CT scan for detailed imaging if needed

**4. Clinical Correlation:**
- Symptoms are crucial for diagnosis
- Medical history matters
- Physical examination essential
- Lab work confirms findings

**5. Treatment:**
- Only follow treatment from licensed healthcare providers
- Do not self-medicate
- Complete prescribed treatments
- Follow up as directed

**If You Have Symptoms:**
- 🚨 **Emergency**: Severe breathing difficulty → Call emergency services
- Persistent fever → See doctor within 24-48 hours
- Mild symptoms → Schedule regular appointment

**Remember:**
- AI assists, doesn't diagnose
- X-rays alone aren't enough
- Professional medical care is essential
- Early consultation improves outcomes"""

    elif 'symptom' in message:
        return """**Common Symptoms by Lung Condition:**

**🦠 COVID-19 (Corona Virus Disease):**
- Fever or chills
- Dry cough
- Shortness of breath
- Fatigue
- Loss of taste/smell (distinctive)
- Muscle aches
- Sore throat

**🫁 Pneumonia:**
- Productive cough (phlegm/pus)
- Fever, sweating, chills
- Sharp chest pain (worse with breathing)
- Shortness of breath
- Fatigue
- Nausea/vomiting

**🔬 Tuberculosis (TB):**
- Chronic cough (3+ weeks)
- Coughing blood
- Night sweats (drenching)
- Significant weight loss
- Loss of appetite
- Chronic fatigue
- Low-grade fever

**✅ Normal/Healthy:**
- No persistent cough
- Normal breathing
- No fever
- Good energy levels
- No chest pain

**⚠️ SEEK EMERGENCY CARE IF:**
- Severe difficulty breathing
- Chest pain or pressure
- Confusion or inability to wake
- Bluish lips or face
- Coughing up blood (more than streaks)

**Important:**
- Symptoms overlap between conditions
- Some people are asymptomatic
- Only medical professionals can diagnose
- Early symptoms are often mild
- Don't ignore persistent symptoms"""

    elif 'difference' in message or 'distinguish' in message or 'tell apart' in message:
        return """**Key Differences Between Lung Conditions:**

**COVID-19 vs Pneumonia vs TB:**

**Onset & Duration:**
- **COVID-19**: Acute, 2-14 days incubation, often resolves in 2-3 weeks
- **Pneumonia**: Acute to subacute, days to weeks
- **Tuberculosis**: Chronic, develops slowly over weeks to months

**Distinctive Features:**

**COVID-19:**
- 🔍 Loss of taste/smell (very distinctive)
- Dry cough most common
- Systemic symptoms (body aches, fatigue)
- Bilateral ground-glass opacities on X-ray
- Confirmed by PCR test

**Pneumonia:**
- 🔍 Productive cough with colored sputum
- Sharp chest pain with breathing (pleuritic)
- Rapid onset of symptoms
- Consolidation on X-ray
- May follow cold/flu

**Tuberculosis:**
- 🔍 Night sweats (drenching, requiring clothing change)
- Hemoptysis (coughing blood)
- Significant weight loss
- Chronic cough (3+ weeks)
- Upper lobe cavitation on X-ray
- Confirmed by sputum test

**X-ray Patterns:**
- **COVID-19**: Bilateral, peripheral, ground-glass
- **Pneumonia**: Lobar or patchy consolidation
- **TB**: Upper lobe, cavitation, lymph nodes

**Transmission:**
- **COVID-19**: Highly contagious, airborne
- **Pneumonia**: Often not contagious (except viral types)
- **TB**: Airborne, requires prolonged exposure

**Remember:** Only healthcare professionals can accurately diagnose and differentiate these conditions!"""

    elif 'thank' in message:
        return "You're welcome! Remember, this is an educational AI tool. For medical concerns, always consult qualified healthcare professionals. Stay healthy! 🏥"

    else:
        return """I'm your AI Medical Assistant for lung disease information. I can help with:

**📚 Disease Information:**
- What is COVID-19/Pneumonia/Tuberculosis?
- Symptoms and signs
- How diseases differ from each other

**🤖 Model Information:**
- How does the AI model work?
- Model architecture (InceptionV3 + ViT)
- Accuracy and performance

**📋 After Diagnosis:**
- What should I do after getting results?
- Next steps and recommendations
- When to seek medical care

**⚠️ Important Reminders:**
- This tool is for research/education only
- NOT for clinical diagnosis
- Always consult healthcare professionals
- Results should be interpreted by doctors

**Example Questions:**
- "What are the symptoms of COVID-19?"
- "How does your model work?"
- "What should I do after diagnosis?"
- "Difference between pneumonia and tuberculosis?"

Ask me anything! I'm here to help. 😊"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
