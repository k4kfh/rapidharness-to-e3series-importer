# Build script for creating Windows executable from from-to-converter.py
# This script automates the process of building a standalone .exe using PyInstaller

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RapidHarness to E3.series Importer - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set development version based on git commit hash
Write-Host "Setting development version..." -ForegroundColor Yellow
& .\set_dev_version.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Could not set dev version (not in git repo?)" -ForegroundColor Yellow
}
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

# Build executable with enhanced PyInstaller options for portability
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
# Enhanced options for true portability:
# --collect-all: Ensures all package data files are bundled (required for click, openpyxl, colorama)
# --hidden-import: Explicitly includes modules that might not be detected automatically
# --noupx: Disables UPX compression to avoid compatibility issues across systems
pyinstaller --onefile `
    --name "RapidHarnessToE3SeriesImporter" `
    --console `
    --collect-all click `
    --collect-all openpyxl `
    --collect-all colorama `
    --hidden-import click `
    --hidden-import openpyxl `
    --hidden-import csv `
    --hidden-import pathlib `
    --hidden-import colorama `
    --collect-submodules src `
    --noupx `
    src/from-to-converter.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location: dist\RapidHarnessToE3SeriesImporter.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now distribute the .exe file to users." -ForegroundColor White
Write-Host "No Python installation required to run it!" -ForegroundColor White
