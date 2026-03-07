"""
Hugging Face Spaces Deployment Entry Point
Lung Disease Detection - InceptionV3 + ViT Model
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app from torch_main
from torch_main import app

# This is required for Hugging Face Spaces deployment
# The file must be named app.py and export an 'app' variable

if __name__ == "__main__":
    import uvicorn
    # For local testing
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")
