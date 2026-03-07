# Hugging Face Spaces Quick Deployment Guide

## 🚀 Quick Deploy to Hugging Face Spaces

### Option 1: Web Interface (Easiest)

1. **Create Space**:
   - Go to https://huggingface.co/new-space
   - Name: `lung-disease-detection`
   - SDK: **Docker**
   - Visibility: Public or Private

2. **Upload Files**:
   - Upload all files from the `backend/` folder:
     - `app.py`
     - `torch_main.py`
     - `requirements.txt`
     - `Dockerfile`
     - `.gitattributes`
     - `inception/inceptionv3_vit_lung.pth` (use Git LFS for this large file)
     - `inception/class_mapping (1).json`

3. **Wait for Build**:
   - Hugging Face will automatically build and deploy
   - Check logs for any errors
   - Usually takes 5-10 minutes

4. **Access API**:
   - URL: `https://YOUR_USERNAME-lung-disease-detection.hf.space`
   - Test: `https://YOUR_USERNAME-lung-disease-detection.hf.space/api/health`

### Option 2: Git Command Line

```bash
# 1. Install Git LFS
git lfs install

# 2. Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/lung-disease-detection
cd lung-disease-detection

# 3. Copy backend files
cp -r /path/to/backend/* .

# 4. Track large files
git lfs track "*.pth"
git add .gitattributes

# 5. Add all files
git add .

# 6. Commit and push
git commit -m "Deploy InceptionV3 + ViT lung disease detection model"
git push
```

### Option 3: Using Hugging Face CLI

```bash
# 1. Install Hugging Face CLI
pip install huggingface_hub

# 2. Login
huggingface-cli login

# 3. Create space
huggingface-cli repo create lung-disease-detection --type space --space_sdk docker

# 4. Clone and add files
git clone https://huggingface.co/spaces/YOUR_USERNAME/lung-disease-detection
cd lung-disease-detection

# 5. Copy backend files
cp -r /path/to/backend/* .

# 6. Push with LFS
git lfs install
git lfs track "*.pth"
git add .
git commit -m "Initial deployment"
git push
```

## 📋 Pre-Deployment Checklist

- [ ] Model file (`inceptionv3_vit_lung.pth`) is present in `backend/inception/`
- [ ] Class mapping file (`class_mapping (1).json`) is present
- [ ] `requirements.txt` has all PyTorch dependencies
- [ ] `app.py` is configured for port 7860
- [ ] `.gitattributes` configured for Git LFS
- [ ] Model file size is tracked with Git LFS (files > 100MB must use LFS)

## 🧪 Test Locally First

Before deploying, test locally:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860/` and test:
- Health check: `/api/health`
- Prediction: `/api/predict` (upload X-ray image)
- Chat: `/api/chat` (ask medical questions)

## 🔧 Troubleshooting

### Build Fails

**Error**: "Model file too large"
- **Solution**: Ensure Git LFS is configured and model is tracked

**Error**: "Module not found"
- **Solution**: Check `requirements.txt` has all dependencies

**Error**: "CUDA not available"
- **Solution**: Model runs on CPU by default. For GPU, upgrade Space to GPU tier.

### Model Not Loading

**Error**: "Model not found"
- **Solution**: Check file path matches: `backend/inception/inceptionv3_vit_lung.pth`

**Error**: "Key mismatch in state dict"
- **Solution**: Ensure model architecture matches training code

### API Not Responding

**Error**: "Connection timeout"
- **Solution**: Check Dockerfile exposes port 7860
- **Solution**: Verify `app.py` runs `uvicorn` on correct port

## 📊 Performance Tips

### Speed Up Inference
- **Use CPU Basic**: Free tier, ~2-5 seconds per prediction
- **Upgrade to GPU**: Paid tier, ~0.5-1 second per prediction

### Optimize Memory
```python
# In torch_main.py, add these optimizations:
torch.set_grad_enabled(False)  # Disable gradients
model.eval()  # Set to evaluation mode
torch.backends.cudnn.benchmark = True  # For GPU
```

### Reduce Cold Starts
- Keep Space awake with periodic health checks
- Use Hugging Face's "Keep Space Running" option

## 🔐 Security Best Practices

1. **Don't commit secrets**: Use Hugging Face Secrets for API keys
2. **Rate limiting**: Add rate limiting to prevent abuse
3. **Input validation**: Model validates file types and sizes
4. **CORS**: Configured to allow frontend access

## 📞 Support

If deployment fails:
1. Check Hugging Face Space logs
2. Review Dockerfile build output
3. Test locally first
4. Check model file integrity

## 🌐 Example Spaces

Browse similar medical AI models on Hugging Face Spaces for inspiration:
- Search for "chest xray" or "medical imaging"
- Look at successful deployments
- Check their configuration

---

**Ready to Deploy?** Follow Option 1 (Web Interface) for the quickest deployment!

Good luck! 🚀
