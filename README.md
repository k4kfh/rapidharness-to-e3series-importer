# From-To List Converter

A tool for converting wire harness designs exported from RapidHarness to a format compatible with E3.series CAD software.

## Overview

This tool reads Excel exports from RapidHarness and converts them into E3.series From-To List format, enabling easy import of harness designs between the two CAD systems.

**Key Features:**
- Converts RapidHarness connection data to E3 From-To List format
- Maps wire types and part numbers between systems
- Handles connectors, splices, and terminals
- Automatically detects and converts splice designations
- Provides wire gauge, color, and type information

## Repository Structure

```
from-to-list-import/
├── from-to-converter.py          # Main conversion script
├── requirements.txt              # Python dependencies
├── build_exe.ps1                 # Local build script for creating .exe
├── README.md                     # This file
├── From-To-Import-Notes.md       # Technical notes and documentation
├── .github/
│   └── workflows/
│       └── build-executable.yml  # GitHub Actions workflow for automated builds
├── dist/                         # Output directory for built executables (gitignored)
└── build/                        # PyInstaller build artifacts (gitignored)
```

## For End Users

### Downloading the Tool

1. Go to the [Releases](../../releases) page
2. Download the latest `FromToConverter.exe`
3. Save it anywhere on your computer (no installation needed!)

### Running the Tool

1. **Prepare your input file:**
   - Export your RapidHarness design to Excel format
   - Note the file location

2. **Edit the script configuration:**
   - Open `from-to-converter.py` in a text editor
   - Update the file paths in the `CONFIG PARAMETERS` section:
     ```python
     rh_excel_path = "path/to/your/RapidHarness_Export.xlsx"
     e3_fromto_excel_path = "path/to/output/E3FromToList.xlsx"
     ```

3. **Run the converter:**
   - Double-click `FromToConverter.exe`
   - The tool will process the input and create the E3 From-To List

4. **Import into E3.series:**
   - Open your E3.series project
   - Use the From-To List import function
   - Select the generated `E3FromToList.xlsx` file

**Note:** Currently, file paths must be configured in the script. A future version will add a GUI or command-line interface for easier file selection.

## For Developers

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setting Up Development Environment

1. **Clone or navigate to this directory**

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the script directly:**
   ```powershell
   python from-to-converter.py
   ```

### Building the Executable Locally

To create a standalone Windows executable for distribution:

1. **Run the build script:**
   ```powershell
   .\build_exe.ps1
   ```

2. **Find the executable:**
   - The built executable will be in `dist\FromToConverter.exe`
   - This is a fully portable, standalone application

3. **Distribute:**
   - Copy `FromToConverter.exe` to any location
   - Share with users (no Python installation required)

### Manual Build (Alternative)

If you prefer to build manually without the script:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --console --name "FromToConverter" from-to-converter.py
```

## Automated Builds (GitHub Actions)

This repository includes a GitHub Actions workflow that automatically builds the executable when a new release is created.

### Creating a Release with Automated Build

1. **Create and push a version tag:**
   ```powershell
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Create a GitHub Release:**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Select the tag you just created (e.g., `v1.0.0`)
   - Add release notes describing changes
   - Click "Publish release"

3. **Automatic build:**
   - GitHub Actions will automatically trigger
   - The workflow builds `FromToConverter.exe` on Windows
   - The executable is automatically attached to the release
   - Users can download it from the Releases page

### Manual Workflow Trigger

You can also trigger the build manually without creating a release:

1. Go to the "Actions" tab in GitHub
2. Select "Build Windows Executable"
3. Click "Run workflow"
4. The built executable will be available as a downloadable artifact (retained for 90 days)

## Technical Details

### Conversion Process

The tool performs the following steps:

1. **Parse RapidHarness Data:**
   - Reads the "Connections" sheet from the RapidHarness Excel export
   - Extracts connection endpoints, wire information, and part numbers

2. **Map Components:**
   - Converts RapidHarness wire SKUs to E3 wire types using lookup tables
   - Maps connector part numbers between systems
   - Detects and converts splice designations

3. **Generate E3 From-To List:**
   - Creates properly formatted Excel file for E3.series import
   - Includes device names, part numbers, pins, wire data, and signal names

### Lookup Tables

The script includes lookup tables for:
- **Wire types:** Maps RapidHarness wire SKUs to E3 wire components (gauge, color, type)
- **Device part numbers:** Converts between RapidHarness and E3 part numbering schemes
- **Splice detection:** Automatically identifies splice designations (e.g., `S1`, `S2`)

### Supported Wire Gauges

Currently supports TXL wire in the following gauges:
- 12 AWG
- 14 AWG
- 16 AWG
- 18 AWG
- 20 AWG

Multiple colors are supported for each gauge. See the `rapidharness_wire_lut` dictionary in the source code for the complete list.

## Known Limitations

- File paths must be manually configured in the script (no GUI yet)
- Cable assemblies (multi-conductor cables) are not fully supported
- Only TXL wire type is currently in the lookup table
- Part number mappings are limited to commonly used components

## Future Enhancements

Planned improvements include:
- GUI or command-line interface for file selection
- Expanded wire type and part number lookup tables
- Better error reporting and validation
- Support for cable assemblies
- Configuration file for custom mappings

## Dependencies

- **openpyxl** (3.1.2): Excel file reading and writing
- **PyInstaller** (build-time only): Creating standalone executables

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if this is open source]

## Support

For questions or issues:
- See `From-To-Import-Notes.md` for technical details
- [Add contact information or issue tracker link]
