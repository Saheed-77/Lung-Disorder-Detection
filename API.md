# API Reference Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

Currently, the API does not require authentication. For production deployment, implement JWT or API key authentication.

---

## Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Request:**
```http
GET /
```

**Response:**
```json
{
  "message": "Lung Disorder Detection API",
  "version": "1.0.0",
  "status": "online",
  "endpoints": {
    "predict": "/api/predict",
    "chat": "/api/chat",
    "health": "/api/health"
  }
}
```

---

### 2. Health Check

Check API and model status.

**Request:**
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

**Status Codes:**
- `200 OK` - Service is healthy

---

### 3. Predict Lung Disorder

Upload a chest X-ray image and get AI prediction.

**Request:**
```http
POST /api/predict
Content-Type: multipart/form-data
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | Chest X-ray image (PNG, JPG, JPEG, DICOM) |

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@chest_xray.jpg"
```

**Example (JavaScript/Axios):**
```javascript
const formData = new FormData()
formData.append('file', fileObject)

const response = await axios.post('/api/predict', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})
```

**Response:**
```json
{
  "prediction": "Pneumonia",
  "confidence": 0.9432,
  "probabilities": {
    "Normal": 0.0234,
    "Pneumonia": 0.9432,
    "Tuberculosis": 0.0189,
    "COVID-19": 0.0145
  },
  "inference_time": 0.823
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| prediction | string | Predicted disease class |
| confidence | float | Confidence score (0-1) for predicted class |
| probabilities | object | Probability scores for all classes |
| inference_time | float | Model inference time in seconds |

**Status Codes:**
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid file type or format
- `500 Internal Server Error` - Prediction failed

**Error Response:**
```json
{
  "detail": "File must be an image"
}
```

---

### 4. Chat with AI

Send a message to the AI medical assistant.

**Request:**
```http
POST /api/chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What is pneumonia?",
  "history": [
    {
      "id": 1,
      "type": "user",
      "text": "Hello",
      "timestamp": "2024-02-26T10:00:00Z"
    },
    {
      "id": 2,
      "type": "bot",
      "text": "Hello! How can I help?",
      "timestamp": "2024-02-26T10:00:01Z"
    }
  ]
}
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| message | string | Yes | User's question or message |
| history | array | No | Conversation history for context |

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is pneumonia?", "history": []}'
```

**Example (JavaScript/Axios):**
```javascript
const response = await axios.post('/api/chat', {
  message: 'What is pneumonia?',
  history: []
})
```

**Response:**
```json
{
  "response": "Pneumonia is an infection that inflames the air sacs in one or both lungs..."
}
```

**Status Codes:**
- `200 OK` - Response generated successfully
- `500 Internal Server Error` - Chat processing failed

---

## Data Models

### PredictionResponse

```typescript
interface PredictionResponse {
  prediction: 'Normal' | 'Pneumonia' | 'Tuberculosis' | 'COVID-19'
  confidence: number  // 0-1
  probabilities: {
    Normal: number
    Pneumonia: number
    Tuberculosis: number
    'COVID-19': number
  }
  inference_time: number  // seconds
}
```

### ChatRequest

```typescript
interface ChatRequest {
  message: string
  history?: Array<{
    id: number
    type: 'user' | 'bot'
    text: string
    timestamp: string
  }>
}
```

### ChatResponse

```typescript
interface ChatResponse {
  response: string
}
```

---

## Rate Limiting

**Current:** No rate limiting implemented

**Recommended for Production:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

Implementation example:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/predict")
@limiter.limit("10/minute")
async def predict(request: Request, file: UploadFile):
    # ... implementation
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 400 | Bad Request | Invalid file type, missing parameters |
| 413 | Payload Too Large | File size exceeds limit (10MB) |
| 422 | Unprocessable Entity | Invalid JSON or data format |
| 500 | Internal Server Error | Model error, server issue |
| 503 | Service Unavailable | Model not loaded |

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

### Swagger UI
```
http://localhost:8000/docs
```
- Interactive API testing
- Request/response examples
- Schema definitions

### ReDoc
```
http://localhost:8000/redoc
```
- Alternative documentation view
- Better for reading
- Cleaner interface

---

## Code Examples

### Python (requests)

```python
import requests

# Predict
with open('xray.jpg', 'rb') as f:
    files = {'file': ('xray.jpg', f, 'image/jpeg')}
    response = requests.post(
        'http://localhost:8000/api/predict',
        files=files
    )
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")

# Chat
chat_response = requests.post(
    'http://localhost:8000/api/chat',
    json={
        'message': 'What is pneumonia?',
        'history': []
    }
)
print(chat_response.json()['response'])
```

### JavaScript (fetch)

```javascript
// Predict
const predictDisorder = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    body: formData
  })

  const result = await response.json()
  console.log('Prediction:', result.prediction)
  console.log('Confidence:', result.confidence)
  return result
}

// Chat
const chatWithAI = async (message) => {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      history: []
    })
  })

  const result = await response.json()
  console.log('Response:', result.response)
  return result
}
```

### cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Predict
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/xray.jpg"

# Chat
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is pneumonia?","history":[]}'
```

---

## Versioning

Current API version: `v1`

Future versions will be prefixed:
```
/api/v2/predict
/api/v2/chat
```

---

## CORS Configuration

Allowed origins for cross-origin requests:
- `http://localhost:3000` (Development)
- `http://localhost:5173` (Vite)

To add custom origins, modify `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Best Practices

1. **Always validate file size before upload** (max 10MB)
2. **Handle errors gracefully** with try-catch blocks
3. **Use proper content types** for requests
4. **Implement retry logic** for network failures
5. **Cache predictions** when appropriate
6. **Log all API calls** for debugging
7. **Implement timeouts** for long-running requests

---

## Support

For API issues or questions:
- GitHub Issues: https://github.com/yourusername/repo/issues
- Email: api-support@lungai.com
- Documentation: /docs endpoint
