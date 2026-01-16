# Build script for creating Windows executable from from-to-converter.py
# This script automates the process of building a standalone .exe using PyInstaller

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "From-To Converter - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous build artifacts..." -ForegroundColor Yellow
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item -Force *.spec -ErrorAction SilentlyContinue

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}

# Build executable
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller --onefile `
    --name "FromToConverter" `
    --console `
    from-to-converter.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location: dist\FromToConverter.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now distribute the .exe file to users." -ForegroundColor White
Write-Host "No Python installation required to run it!" -ForegroundColor White
