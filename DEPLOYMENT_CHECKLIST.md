# 📋 Deployment Checklist - Hugging Face Spaces

## Pre-Deployment Verification

### ✅ Backend Files Present

- [x] `backend/app.py` - Hugging Face entry point
- [x] `backend/torch_main.py` - Main FastAPI application
- [x] `backend/requirements.txt` - PyTorch dependencies
- [x] `backend/Dockerfile` - Container configuration
- [x] `backend/.gitattributes` - Git LFS setup
- [x] `backend/test_api.py` - Testing script
- [x] `backend/inception/inceptionv3_vit_lung.pth` - Model weights (~300MB)
- [x] `backend/inception/class_mapping (1).json` - Class labels

### ✅ Model Architecture Verified

```python
MultiStageInceptionViT:
  ├── InceptionV3 backbone
  │   ├── Input: 299×299 RGB
  │   ├── Output: 2048-dim features
  │   └── Pretrained: ImageNet
  │
  ├── Vision Transformer (ViT)
  │   ├── Model: google/vit-base-patch16-224
  │   ├── Input: 224×224 (resized from 299×299)
  │   ├── Output: 768-dim features
  │   └── Pretrained: Hugging Face
  │
  └── Classification Head
      ├── Input: 2816-dim (2048 + 768)
      ├── Output: 4 classes
      └── Activation: Softmax
```

### ✅ Classes Configured

```json
{
  "Corona Virus Disease": 0,
  "Normal": 1,
  "Pneumonia": 2,
  "Tuberculosis": 3
}
```

---

## Local Testing Checklist

### Step 1: Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully

### Step 2: Run Backend
```powershell
python torch_main.py
```

**Expected output**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Using device: cpu
INFO:     Classes loaded: {'Corona Virus Disease': 0, 'Normal': 1, ...}
INFO:     Model loaded successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test Health Check
```powershell
# In a new terminal
curl http://localhost:8000/api/health
```

**Expected response**:
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

### Step 4: Test Root Endpoint
```powershell
curl http://localhost:8000/
```

**Expected response**:
```json
{
  "message": "Lung Disease Detection API - InceptionV3 + ViT",
  "version": "2.0.0",
  "model": "InceptionV3 + Vision Transformer",
  "status": "online",
  "classes": ["Corona Virus Disease", "Normal", "Pneumonia", "Tuberculosis"],
  "endpoints": {...}
}
```

### Step 5: Test Chat Endpoint
```powershell
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"What is COVID-19?\", \"history\": []}'
```

**Expected response**: JSON with medical information about COVID-19

### Step 6: Test Prediction (Optional - Requires X-ray image)
```powershell
curl -X POST http://localhost:8000/api/predict `
  -F "file=@path\to\xray.jpg"
```

**Expected response**:
```json
{
  "prediction": "Normal",
  "confidence": 0.92,
  "probabilities": {...},
  "inference_time": 0.345,
  "model": "InceptionV3 + ViT"
}
```

### Step 7: Run Test Suite
```powershell
python test_api.py
```

**Expected output**:
```
╔══════════════════════════════════════════════════════╗
║               API TEST SUITE                         ║
║          Lung Disease Detection API                  ║
╚══════════════════════════════════════════════════════╝

Testing Health Check Endpoint
✓ Health check passed!

Testing Root Endpoint
✓ Root endpoint working!

Testing Chat Endpoint
✓ Response received (500+ chars)

TEST SUMMARY
HEALTH         : ✓ PASSED
ROOT           : ✓ PASSED
CHAT           : ✓ PASSED
PREDICTION     : ⊘ SKIPPED (no image provided)

✅ All tests passed! Backend is ready for deployment.
```

---

## Hugging Face Deployment Checklist

### Option 1: Web Interface (Recommended)

#### ☐ Step 1: Create Space
1. Go to https://huggingface.co/new-space
2. Fill in details:
   - **Name**: `lung-disease-detection` (or your choice)
   - **License**: MIT (recommended)
   - **SDK**: **Docker** ⚠️ Important!
   - **Visibility**: Public or Private
3. Click "Create Space"

#### ☐ Step 2: Upload Files
Upload all files from `backend/` directory:

**Required Files** (must upload):
- [ ] `app.py`
- [ ] `torch_main.py`
- [ ] `requirements.txt`
- [ ] `Dockerfile`
- [ ] `.gitattributes`
- [ ] `inception/inceptionv3_vit_lung.pth` (300MB - may take time)
- [ ] `inception/class_mapping (1).json`

**Optional Files** (helpful but not required):
- [ ] `README_HUGGINGFACE.md` (shows as Space README)
- [ ] `test_api.py` (for debugging)

#### ☐ Step 3: Monitor Build
1. Check "Logs" tab in your Space
2. Wait for build to complete (5-10 minutes)
3. Look for success message: "Running on http://0.0.0.0:7860"

#### ☐ Step 4: Test Deployment
```python
import requests

BASE_URL = "https://YOUR_USERNAME-lung-disease-detection.hf.space"

# Health check
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())
```

**Expected**: `{"status": "healthy", "model_loaded": true, ...}`

---

### Option 2: Git CLI

#### ☐ Step 1: Install Git LFS
```bash
git lfs install
```

#### ☐ Step 2: Clone Space
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/lung-disease-detection
cd lung-disease-detection
```

#### ☐ Step 3: Configure LFS
```bash
git lfs track "*.pth"
git add .gitattributes
```

#### ☐ Step 4: Copy Files
```bash
# Copy all backend files
cp -r /path/to/backend/* .

# Or on Windows PowerShell
Copy-Item -Recurse c:\Users\DELL\Documents\Main-Project\project\Ui\backend\* .
```

#### ☐ Step 5: Commit and Push
```bash
git add .
git commit -m "Deploy InceptionV3 + ViT lung disease detection model"
git push
```

#### ☐ Step 6: Monitor Logs
- Go to your Space on Hugging Face
- Check "Logs" tab for build progress

---

## Post-Deployment Verification

### ☐ Test All Endpoints

#### 1. Root Endpoint
```bash
curl https://YOUR_USERNAME-lung-disease-detection.hf.space/
```
**Expected**: JSON with API info

#### 2. Health Check
```bash
curl https://YOUR_USERNAME-lung-disease-detection.hf.space/api/health
```
**Expected**: `{"status": "healthy", "model_loaded": true, ...}`

#### 3. Chat Endpoint
```python
import requests

url = "https://YOUR_USERNAME-lung-disease-detection.hf.space/api/chat"
data = {"message": "What is pneumonia?", "history": []}
response = requests.post(url, json=data)
print(response.json())
```
**Expected**: Medical information response

#### 4. Prediction Endpoint
```python
import requests

url = "https://YOUR_USERNAME-lung-disease-detection.hf.space/api/predict"
files = {"file": open("xray.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```
**Expected**: Prediction with probabilities

---

## Frontend Integration Checklist

### ☐ Update API URL in Frontend

#### Location 1: `src/pages/DiagnosisPage.jsx`
Find and update:
```javascript
const API_URL = "https://YOUR_USERNAME-lung-disease-detection.hf.space";
```

#### Location 2: `src/pages/ChatbotPage.jsx`
Find and update:
```javascript
const API_URL = "https://YOUR_USERNAME-lung-disease-detection.hf.space";
```

### ☐ Test Frontend with Deployed Backend

1. **Start Frontend**:
   ```powershell
   npm run dev
   ```

2. **Test Diagnosis Page**:
   - Upload a chest X-ray image
   - Verify prediction appears
   - Check confidence scores
   - Verify chart displays correctly

3. **Test Chatbot Page**:
   - Ask: "What is COVID-19?"
   - Ask: "Symptoms of pneumonia?"
   - Ask: "How does your model work?"
   - Verify responses are detailed and accurate

---

## Troubleshooting Guide

### ❌ Build Fails: "Model file too large"
**Solution**: Ensure Git LFS is configured
```bash
git lfs track "*.pth"
git add .gitattributes
```

### ❌ Runtime Error: "Module not found"
**Solution**: Check `requirements.txt` has all dependencies
```txt
torch==2.1.2
torchvision==0.16.2
transformers==4.36.2
```

### ❌ Prediction Error: "Model not loaded"
**Solution**: 
1. Check logs for model loading errors
2. Verify file path: `backend/inception/inceptionv3_vit_lung.pth`
3. Ensure file uploaded correctly (check file size)

### ❌ CORS Error in Frontend
**Solution**: Backend has CORS enabled for all origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    ...
)
```

### ❌ Slow Inference (~10s per image)
**Solution**: Upgrade Space to GPU
- Go to Space Settings
- Change Hardware: CPU Basic → GPU
- Accept billing (GPU is paid)
- **Expected speed**: 0.5-1s per image (vs 2-5s on CPU)

---

## Performance Optimization

### Recommended Settings

| Setting | Free (CPU) | Paid (GPU) |
|---------|-----------|-----------|
| **Hardware** | CPU Basic | T4 Small |
| **Inference Time** | 2-5 seconds | 0.5-1 second |
| **Cost** | Free | ~$0.60/hour |
| **Best For** | Development, Testing | Production |

### Keep Space Active
- Spaces sleep after inactivity
- First request after sleep takes longer (cold start)
- Solution: Periodic health checks or upgrade to persistent

---

## Success Criteria

✅ **Backend Deployed**: Space shows "Running"
✅ **Health Check Passes**: `/api/health` returns healthy status
✅ **Model Loads**: Logs show "Model loaded successfully!"
✅ **Chat Works**: Returns medical information
✅ **Prediction Works**: Returns class probabilities
✅ **Frontend Connected**: Can make predictions from UI
✅ **No CORS Errors**: Frontend can communicate with backend

---

## 📚 Additional Resources

- **Full Deployment Guide**: `backend/README_HUGGINGFACE.md`
- **Quick Start**: `backend/DEPLOYMENT_QUICK_START.md`
- **API Documentation**: `docs/API.md`
- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces

---

## 🎉 Congratulations!

Once all checklist items are complete, your AI lung disease detection system is live!

**Next Steps**:
1. Share your Hugging Face Space URL
2. Test with real chest X-ray images
3. Monitor performance and logs
4. Consider upgrading to GPU for faster inference

**Your Space URL**:
```
https://YOUR_USERNAME-lung-disease-detection.hf.space
```

Good luck! 🚀
