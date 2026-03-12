# Quick Start Script for Windows PowerShell

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Lung Disorder Detection - Quick Start" -ForegroundColor Cyan
Write-Host "  AI-Powered Medical Diagnostic System" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "[1/5] Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found. Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "`n[2/5] Checking Python..." -ForegroundColor Yellow
$pythonCommand = $null
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -eq 0) {
    $pythonCommand = "python"
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    $pythonVersion = py -3.10 --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonCommand = "py -3.10"
        Write-Host "✓ Python found via launcher: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Python not found. Please install Python 3.10+ from https://python.org/" -ForegroundColor Red
        Write-Host "  On Windows, you can also use the Python launcher command: py -3.10" -ForegroundColor Yellow
        exit 1
    }
}

# Install Frontend Dependencies
Write-Host "`n[3/5] Installing frontend dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install frontend dependencies" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "`n[4/5] Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    if ($pythonCommand -eq "python") {
        python -m venv venv
    } else {
        py -3.10 -m venv venv
    }
}

# Activate virtual environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Backend setup complete" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

Set-Location ..

# Success message
Write-Host "`n[5/5] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Ready to start the application!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start Backend (Terminal 1):" -ForegroundColor Cyan
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Start Frontend (Terminal 2):" -ForegroundColor Cyan
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Open browser:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "For detailed documentation, see README.md" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
