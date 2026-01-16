"""Lookup table loading utilities."""

import csv
from pathlib import Path
from models import E3WireComponent


def load_wire_lookup_table(csv_path: Path) -> dict:
    """Load wire lookup table from CSV file.
    
    CSV Format:
        RapidHarness_Name,Wire_Group,E3_Wire_Type,AWG_Gauge,Color
    
    Example:
        Generic 14AWG TXL Red,TXL,14-AWG-RED,14,RED
        Generic 20AWG TXL Black,TXL,20-AWG-BLK,20,BLACK
    
    Returns:
        dict: Maps RapidHarness wire names to E3WireComponent objects
    """
    wire_lut = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wire_lut[row['RapidHarness_Name']] = E3WireComponent(
                wire_group=row['Wire_Group'],
                wire_type=row['E3_Wire_Type'],
                cross_section_awg=int(row['AWG_Gauge']),
                color=row['Color']
            )
    return wire_lut


def load_device_lookup_table(csv_path: Path) -> dict:
    """Load device/connector lookup table from CSV file.
    
    CSV Format:
        RapidHarness_PartNumber,E3_Device_Name
    
    Example:
        CONNECTOR-001,DT06-3S-E008
        TERMINAL-002,RingTerm_Example
    
    Returns:
        dict: Maps RapidHarness part numbers to E3 device names
    """
    device_lut = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            device_lut[row['RapidHarness_PartNumber']] = row['E3_Device_Name']
    return device_lut
