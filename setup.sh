#!/bin/bash

# Quick Start Script for Linux/Mac

echo "================================================"
echo "  Lung Disorder Detection - Quick Start"
echo "  AI-Powered Medical Diagnostic System"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Node.js
echo -e "${YELLOW}[1/5] Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+ from https://nodejs.org/${NC}"
    exit 1
fi

# Check Python
echo -e "\n${YELLOW}[2/5] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.10+ from https://python.org/${NC}"
    exit 1
fi

# Install Frontend Dependencies
echo -e "\n${YELLOW}[3/5] Installing frontend dependencies...${NC}"
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install frontend dependencies${NC}"
    exit 1
fi

# Setup Backend
echo -e "\n${YELLOW}[4/5] Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${CYAN}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo -e "${CYAN}Installing backend dependencies...${NC}"
source venv/bin/activate
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend setup complete${NC}"
else
    echo -e "${RED}✗ Failed to install backend dependencies${NC}"
    exit 1
fi

cd ..

# Success message
echo -e "\n${GREEN}[5/5] Setup Complete!${NC}"
echo ""
echo "================================================"
echo "  Ready to start the application!"
echo "================================================"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo ""
echo -e "${CYAN}1. Start Backend (Terminal 1):${NC}"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo -e "${CYAN}2. Start Frontend (Terminal 2):${NC}"
echo "   npm run dev"
echo ""
echo -e "${CYAN}3. Open browser:${NC}"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "================================================"
echo -e "${YELLOW}For detailed documentation, see README.md${NC}"
echo "================================================"
