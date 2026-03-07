# 🫁 Lung Disease Detection API - InceptionV3 + Vision Transformer

AI-powered chest X-ray analysis for detecting lung disorders: COVID-19, Normal, Pneumonia, and Tuberculosis.

## 🔬 Model Architecture

**Hybrid InceptionV3 + Vision Transformer (ViT)**

- **InceptionV3 Backbone**: Extracts 2048-dimensional CNN features from 299×299 images
- **Vision Transformer**: Extracts 768-dimensional transformer features from 224×224 images  
- **Feature Fusion**: Concatenates both feature vectors (2816 dimensions total)
- **Classification**: Fully connected layer for 4-class prediction

### Model Specifications

- **Framework**: PyTorch 2.1.2
- **Input Size**: 299×299 RGB images
- **Normalization**: ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Output Classes**: 4 disease categories
  - Corona Virus Disease (COVID-19)
  - Normal
  - Pneumonia  
  - Tuberculosis

## 🚀 API Endpoints

### **POST /api/predict**
Upload a chest X-ray image for disease prediction.

**Request**:
- Content-Type: `multipart/form-data`
- Body: `file` (image file: PNG, JPG, JPEG)

**Response**:
```json
{
  "prediction": "Normal",
  "confidence": 0.95,
  "probabilities": {
    "Corona Virus Disease": 0.02,
    "Normal": 0.95,
    "Pneumonia": 0.02,
    "Tuberculosis": 0.01
  },
  "inference_time": 0.234,
  "model": "InceptionV3 + ViT"
}
```

### **POST /api/chat**
AI medical chatbot for disease information.

**Request**:
```json
{
  "message": "What is COVID-19?",
  "history": []
}
```

**Response**:
```json
{
  "response": "COVID-19 (Corona Virus Disease) is..."
}
```

### **GET /api/health**
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "model_type": "InceptionV3 + ViT",
  "num_classes": 4,
  "timestamp": 1234567890.123
}
```

## 📦 Deployment on Hugging Face Spaces

### Prerequisites

1. Hugging Face account
2. Git LFS installed (for model files)

### Deployment Steps

#### 1. Create a New Space

- Go to [Hugging Face Spaces](https://huggingface.co/spaces)
- Click "Create new Space"
- Choose:
  - **Space name**: lung-disease-detection
  - **SDK**: Docker
  - **License**: MIT (or your choice)
  - **Visibility**: Public or Private

#### 2. Prepare Files

Upload the following files to your Space:

```
backend/
├── app.py                       # Hugging Face entry point
├── torch_main.py                # Main FastAPI application
├── requirements.txt             # Python dependencies
├── inception/
│   ├── inceptionv3_vit_lung.pth    # Model weights (~300MB)
│   └── class_mapping (1).json      # Class labels
└── Dockerfile                   # (Optional) Custom Docker config
```

#### 3. Create Dockerfile (Optional)

If you need custom Docker configuration:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend/ .

# Expose port
EXPOSE 7860

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### 4. Upload Model File with Git LFS

```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/lung-disease-detection
cd lung-disease-detection

# Track large files with Git LFS
git lfs install
git lfs track "*.pth"
git add .gitattributes

# Add files
cp -r /path/to/backend/* .
git add .

# Commit and push
git commit -m "Initial commit: InceptionV3 + ViT model"
git push
```

#### 5. Configure Space Settings

In your Space settings:
- **Hardware**: CPU Basic (free) or GPU (paid)
- **Environment Variables**: None required for basic setup
- **Secrets**: Add if using external APIs

#### 6. Access Your API

Once deployed, your API will be available at:
```
https://YOUR_USERNAME-lung-disease-detection.hf.space
```

Test endpoints:
- Main: `https://YOUR_USERNAME-lung-disease-detection.hf.space/`
- Health: `https://YOUR_USERNAME-lung-disease-detection.hf.space/api/health`
- Predict: `https://YOUR_USERNAME-lung-disease-detection.hf.space/api/predict`

## 🧪 Testing Locally

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run server (port 8000)
python torch_main.py

# Or use uvicorn
uvicorn torch_main:app --reload --host 0.0.0.0 --port 8000

# For Hugging Face Spaces (port 7860)
python app.py
```

### Test with cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Prediction
curl -X POST http://localhost:8000/api/predict \
  -F "file=@path/to/xray.jpg"

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is COVID-19?", "history": []}'
```

### Test with Python

```python
import requests

# Prediction
url = "http://localhost:8000/api/predict"
files = {"file": open("xray.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())

# Chat
chat_url = "http://localhost:8000/api/chat"
data = {"message": "What are the symptoms of pneumonia?", "history": []}
response = requests.post(chat_url, json=data)
print(response.json())
```

## 📊 Model Performance

- **Training Dataset**: Multi-class chest X-ray dataset with 4 categories
- **Architecture**: Hybrid CNN (InceptionV3) + Transformer (ViT) approach
- **Input Resolution**: 299×299 for InceptionV3, internally resized to 224×224 for ViT
- **Feature Extraction**: 
  - Local features via InceptionV3 (2048-dim)
  - Global context via Vision Transformer (768-dim)
- **Classification**: Combined 2816-dimensional feature vector

## ⚠️ Important Disclaimers

- **NOT FOR CLINICAL USE**: This model is for research and educational purposes only
- **NOT FDA APPROVED**: Not validated for clinical diagnosis
- **REQUIRES PROFESSIONAL REVIEW**: Results must be interpreted by qualified radiologists
- **NO MEDICAL DECISIONS**: Do not make treatment decisions based solely on this tool
- **SUPPLEMENTARY TOOL**: Should be used alongside clinical examination and other diagnostic methods

## 🔒 Privacy & Security

- **No Data Storage**: Images are processed in memory and not saved
- **No User Tracking**: No personal information collected
- **HIPAA Compliance**: This deployment is NOT HIPAA-compliant in its current form
- **For Educational Use**: Intended for research and learning only

## 📄 License

See LICENSE file for model and code licensing information.

## 🤝 Contributing

For issues or contributions related to this model deployment, please open an issue on the GitHub repository.

## 📚 Citation

If you use this model in your research, please cite appropriately and acknowledge that it's for educational purposes only.

## 🔗 Links

- **Frontend Application**: [GitHub Repository]
- **Model Training Notebook**: See `Lung_Disease_MultistageViT_with_inceptionV3_2_0.ipynb`
- **Documentation**: Full project documentation in repository

---

**Version**: 2.0.0  
**Last Updated**: 2024  
**Model Framework**: PyTorch 2.1.2  
**API Framework**: FastAPI 0.109.0
