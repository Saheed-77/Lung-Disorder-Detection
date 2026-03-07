# Getting Started

Welcome to the Lung Disorder Detection AI project! This guide will help you get up and running quickly.

## Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ installed
- Python 3.10+ installed
- Git installed

### Automated Setup

**Windows**:
```powershell
.\setup.ps1
```

**Linux/Mac**:
```bash
chmod +x setup.sh
./setup.sh
```

This script will:
1. Check prerequisites
2. Install frontend dependencies
3. Set up Python virtual environment
4. Install backend dependencies

### Manual Setup

If the automated script doesn't work:

1. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```

2. **Set Up Backend**:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

## Running the Application

### Start Both Servers

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```
Backend will run on: http://localhost:8000

**Terminal 2 - Frontend**:
```bash
npm run dev
```
Frontend will run on: http://localhost:3000

### Access the Application

Open your browser and navigate to:
- **Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## First Steps

1. **Explore the Home Page**
   - Learn about the project
   - Understand the AI model
   - See supported diseases

2. **Try the Diagnosis System**
   - Navigate to "Diagnosis" page
   - Upload a chest X-ray image
   - Click "Analyze X-Ray"
   - View results and confidence scores

3. **Chat with AI Assistant**
   - Go to "AI Assistant" page
   - Ask questions about lung disorders
   - Try suggested questions

## Sample X-Ray Images

For testing, you can use sample chest X-ray images from:
- [NIH Chest X-ray Dataset](https://www.kaggle.com/nih-chest-xrays/data)
- [COVID-19 Radiography Database](https://www.kaggle.com/tawsifurrahman/covid19-radiography-database)

## Project Structure

```
Ui/
├── src/              # Frontend source code
│   ├── components/   # React components
│   ├── pages/        # Page components
│   └── App.jsx       # Main app
├── backend/          # Backend API
│   ├── main.py       # FastAPI app
│   └── model_utils.py # Model utilities
└── public/           # Static assets
```

## Common Commands

```bash
# Frontend
npm run dev           # Start dev server
npm run build         # Build for production
npm run preview       # Preview production build

# Backend
python main.py        # Start API server
uvicorn main:app --reload  # Start with auto-reload
```

## Troubleshooting

### Port Already in Use
If you see "Port 3000 is already in use":
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### Module Not Found
```bash
# Frontend
rm -rf node_modules package-lock.json
npm install

# Backend
pip install --force-reinstall -r requirements.txt
```

### CORS Errors
Make sure both frontend and backend are running on the correct ports:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Next Steps

- Read the [full README](README.md) for detailed information
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
- See [API.md](API.md) for API documentation
- Review [DEPLOYMENT.md](DEPLOYMENT.md) when ready to deploy

## Need Help?

- Check the documentation files
- Review the code comments
- Open an issue on GitHub
- Contact: research@lungai.com

---

**You're all set! Start building with confidence. 🚀**
