# Project Structure Overview

```
Ui/
│
├── 📄 Configuration Files
│   ├── package.json              # Node.js dependencies and scripts
│   ├── vite.config.js            # Vite build configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   ├── postcss.config.js         # PostCSS configuration
│   ├── jsconfig.json             # JavaScript configuration
│   ├── .eslintrc.json            # ESLint rules
│   └── .gitignore                # Git ignore patterns
│
├── 📄 Entry Point
│   ├── index.html                # HTML entry point
│   └── src/
│       ├── main.jsx              # JavaScript entry point
│       ├── App.jsx               # Main App component with routing
│       └── index.css             # Global styles and Tailwind imports
│
├── 🎨 Frontend Components
│   └── src/
│       ├── components/
│       │   ├── Navbar.jsx                # Navigation bar with responsive menu
│       │   ├── Footer.jsx                # Footer with links and disclaimer
│       │   ├── PredictionResult.jsx      # Display prediction results
│       │   └── ProbabilityChart.jsx      # Chart for probabilities
│       │
│       └── pages/
│           ├── HomePage.jsx              # Landing page with project info
│           ├── DiagnosisPage.jsx         # X-ray upload and analysis
│           └── ChatbotPage.jsx           # AI medical assistant
│
├── ⚙️ Backend API
│   └── backend/
│       ├── main.py                       # FastAPI application and routes
│       ├── model_utils.py                # Model architecture and training
│       ├── requirements.txt              # Python dependencies
│       └── .env.example                  # Environment variables template
│
├── 📚 Documentation
│   ├── README.md                         # Main documentation
│   ├── DEVELOPMENT.md                    # Development guide
│   ├── API.md                            # API reference
│   ├── DEPLOYMENT.md                     # Deployment guide
│   └── PROJECT_STRUCTURE.md              # This file
│
└── 🚀 Scripts
    ├── setup.ps1                         # Windows setup script
    └── setup.sh                          # Linux/Mac setup script
```

---

## File Descriptions

### Configuration Files

#### package.json
Contains all frontend dependencies including:
- React and React Router for UI
- Tailwind CSS for styling
- Framer Motion for animations
- Recharts for data visualization
- Axios for API calls
- React Dropzone for file uploads

#### vite.config.js
Configures Vite dev server and build process:
- Port configuration (3000)
- API proxy to backend
- React plugin integration

#### tailwind.config.js
Tailwind CSS customization:
- Custom color palette (primary, medical colors)
- Custom animations (fade-in, slide-up)
- Extended theme configuration

---

## Frontend Structure

### Components

#### Navbar.jsx
**Purpose**: Main navigation component
**Features**:
- Responsive mobile menu
- Active route highlighting
- Model status indicator
- Smooth animations with Framer Motion

**Key Props**: None (uses React Router location)

#### Footer.jsx
**Purpose**: Site footer with information
**Features**:
- Quick links to pages
- Project information
- Medical disclaimer
- Contact information

#### PredictionResult.jsx
**Purpose**: Display AI prediction results
**Features**:
- Color-coded by condition
- Confidence percentage bar
- Interpretation text
- Visual indicators

**Props**:
- `result`: Object containing prediction, confidence, probabilities

#### ProbabilityChart.jsx
**Purpose**: Visualize probability distribution
**Features**:
- Bar chart using Recharts
- Color-coded bars
- Responsive layout
- Legend with percentages

**Props**:
- `probabilities`: Object with class probabilities

---

### Pages

#### HomePage.jsx
**Purpose**: Landing page and project overview
**Sections**:
1. Hero - Project introduction with CTA
2. About - Problem statement and solution
3. Architecture - Model explanation
4. Diseases - Detectable conditions
5. Features - System capabilities
6. CTA - Call to action

**Animations**: Framer Motion scroll-based animations

#### DiagnosisPage.jsx
**Purpose**: Main diagnostic interface
**Features**:
1. Drag-and-drop image upload
2. Image preview
3. Loading state with progress bar
4. Results display
5. Report download
6. Guidelines and instructions

**State Management**:
- `selectedFile`: Uploaded file
- `preview`: Image preview URL
- `loading`: Processing state
- `result`: Prediction results

**API Integration**: POST /api/predict

#### ChatbotPage.jsx
**Purpose**: AI medical assistant interface
**Features**:
1. Chat message display
2. User/bot message differentiation
3. Suggested questions
4. Conversation history
5. Typing indicator
6. Disclaimer

**State Management**:
- `messages`: Array of chat messages
- `input`: Current user input
- `loading`: Bot response loading

**API Integration**: POST /api/chat

---

## Backend Structure

### main.py
**FastAPI application with endpoints**:

#### Routes:
1. `GET /` - API information
2. `GET /api/health` - Health check
3. `POST /api/predict` - Image prediction
4. `POST /api/chat` - Chatbot interaction

#### Key Functions:
- `load_model()` - Load trained model
- `preprocess_image()` - Image preprocessing
- `get_mock_prediction()` - Mock predictions
- `get_chatbot_response()` - Rule-based responses

### model_utils.py
**Model architecture and utilities**:

#### Classes:
- `PatchExtractor` - Extract patches for ViT
- `PatchEncoder` - Encode patches with positions

#### Functions:
- `create_mobilenet_base()` - MobileNet CNN
- `transformer_encoder()` - Transformer block
- `create_hybrid_model()` - Full hybrid model
- `compile_model()` - Compile with optimizer
- `get_callbacks()` - Training callbacks

---

## Data Flow

### Prediction Flow
```
User uploads image
      ↓
Frontend validates file
      ↓
POST /api/predict (FormData)
      ↓
Backend receives file
      ↓
Preprocess image (resize, normalize)
      ↓
Model prediction
      ↓
Return JSON response
      ↓
Frontend displays results
```

### Chat Flow
```
User types message
      ↓
POST /api/chat (JSON)
      ↓
Backend processes message
      ↓
Generate response (rule-based/LLM)
      ↓
Return response
      ↓
Display in chat UI
```

---

## State Management

### Frontend State (React Hooks)

**HomePage**: Minimal state (mostly static)

**DiagnosisPage**:
```javascript
{
  selectedFile: File | null,
  preview: string | null,
  loading: boolean,
  result: {
    prediction: string,
    confidence: number,
    probabilities: object,
    inference_time: number
  } | null
}
```

**ChatbotPage**:
```javascript
{
  messages: [{
    id: number,
    type: 'user' | 'bot',
    text: string,
    timestamp: Date
  }],
  input: string,
  loading: boolean
}
```

---

## Styling System

### Tailwind Utility Classes

**Buttons**:
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button

**Cards**:
- `.card` - Base card component

**Inputs**:
- `.input-field` - Form input styling

**Custom Colors**:
- `primary-*` - Blue shades
- `medical-*` - Medical theme colors

### Responsive Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

---

## API Data Models

### Request Models

#### PredictRequest
```
Content-Type: multipart/form-data
file: Image file (PNG, JPG, JPEG, DICOM)
```

#### ChatRequest
```json
{
  "message": "string",
  "history": [...]  // optional
}
```

### Response Models

#### PredictionResponse
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

#### ChatResponse
```json
{
  "response": "Detailed answer..."
}
```

---

## Dependencies

### Frontend Dependencies

**Core**:
- react: ^18.2.0
- react-dom: ^18.2.0
- react-router-dom: ^6.22.0

**UI & Styling**:
- tailwindcss: ^3.4.1
- framer-motion: ^11.0.3
- lucide-react: ^0.344.0

**Data & API**:
- axios: ^1.6.7
- recharts: ^2.12.0

**Utilities**:
- react-dropzone: ^14.2.3
- react-hot-toast: ^2.4.1

### Backend Dependencies

**Core**:
- fastapi: ^0.109.0
- uvicorn: ^0.27.0

**ML/AI**:
- tensorflow: ^2.15.0
- numpy: ^1.26.3
- pillow: ^10.2.0

**Utilities**:
- python-multipart: ^0.0.6
- pydantic: ^2.5.3

---

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```env
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/hybrid_mobilenet_vit.h5
CORS_ORIGINS=http://localhost:3000
```

---

## Build Outputs

### Frontend Build
```
dist/
├── assets/
│   ├── index-[hash].js      # Bundled JavaScript
│   ├── index-[hash].css     # Bundled CSS
│   └── [images]             # Optimized images
└── index.html               # Entry HTML
```

### Backend (No build, runs directly)

---

## Testing Structure (To be implemented)

```
tests/
├── frontend/
│   ├── components/
│   │   ├── Navbar.test.jsx
│   │   └── Footer.test.jsx
│   └── pages/
│       └── HomePage.test.jsx
│
└── backend/
    ├── test_api.py
    └── test_model.py
```

---

## Development Workflow

1. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   npm run dev
   ```

3. **Make Changes**:
   - Edit components/pages
   - Hot reload applies automatically

4. **Test**:
   - Manual testing in browser
   - API testing via /docs

5. **Build**:
   ```bash
   npm run build
   ```

---

## Key Design Decisions

### Why React?
- Component-based architecture
- Large ecosystem
- Excellent performance
- Great developer experience

### Why FastAPI?
- Modern Python framework
- Automatic API documentation
- Type hints and validation
- Async support

### Why Tailwind CSS?
- Utility-first approach
- Highly customizable
- Small bundle size
- Rapid development

### Why MobileNet + ViT?
- Efficient (MobileNet)
- Accurate (Transformer)
- Best of both worlds

---

## Future Enhancements

Potential additions:
- [ ] User authentication
- [ ] Prediction history
- [ ] Advanced heatmaps (Grad-CAM)
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Real-time collaboration
- [ ] Advanced analytics
- [ ] Model comparison
- [ ] Batch processing
- [ ] Report templates

---

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review security advisories
- Monitor performance
- Check error logs
- Backup data/models

### Version Updates
- Follow semantic versioning
- Document breaking changes
- Provide migration guides

---

For detailed information on any component, see the source code comments and related documentation files.
