# Build System Documentation

## Overview

This project uses a two-pronged build system:
1. **Local builds** via PowerShell script (`build_exe.ps1`) for development
2. **Automated CI/CD builds** via GitHub Actions for releases

Both approaches use **PyInstaller** to package the Python application into a standalone Windows executable that requires no Python installation.

## Critical Files & Tools

### Core Build Files

| File | Purpose |
|------|---------|
| `RapidHarnessToE3SeriesImporter.spec` | PyInstaller configuration file that defines how to package the application. Ensures consistent, reproducible builds across environments. |
| `build_exe.ps1` | Local build script for developers. Automates dependency installation, version setting, and PyInstaller invocation. |
| `set_dev_version.ps1` | Sets the application version based on the current git commit hash for development builds. |
| `.github/workflows/build-executable.yml` | GitHub Actions workflow that automatically builds and releases executables when a release is published or manually triggered. |
| `requirements.txt` | Python package dependencies (openpyxl, click, colorama). |
| `src/__version__.py` | Version information file. Updated dynamically during builds. |

### Key Dependencies

- **openpyxl** (3.1.2): Excel file reading/writing
- **click** (8.1.7): Command-line interface framework
- **colorama** (0.4.6): Colored terminal output
- **PyInstaller**: Packages Python code into standalone executables (installed during build, not in requirements.txt)

## Build Process

### Local Build (Development)

```powershell
.\build_exe.ps1
```

**Steps:**
1. Sets development version from git commit hash via `set_dev_version.ps1`
2. Cleans previous build artifacts (`dist/` and `build/` directories)
3. Installs Python dependencies from `requirements.txt`
4. Installs PyInstaller
5. Runs PyInstaller using `RapidHarnessToE3SeriesImporter.spec`
6. Outputs executable to `dist/RapidHarnessToE3SeriesImporter.exe`

### Automated Build (GitHub Actions)

Triggered by:
- Publishing a GitHub Release (uses release tag as version)
- Manual workflow dispatch from GitHub UI (uses git commit hash as dev version)

**Steps:**
1. Checks out code with full git history
2. Sets up Python 3.13
3. Installs dependencies and PyInstaller
4. Sets version:
   - **Release builds**: Extracts version from git tag (e.g., `v1.0.0` → `1.0.0`)
   - **Manual builds**: Uses `dev-<commit-hash>` format
5. Builds executable using PyInstaller spec file
6. Tests executable with `--version` flag
7. Uploads executable as GitHub Actions artifact
8. (Implicitly) Attaches to release if triggered by release event

## PyInstaller Configuration

The `.spec` file handles:

- **Entry point**: `src/from-to-converter.py`
- **Hidden imports**: Explicitly lists all dependencies to ensure they're bundled
  - Standard library: csv, pathlib
  - Third-party: click, openpyxl, colorama
  - Local modules: __version__, utils, input_parsers, converters, output_writers, models
- **Data collection**: Uses `collect_all()` to gather all submodules and data files from dependencies
- **Optimization**: Disables UPX compression for maximum compatibility across Windows versions
- **Console mode**: Enabled for command-line output

## Version Management

### Development Builds
- Version format: `dev-<short-commit-hash>` (e.g., `dev-a1b2c3d`)
- Set by `set_dev_version.ps1` or GitHub Actions workflow
- Useful for tracking which commit a build came from

### Release Builds
- Version format: Extracted from git tag (e.g., `v1.0.0` → `1.0.0`)
- Set by GitHub Actions when a release is published
- Matches the semantic versioning tag

### Version File
- Located at `src/__version__.py`
- Contains single variable: `__version__`
- Dynamically updated during build process
- Accessible via `--version` CLI flag

## Output Artifacts

### Local Build
- **Location**: `dist/RapidHarnessToE3SeriesImporter.exe`
- **Size**: Typically 50-60 MB (includes Python runtime and all dependencies)
- **Distribution**: Can be copied to any Windows machine without Python installation

### GitHub Actions Build
- **Artifact**: Uploaded to GitHub Actions artifacts
- **Release**: Automatically attached to GitHub Release (if triggered by release event)
- **Availability**: Downloadable from Releases page

## Build Environment Requirements

### Local Development
- Windows OS (PowerShell 5.1+)
- Python 3.13+ (or compatible version)
- Git (for version detection)
- pip (Python package manager)

### GitHub Actions
- Automatically provided by `windows-latest` runner
- Python 3.13 installed via `actions/setup-python@v5`

## Troubleshooting

### Build Fails with "PyInstaller not found"
- Ensure PyInstaller is installed: `pip install pyinstaller`
- The build script installs it automatically

### Executable won't run on target machine
- Verify Windows version compatibility (PyInstaller builds for Windows 7+)
- Check that all dependencies are listed in the spec file's `hiddenimports`
- Ensure UPX is disabled (it is, for compatibility)

### Version not updating
- For local builds: Ensure you're in a git repository
- For GitHub Actions: Verify the release tag format (should start with `v`)
- Check `src/__version__.py` was updated correctly

### Build artifacts not cleaning up
- Manually delete `dist/` and `build/` directories
- The build script attempts to clean these automatically

## Best Practices

1. **Always use the spec file**: Ensures reproducible builds across environments
2. **Test the executable**: Both build scripts include version testing
3. **Tag releases properly**: Use semantic versioning (e.g., `v1.0.0`, `v1.2.3`)
4. **Keep dependencies minimal**: Only add packages that are truly necessary
5. **Update hidden imports**: When adding new dependencies, add them to the spec file's `hiddenimports` list
