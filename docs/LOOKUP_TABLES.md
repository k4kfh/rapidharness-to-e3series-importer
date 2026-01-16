# Lookup Table Configuration

This tool requires two CSV files to map components between RapidHarness and E3.series:

1. **Wire Lookup Table** - Maps wire part numbers to E3 wire specifications
2. **Device Lookup Table** - Maps connector/device part numbers between systems

## Wire Lookup Table Format

**Filename:** `wire_lookup.csv` (or any name you choose)

**Required Columns:**
- `RapidHarness_Name` - The exact wire part number/name as it appears in your RapidHarness export
- `Wire_Group` - The wire group in E3 (e.g., TXL, GXL, SXL)
- `E3_Wire_Type` - The complete wire type designation in E3 (e.g., 14-AWG-RED)
- `AWG_Gauge` - The wire gauge as an integer (e.g., 14, 16, 18, 20)
- `Color` - The wire color (e.g., RED, BLACK, BLUE)

### Example Wire Lookup Table

```csv
RapidHarness_Name,Wire_Group,E3_Wire_Type,AWG_Gauge,Color
Generic 14AWG TXL Red,TXL,14-AWG-RED,14,RED
Generic 14AWG TXL Black,TXL,14-AWG-BLK,14,BLACK
Generic 16AWG TXL Red,TXL,16-AWG-RED,16,RED
Generic 16AWG TXL White,TXL,16-AWG-WHT,16,WHITE
Generic 18AWG TXL Blue,TXL,18-AWG-BLU,18,BLUE
Generic 18AWG TXL Yellow,TXL,18-AWG-YEL,18,YELLOW
Generic 20AWG TXL Orange,TXL,20-AWG-ORG,20,ORANGE
Generic 20AWG TXL Gray,TXL,20-AWG-GRY,20,GREY
14AWG-TXL-RED-WHITE,TXL,14-AWG-RED/WHT,14,RED
```

**Notes:**
- The `RapidHarness_Name` must match exactly what appears in Column E of your RapidHarness "Connections" sheet
- For striped wires, use a slash in the `E3_Wire_Type` (e.g., RED/WHT)
- The `Color` field is used for the wire color column in the E3 From-To List
- All column headers are case-sensitive

## Device Lookup Table Format

**Filename:** `device_lookup.csv` (or any name you choose)

**Required Columns:**
- `RapidHarness_PartNumber` - The connector/device part number from RapidHarness
- `E3_Device_Name` - The corresponding device name/part number in E3.series

### Example Device Lookup Table

```csv
RapidHarness_PartNumber,E3_Device_Name
AT06-3S-SR01GRY,DT06-3S-E008
ATM06-2S-SR01GY,DTM06-2S-E007
368376-1,368376-1_WithBackshell
1-368376-1,1-368376-1_WithBackshell
33462,RingTerm_5/16in_Uninsulated
33466,RingTerm_3/8in_Uninsulated
PV18-6FN-MY,ForkTerm_VinylInsulated
```

**Notes:**
- The `RapidHarness_PartNumber` must match exactly what appears in Columns K and M of your RapidHarness "Connections" sheet
- The `E3_Device_Name` should match the part number or device name as it exists in your E3.series database
- If a part number is not found in this table, the original RapidHarness part number will be used
- Splices (devices with names like S1, S2, S3) are automatically detected and assigned the part number "SPLICE"

## Creating Your Lookup Tables

### Step 1: Export Unique Values from RapidHarness

To create your lookup tables, you'll need to identify all unique wire types and device part numbers in your RapidHarness export:

1. Open your RapidHarness export Excel file
2. Go to the "Connections" sheet
3. For wires: Copy all unique values from Column E (Wire Part Number)
4. For devices: Copy all unique values from Columns K and M (Connector Part Numbers)

### Step 2: Create the CSV Files

1. Create a new CSV file for each lookup table
2. Add the required column headers (exactly as shown above)
3. Add one row for each unique part number
4. Fill in the corresponding E3 values

### Step 3: Validate Your CSV Files

- Ensure there are no extra spaces in column headers
- Make sure all required columns are present
- Verify that part numbers match exactly (case-sensitive)
- Check that AWG_Gauge values are integers (no quotes)
- Save files with UTF-8 encoding

## Usage Example

Once you've created your lookup table CSV files, run the converter like this:

```bash
python src/from-to-converter.py \
  --input "RapidHarness_Export.xlsx" \
  --output "E3_FromToList.xlsx" \
  --wire-map "wire_lookup.csv" \
  --device-map "device_lookup.csv"
```

Or using short options:

```bash
python src/from-to-converter.py -i input.xlsx -o output.xlsx -w wires.csv -d devices.csv
```

## Troubleshooting

### "Unable to find wire in lookup table"

This error means a wire part number from your RapidHarness export wasn't found in your wire lookup CSV. Wire mappings are critical—without them, E3.series won't know how to import the wire data, since manufacturer part numbers aren't the common way to specify wires (nobody cares who made it most of the time, they care that it's 14AWG Orange GXL wire). To fix:

1. Check the exact spelling of the wire name in the error message
2. Add that wire name to your `wire_lookup.csv` file with the correct E3 wire specifications
3. Re-run the conversion

### "Error loading lookup table"

This error usually means:
- The CSV file path is incorrect
- The CSV file is missing required columns
- The CSV file has formatting issues (check for extra commas, quotes, etc.)

To troubleshoot:
1. Verify the CSV file exists at the path specified
2. Open the file in a text editor and confirm it has the correct column headers
3. Check for extra spaces in headers or malformed lines
4. Ensure the file is saved with UTF-8 encoding

### Missing Device Mappings

If a device part number isn't in your device lookup table, the tool will silently use the original RapidHarness part number. This is **not** an error because device part numbers are globally unique and may already exist in your E3.series database. However, if the part number doesn't match your E3 database, you may see errors during E3 import (E3 will create a "virtual device" placeholder to allow the import to continue).

## Template Files

Example lookup table files are provided:
- `wire_lookup_example.csv` - Template for wire mappings
- `device_lookup_example.csv` - Template for device mappings

Copy these files and modify them with your actual part numbers.
