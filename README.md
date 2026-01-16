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
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── build_exe.ps1                 # Local build script for creating .exe
├── src/
│   ├── from-to-converter.py      # Main CLI entry point
│   ├── models.py                 # Data model definitions
│   ├── input_parsers.py          # Abstract parser interface + RapidHarness parser
│   ├── converters.py             # Conversion logic for device part numbers
│   ├── output_writers.py         # E3 Excel output formatting
│   └── utils.py                  # Lookup table loading utilities
├── examples/
│   ├── wire_lookup_example.csv   # Example wire lookup table template
│   └── device_lookup_example.csv # Example device lookup table template
├── docs/
│   ├── LOOKUP_TABLES.md          # Detailed guide for creating CSV lookup tables
│   ├── From-To-Import-Notes.md   # Technical notes and documentation
│   └── images/
│       └── device-not-in-db-during-import.png
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

1. **Prepare your input files:**
   - Export your RapidHarness design to Excel format
   - Create two CSV lookup tables (see [docs/LOOKUP_TABLES.md](docs/LOOKUP_TABLES.md) for detailed instructions):
     - Wire lookup table (maps wire part numbers)
     - Device lookup table (maps connector/device part numbers)
   - Example templates are provided in the `examples/` folder: `wire_lookup_example.csv` and `device_lookup_example.csv`

2. **Run the converter:**
   
   **Option A: Using the executable (Windows)**
   ```cmd
   FromToConverter.exe --input "RapidHarness_Export.xlsx" --output "E3FromToList.xlsx" --wire-map "wire_lookup.csv" --device-map "device_lookup.csv"
   ```
   
   **Option B: Short form**
   ```cmd
   FromToConverter.exe -i input.xlsx -o output.xlsx -w wires.csv -d devices.csv
   ```
   
   **Option C: Save errors to a CSV file for analysis**
   ```cmd
   FromToConverter.exe -i input.xlsx -o output.xlsx -w wires.csv -d devices.csv --error-log errors.csv
   ```
   
   **Option D: With verbose output**
   ```cmd
   FromToConverter.exe -i input.xlsx -o output.xlsx -w wires.csv -d devices.csv -v
   ```

3. **Import into E3.series:**
   - Open your E3.series project
   - Use the From-To List import function
   - Select the generated output file

**Command-line Options:**
- `--input` or `-i`: Path to the RapidHarness Excel export file (required)
- `--output` or `-o`: Path for the output E3 From-To List file (required)
- `--wire-map` or `-w`: Path to the wire lookup table CSV file (required)
- `--device-map` or `-d`: Path to the device lookup table CSV file (required)
- `--verbose` or `-v`: Enable detailed output messages (optional)
- `--error-log` or `-e`: Path to save a CSV file containing detailed error information (optional)
- `--version`: Display the application version
- `--help`: Display help information

**Error Handling:**
The tool logs issues encountered during conversion and displays them in the console:
- **Errors (displayed in red):** Critical issues representing data loss (e.g., missing wire mappings)
- **Warnings (if any, displayed in yellow):** Non-critical issues that don't prevent conversion, but may warrant investigation

Use the `--error-log` flag to save detailed issue information to a CSV file for further analysis. The issue log includes:
- Severity level (error or warning)
- Issue type (e.g., WIRE_NOT_FOUND)
- Row number where the issue occurred
- Entity ID and value that caused the issue
- Detailed description
- Timestamp

**Note:** Missing device mappings are not logged as errors — device part numbers are globally unique and may already exist in your E3.series database. The original RapidHarness part number will be used if no mapping is found. It's up to you to ensure that RapidHarness parts also exist in the E3 database. You'll see errors in the log when importing the from/to list into E3 if some devices are missing from the E3 database.

**See [docs/LOOKUP_TABLES.md](docs/LOOKUP_TABLES.md) for detailed information on creating and formatting the CSV lookup tables.**

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

3. **Create your lookup table CSV files:**
   - See [LOOKUP_TABLES.md](docs/LOOKUP_TABLES.md) for detailed instructions
   - Use the provided example files in `examples/` as templates

4. **Run the script directly:**
   ```powershell
   python src/from-to-converter.py --input "input.xlsx" --output "output.xlsx" --wire-map "examples/wire_lookup.csv" --device-map "examples/device_lookup.csv"
   ```
   
   Or use the short form:
   ```powershell
   python src/from-to-converter.py -i input.xlsx -o output.xlsx -w examples/wires.csv -d examples/devices.csv
   ```
   
   With error logging:
   ```powershell
   python src/from-to-converter.py -i input.xlsx -o output.xlsx -w examples/wires.csv -d examples/devices.csv -e errors.csv
   ```

### Building the Executable Locally

To create a standalone Windows executable for distribution:

1. **Run the build script:**
   ```powershell
   .\build_exe.ps1
   ```
   
   The build script will automatically:
   - Set the version to `dev-<commit-hash>` (e.g., `dev-261c5a6`)
   - Clean previous build artifacts
   - Install dependencies
   - Build the executable with PyInstaller

2. **Find the executable:**
   - The built executable will be in `dist\FromToConverter.exe`
   - This is a fully portable, standalone application
   - Check the version: `FromToConverter.exe --version`

3. **Distribute:**
   - Copy `FromToConverter.exe` to any location
   - Share with users (no Python installation required)

### Manual Build (Alternative)

If you prefer to build manually without the script:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --console --name "FromToConverter" src/from-to-converter.py
```

### Version Management

The application version is managed in `src/__version__.py`:

**For Release Builds (GitHub Actions):**
- Create a git tag: `git tag v1.0.0`
- Push the tag: `git push origin v1.0.0`
- Create a GitHub Release from the tag
- GitHub Actions automatically extracts the version from the tag and updates `src/__version__.py`
- The executable is built with the release version (e.g., `1.0.0`)

**For Development Builds (Local):**
- Run `.\build_exe.ps1` to build locally
- The script automatically sets the version to `dev-<commit-hash>` (e.g., `dev-261c5a6`)
- Check the version: `FromToConverter.exe --version`

**To manually update the version:**
- Edit `src/__version__.py` and change `__version__ = "1.0.0"` to your desired version
- The CLI will display this version with `--version` flag

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
tool uses external CSV files for component mapping:
- **Wire lookup table:** Maps RapidHarness wire SKUs to E3 wire components (gauge, color, type)
- **Device lookup table:** Converts between RapidHarness and E3 part numbering schemes
- **Splice detection:** Automatically identifies splice designations (e.g., `S1`, `S2`)

See [docs/LOOKUP_TABLES.md](docs/LOOKUP_TABLES.md) for detailed information on creating and formatting these CSV files.

Example template files are provided in the `examples/` folder:
- `wire_lookup_example.csv` - Template showing wire mapping format
- `device_lookup_example.csv` - Template showing device mapping format
- 20 AWG

Multiple colors are supported for each gauge. See the `rapidharness_wire_lut` dictionary in the source code for the complete list.

## Known Limitations

- File paths must be manually configured in the script (no GUI yet)
- Cable assemblies (multi-conductor cables) are not fully supported
- Cable assemblies (multi-conductor cables) are not fully supported
- Lookup tables must be manually created for each project
- CSV files must be properly formatted (UTF-8 encoding, correct column headers)

## Future Enhancements

Planned improvements include:
- GUI for easier file and lookup table management
- Better error reporting and validation
- Support for cable assemblies
- Auto-generation of lookup table templates from RapidHarness export

## Dependencies

- **openpyxl** (3.1.2): Excel file reading and writing
- **click** (8.1.7): Command-line interface framework
- **colorama** (0.4.6): Cross-platform colored terminal output
- **PyInstaller** (build-time only): Creating standalone executables

## License

[Add your license information here]

## Contributing
click** (8.1.7): Command-line interface framework
- **
[Add contribution guidelines if this is open source]

## Support

For questions or issues:
- See [docs/From-To-Import-Notes.md](docs/From-To-Import-Notes.md) for technical details
- [Add contact information or issue tracker link]
