# Build System Notes

## Problem Summary
The GitHub Actions build was creating a 10MB executable that failed with `ModuleNotFoundError: No module named 'src.__version__'`, while the local build created a working 25MB executable.

## Root Causes
1. **Missing dependency**: `colorama` was not in `requirements.txt`
2. **Python version mismatch**: Local build used Python 3.13, GitHub Actions used 3.11
3. **Inconsistent build process**: Command-line PyInstaller flags weren't reliably collecting all dependencies
4. **Module import issues**: PyInstaller wasn't finding local modules in the `src/` directory

## Solution
Switched to using a **PyInstaller spec file** (`RapidHarnessToE3SeriesImporter.spec`) for consistent, reproducible builds:

### Key Changes:
1. **Added `colorama==0.4.6`** to `requirements.txt`
2. **Updated GitHub Action** to use Python 3.13 (matching local environment)
3. **Created comprehensive spec file** that:
   - Uses `collect_all()` to gather all submodules and data files from dependencies
   - Explicitly lists all hidden imports (local modules and third-party packages)
   - Uses cross-platform path handling (`os.path.join`)
   - Disables UPX compression for maximum compatibility
4. **Simplified build scripts** to use the spec file instead of long command-line arguments

### Files Modified:
- `requirements.txt` - Added colorama
- `build_exe.ps1` - Removed spec file deletion, simplified to use spec file
- `.github/workflows/build-executable.yml` - Updated Python version, simplified build command
- `RapidHarnessToE3SeriesImporter.spec` - Created comprehensive spec file

## Build Process
Both local and CI builds now use the same process:
```powershell
pyinstaller --clean --noconfirm RapidHarnessToE3SeriesImporter.spec
```

This ensures:
- ✅ Consistent builds across environments
- ✅ All dependencies properly bundled
- ✅ Fully portable executable (~24MB)
- ✅ No external dependencies required

## Testing
The executable can be tested with:
```powershell
.\dist\RapidHarnessToE3SeriesImporter.exe --version
```

Expected output: `RapidHarness-to-E3Series-Importer, version <version>`
