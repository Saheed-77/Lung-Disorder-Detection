# Development Guide

## Table of Contents
- [Setup Development Environment](#setup-development-environment)
- [Running in Development Mode](#running-in-development-mode)
- [Building for Production](#building-for-production)
- [Code Structure](#code-structure)
- [Adding New Features](#adding-new-features)
- [Model Training](#model-training)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Setup Development Environment

### Prerequisites Check

```bash
# Check Node.js version (should be 18+)
node --version

# Check npm version
npm --version

# Check Python version (should be 3.10+)
python --version

# Check pip
pip --version
```

### IDE Setup

**Recommended Extensions for VS Code:**

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- Python
- Pylance

### Environment Setup

1. **Frontend Environment**:
   ```bash
   npm install
   ```

2. **Backend Environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

---

## Running in Development Mode

### Frontend Development Server

```bash
# Start Vite dev server with hot reload
npm run dev

# Access at http://localhost:3000
```

Features:
- Hot Module Replacement (HMR)
- Fast refresh
- Source maps for debugging
- Automatic browser reload

### Backend Development Server

```bash
cd backend
python main.py

# Or with auto-reload:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Features:
- Auto-reload on code changes
- Interactive API docs at `/docs`
- Request logging
- Error tracebacks

### Running Both Simultaneously

**Option 1: Two Terminal Windows**
```bash
# Terminal 1
npm run dev

# Terminal 2
cd backend && python main.py
```

**Option 2: Using concurrently (package.json script)**
```bash
npm run dev:all
```

---

## Building for Production

### Frontend Build

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

Output location: `dist/` directory

### Backend Deployment

1. **Install production dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with production server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Using Docker** (optional):
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

---

## Code Structure

### Frontend Component Pattern

```jsx
// Component Template
import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

const ComponentName = ({ props }) => {
  const [state, setState] = useState(initialValue)

  useEffect(() => {
    // Side effects
  }, [dependencies])

  const handleAction = () => {
    // Action handler
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="component-styles"
    >
      {/* Component JSX */}
    </motion.div>
  )
}

export default ComponentName
```

### Backend Route Pattern

```python
# Route Template
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class RequestModel(BaseModel):
    field: str

@router.post("/endpoint")
async def endpoint_handler(data: RequestModel):
    try:
        # Processing logic
        result = process_data(data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Adding New Features

### Adding a New Frontend Page

1. **Create page component**:
   ```jsx
   // src/pages/NewPage.jsx
   import React from 'react'
   
   const NewPage = () => {
     return (
       <div className="container">
         <h1>New Page</h1>
       </div>
     )
   }
   
   export default NewPage
   ```

2. **Add route**:
   ```jsx
   // src/App.jsx
   import NewPage from './pages/NewPage'
   
   <Route path="/new-page" element={<NewPage />} />
   ```

3. **Add navigation link**:
   ```jsx
   // src/components/Navbar.jsx
   { name: 'New Page', path: '/new-page' }
   ```

### Adding a New Backend Endpoint

1. **Define route in main.py**:
   ```python
   @app.post("/api/new-endpoint")
   async def new_endpoint(data: DataModel):
       # Logic here
       return {"result": "success"}
   ```

2. **Add frontend API call**:
   ```javascript
   // Frontend component
   const response = await axios.post('/api/new-endpoint', data)
   ```

---

## Model Training

### Preparing Dataset

```python
# Dataset structure
dataset/
├── train/
│   ├── Normal/
│   ├── Pneumonia/
│   ├── Tuberculosis/
│   └── COVID-19/
├── validation/
└── test/
```

### Training Script

```python
from model_utils import create_hybrid_model, compile_model, get_callbacks

# Create model
model = create_hybrid_model(
    input_shape=(224, 224, 3),
    num_classes=4
)

# Compile
model = compile_model(model, learning_rate=0.001)

# Prepare data (implement your data pipeline)
train_dataset = prepare_dataset('dataset/train')
val_dataset = prepare_dataset('dataset/validation')

# Train
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=50,
    callbacks=get_callbacks('models/best_model.h5')
)

# Save final model
model.save('models/hybrid_mobilenet_vit.h5')
```

### Loading Trained Model

```python
# In backend/main.py
import tensorflow as tf

def load_model():
    global model
    model = tf.keras.models.load_model('models/hybrid_mobilenet_vit.h5')
    return model
```

---

## Testing

### Frontend Testing

```bash
# Run tests (if configured)
npm test

# Linting
npm run lint
```

### Backend Testing

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/api/predict",
            files={"file": ("test.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "prediction" in response.json()
```

Run tests:
```bash
pytest test_api.py -v
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Frontend (Port 3000)**:
```bash
# Find process
netstat -ano | findstr :3000  # Windows
lsof -i :3000  # Linux/Mac

# Kill process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # Linux/Mac
```

**Backend (Port 8000)**:
```bash
# Similar process as above for port 8000
```

#### 2. Module Not Found

**Frontend**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Backend**:
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 3. CORS Errors

Update CORS origins in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Model Loading Errors

- Ensure model file exists at specified path
- Check TensorFlow version compatibility
- Verify model architecture matches saved model

#### 5. Image Upload Issues

- Check file size limits (default 10MB)
- Verify image format support
- Check server file upload configuration

### Getting Help

If issues persist:
1. Check the [GitHub Issues](https://github.com/yourusername/repo/issues)
2. Review FastAPI documentation
3. Check React/Vite documentation
4. Search Stack Overflow

---

## Performance Optimization

### Frontend

1. **Code Splitting**:
   ```javascript
   const LazyComponent = React.lazy(() => import('./Component'))
   ```

2. **Image Optimization**:
   - Use WebP format
   - Implement lazy loading
   - Compress images

3. **Bundle Size**:
   ```bash
   # Analyze bundle
   npm run build -- --analyze
   ```

### Backend

1. **Async Operations**:
   ```python
   async def process_image(image):
       # Use async/await for I/O operations
       result = await async_model_predict(image)
       return result
   ```

2. **Caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_prediction(image_hash):
       return model.predict(image)
   ```

3. **Connection Pooling**:
   - Use proper database connections
   - Configure worker processes
   - Implement request queuing

---

## Deployment Checklist

- [ ] Update environment variables
- [ ] Test production build locally
- [ ] Optimize bundle size
- [ ] Enable compression (gzip)
- [ ] Set up SSL certificates
- [ ] Configure CORS properly
- [ ] Set up logging and monitoring
- [ ] Implement rate limiting
- [ ] Add health check endpoints
- [ ] Test on target deployment platform
- [ ] Document deployment process
- [ ] Set up CI/CD pipeline

---

## Resources

- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Vite Documentation](https://vitejs.dev/)

---

**Happy Coding! 🚀**
