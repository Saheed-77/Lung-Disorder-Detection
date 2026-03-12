ZZZZaaaaaaaaaaaaaaaaaa    A # 🫁 Lung Disorder Detection using Hybrid InceptionV3 + Vision Transformer (ViT)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.2-orange.svg)](https://pytorch.org/)

> **AI-powered lung disorder detection system for identifying Pneumonia, Tuberculosis, COVID-19, and Normal cases from chest X-ray images.**

![Project Banner](https://via.placeholder.com/1200x400/0284c7/ffffff?text=Lung+Disorder+Detection+AI)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 🎯 Overview

This project presents a **state-of-the-art AI diagnostic system** for detecting lung disorders from chest X-ray images. The system combines the powerful **InceptionV3** architecture for multi-scale feature extraction with the global attention capabilities of **Vision Transformers (ViT)** to achieve superior diagnostic accuracy.

### Key Highlights

- 🤖 **Hybrid AI Model**: InceptionV3 + Vision Transformer architecture (PyTorch)
- 🎯 **High Accuracy**: Production-ready detection on test datasets
- ⚡ **Fast Inference**: Results in under 2 seconds
- 📊 **Detailed Analysis**: Confidence scores and probability distributions
- 💬 **AI Chatbot**: Interactive medical Q&A assistant
- 🎨 **Modern UI**: Clean, medical-grade interface
- 📱 **Responsive Design**: Works on desktop and tablets
- 🚀 **Hugging Face Ready**: Easy deployment to Hugging Face Spaces

---

## ✨ Features

### 🏥 Diagnostic System

- **Multi-Class Detection**: Pneumonia, Tuberculosis, COVID-19, Normal
- **Image Upload**: Drag-and-drop or click to upload
- **Real-time Analysis**: Fast AI-powered prediction
- **Confidence Scoring**: Detailed probability breakdown
- **Visual Results**: Charts and visualizations
- **Report Download**: Export results as JSON

### 💬 AI Medical Assistant

- **Interactive Chatbot**: Natural language Q&A
- **Medical Information**: Disease symptoms and treatment info
- **Model Explanation**: How the AI system works
- **Suggested Questions**: Quick access to common queries
- **Conversation History**: Context-aware responses

### 🎨 User Interface

- **Landing Page**: Project overview and features
- **Diagnosis Page**: Upload and analyze X-rays
- **Chatbot Page**: AI medical assistant
- **Responsive Design**: Mobile and tablet friendly
- **Modern Animations**: Smooth transitions with Framer Motion
- **Toast Notifications**: User feedback and alerts

---

## 🏗️ Architecture

### Hybrid Model Architecture

```
Input X-Ray Image (299x299x3)
         ↓
    ┌────┴────┐
    ↓         ↓
InceptionV3   Vision Transformer
(2048-dim     (768-dim features
features)     via self-attention)
299x299       224x224 (resized)
    ↓         ↓
    └────┬────┘
         ↓
   Feature Fusion
   (2816 dimensions)
         ↓
Fully Connected Layer
         ↓
4 Classes + Confidence
(Softmax Activation)
```

### System Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │
│  React UI   │◄──────►│  FastAPI    │◄──────►│  PyTorch    │
│  (Frontend) │   REST  │  (Backend)  │  Model  │   Model     │
│             │   API   │             │  Load   │ (InceptionV3│
│             │         │             │         │   + ViT)    │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

- **React 18.2** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Router** - Navigation
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **React Dropzone** - File upload
- **React Hot Toast** - Notifications
- **Lucide React** - Icons

### Backend

- **FastAPI** - Modern Python web framework
- **PyTorch 2.1.2** - Deep learning framework
- **Transformers (Hugging Face)** - Vision Transformer models
- **Pillow (PIL)** - Image processing
- **NumPy** - Numerical computing
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI/ML

- **InceptionV3** - CNN backbone (2048-dim features)
- **Vision Transformer (ViT)** - Transformer backbone (768-dim features)
- **PyTorch/TorchVision** - Model implementation
- **Hugging Face Transformers** - Pre-trained ViT model (google/vit-base-patch16-224)
- **Feature Fusion** - Combined CNN + Transformer approach

---

## 📦 Installation

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.10+
- **pip** package manager
- **Git**

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/lung-disorder-detection.git
cd lung-disorder-detection/Ui
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
# Windows PowerShell if `python` is not on PATH:
# py -3.10 -m venv venv
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python main.py
```

On Windows, if `python` is not recognized but Python is installed, use the launcher commands instead:

```powershell
py -3.10 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

The backend API will be available at `http://localhost:8000`

### 4. Environment Variables

Create `.env` file in backend directory:

```env
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/hybrid_mobilenet_vit.h5
IMAGE_SIZE=224
```

---

## 🚀 Usage

### Running the Application

1. **Start Backend Server**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend Development Server**:
   ```bash
   npm run dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Using the Diagnostic System

1. Navigate to the **Diagnosis** page
2. Upload a chest X-ray image (PNG, JPG, JPEG, or DICOM)
3. Click **Analyze X-Ray**
4. View results:
   - Predicted condition
   - Confidence percentage
   - Probability distribution chart
5. Download report if needed

### Using the AI Chatbot

1. Navigate to the **AI Assistant** page
2. Type your question or select a suggested question
3. Receive AI-generated responses about:
   - Lung disorders and symptoms
   - Model accuracy and architecture
   - Post-diagnosis recommendations
   - General medical information

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": 1234567890.123
}
```

#### 2. Predict Disorder
```http
POST /api/predict
Content-Type: multipart/form-data
```

**Request:**
```
file: <image_file>
```

**Response:**
```json
{
  "prediction": "Pneumonia",
  "confidence": 0.94,
  "probabilities": {
    "Normal": 0.02,
    "Pneumonia": 0.94,
    "Tuberculosis": 0.03,
    "COVID-19": 0.01
  },
  "inference_time": 0.823
}
```

#### 3. Chat with AI
```http
POST /api/chat
Content-Type: application/json
```

**Request:**
```json
{
  "message": "What is pneumonia?",
  "history": []
}
```

**Response:**
```json
{
  "response": "Pneumonia is an infection that inflames..."
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧠 Model Details

### Hybrid InceptionV3 + Vision Transformer

#### InceptionV3 Component
- **Purpose**: Multi-scale feature extraction via inception modules
- **Architecture**: Efficient CNN with auxiliary classifiers
- **Features Extracted**: 2048-dimensional feature vector
- **Input Size**: 299×299 pixels
- **Advantages**: 
  - Pre-trained on ImageNet (strong transfer learning)
  - Multi-scale convolutions (1×1, 3×3, 5×5)
  - Captures local patterns and textures efficiently
  - Proven performance on medical imaging tasks

#### Vision Transformer (ViT) Component
- **Model**: google/vit-base-patch16-224-in21k (Hugging Face)
- **Purpose**: Global attention and contextual understanding
- **Architecture**: Self-attention mechanism on 16×16 image patches
- **Features Extracted**: 768-dimensional pooled output
- **Input Size**: 224×224 pixels (resized internally from 299×299)
- **Advantages**:
  - Captures long-range dependencies across entire image
  - Better understanding of spatial relationships
  - Superior performance on complex medical images
  - Attention mechanism highlights important regions

#### Fusion Strategy
- **Feature Concatenation**: InceptionV3 (2048-dim) + ViT (768-dim) = 2816-dim combined vector
- **Classification Head**: Fully connected layer with 4 output classes
- **Activation**: Softmax for probability distribution
- **Framework**: PyTorch 2.1.2

### Training Details

- **Dataset**: Chest X-ray images (COVID-19, Normal, Pneumonia, Tuberculosis)
- **Classes**: 4 disease categories
- **Image Preprocessing**: 
  - Resize to 299×299 (InceptionV3 input)
  - Normalize with ImageNet statistics
  - RGB conversion
- **Augmentation**: Multiple techniques applied during training
- **Framework**: PyTorch with Hugging Face Transformers
- **Model File**: `inceptionv3_vit_lung.pth` (~300MB)

### Model Architecture Code

```python
class MultiStageInceptionViT(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        # InceptionV3 backbone (2048 features)
        self.backbone_cnn = inception_v3(pretrained=True, aux_logits=True)
        self.backbone_cnn.fc = nn.Identity()
        
        # Vision Transformer (768 features)
        self.vit = ViTModel.from_pretrained(
            "google/vit-base-patch16-224-in21k"
        )
        
        # Classifier (2816 → 4 classes)
        self.fc = nn.Linear(2048 + 768, num_classes)
    
    def forward(self, x):
        # InceptionV3 path (299x299)
        cnn_features = self.backbone_cnn(x)
        if not torch.is_tensor(cnn_features):
            cnn_features = cnn_features.logits
        
        # ViT path (resize to 224x224)
        vit_input = F.interpolate(x, size=(224, 224))
        vit_features = self.vit(pixel_values=vit_input).pooler_output
        
        # Fusion and classification
        combined = torch.cat((cnn_features, vit_features), dim=1)
        return self.fc(combined)
```

### Model Performance

| Disease Class | Detection Capability |
|--------------|---------------------|
| COVID-19 (Corona Virus Disease) | ✓ Trained & Available |
| Normal | ✓ Trained & Available |
| Pneumonia | ✓ Trained & Available |
| Tuberculosis | ✓ Trained & Available |

**Note**: This is a production-ready model trained on real chest X-ray data. Specific performance metrics (accuracy, precision, recall) are available in the training notebook.

---

## 📁 Project Structure

```
Ui/
├── backend/
│   ├── torch_main.py               # FastAPI application (PyTorch)
│   ├── app.py                      # Hugging Face Spaces entry point
│   ├── main.py                     # Legacy TensorFlow backend (deprecated)
│   ├── model_utils.py              # Legacy model utilities (deprecated)
│   ├── test_api.py                 # API testing script
│   ├── requirements.txt            # Python dependencies (PyTorch)
│   ├── Dockerfile                  # Docker configuration for HF Spaces
│   ├── .gitattributes              # Git LFS configuration
│   ├── README_HUGGINGFACE.md       # Hugging Face deployment guide
│   ├── DEPLOYMENT_QUICK_START.md   # Quick deployment instructions
│   ├── inception/
│   │   ├── inceptionv3_vit_lung.pth        # Model weights (~300MB)
│   │   ├── class_mapping (1).json          # Class labels
│   │   └── Lung_Disease_MultistageViT_with_inceptionV3_2_0.ipynb  # Training notebook
│   └── .env.example                # Environment variables template
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx              # Navigation bar
│   │   ├── Footer.jsx              # Footer component
│   │   ├── PredictionResult.jsx    # Result display
│   │   └── ProbabilityChart.jsx    # Chart visualization
│   │
│   ├── pages/
│   │   ├── HomePage.jsx            # Landing page
│   │   ├── DiagnosisPage.jsx       # Diagnosis interface
│   │   └── ChatbotPage.jsx         # AI chatbot
│   │
│   ├── App.jsx                     # Main app component
│   ├── main.jsx                    # Entry point
│   └── index.css                   # Global styles
│
├── docs/                            # Documentation
│   ├── README.md                   # Project overview
│   ├── GETTING_STARTED.md          # Setup guide
│   ├── DEVELOPMENT.md              # Development guide
│   ├── DEPLOYMENT.md               # Deployment guide  
│   ├── API.md                      # API documentation
│   ├── PROJECT_STRUCTURE.md        # Detailed structure
│   └── PROJECT_COMPLETE.md         # Completion report
│
├── public/                          # Static assets
├── package.json                     # Node dependencies
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS config
├── postcss.config.js                # PostCSS config
└── README.md                        # This file (main documentation)
```

---

## 📸 Screenshots

### Home Page
![Home Page](https://via.placeholder.com/800x500/0284c7/ffffff?text=Home+Page)

### Diagnosis Page
![Diagnosis](https://via.placeholder.com/800x500/0284c7/ffffff?text=Diagnosis+Page)

### AI Chatbot
![Chatbot](https://via.placeholder.com/800x500/0284c7/ffffff?text=AI+Chatbot)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

**IMPORTANT MEDICAL DISCLAIMER**

This application is developed for **research and educational purposes only**. It is **NOT** intended for actual medical diagnosis or clinical use.

- ❌ **NOT a medical device**
- ❌ **NOT a substitute for professional medical advice**
- ❌ **NOT validated for clinical use**
- ✅ **For research and demonstration only**

**Always consult qualified healthcare professionals for medical diagnosis and treatment.**

The developers and contributors are not responsible for any medical decisions or outcomes based on the use of this tool.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGithub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- TensorFlow and Keras teams for deep learning frameworks
- React and FastAPI communities
- Medical imaging datasets providers
- Open-source contributors

---

## 📧 Contact

For questions, suggestions, or collaborations:

- **Email**: research@lungai.com
- **GitHub**: [Create an Issue](https://github.com/yourusername/lung-disorder-detection/issues)
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for medical AI research

</div>
