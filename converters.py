"""Conversion logic for device part numbers and other transformations."""

import re
import click
from colorama import Fore, Style

from models import E3FromToListRow, ConversionError


def convert_device_partnumbers(row: E3FromToListRow, device_lut: dict, 
                               errors: list = None, row_num: int = None) -> tuple:
    """Convert RapidHarness device part numbers to E3.series equivalents.
    
    Handles:
    - Device lookup table mappings
    - Splice detection (devices named S\d+)
    - Error logging for unmapped devices
    
    Args:
        row: E3FromToListRow with device part numbers to convert
        device_lut: Device lookup table (maps RH P/N to E3 names)
        errors: List to accumulate ConversionError objects
        row_num: Row number for error tracking
        
    Returns:
        Tuple of (from_device_pn, to_device_pn) with conversions applied
    """
    
    # Convert FROM device
    from_converted = row.from_device_pn
    if row.from_device_pn in device_lut:
        from_converted = device_lut[row.from_device_pn]
    elif re.search(r'S\d+$', row.from_device_name or ''):
        # Splice detection: devices named S1, S2, etc. should have SPLICE part number
        from_converted = "SPLICE"
    elif row.from_device_pn is not None and errors is not None and row_num is not None:
        error_msg = f"Device '{row.from_device_pn}' not found in lookup table (FROM device)"
        click.echo(f"{Fore.RED}⚠ Row {row_num}: {error_msg}{Style.RESET_ALL}", err=True)
        error = ConversionError(
            error_type="DEVICE_NOT_FOUND",
            row_number=row_num,
            entity_id="FROM Device",
            entity_value=str(row.from_device_pn),
            description=error_msg
        )
        errors.append(error)
    
    # Convert TO device
    to_converted = row.to_device_pn
    if row.to_device_pn in device_lut:
        to_converted = device_lut[row.to_device_pn]
    elif re.search(r'S\d+$', row.to_device_name or ''):
        # Splice detection
        to_converted = "SPLICE"
    elif row.to_device_pn is not None and errors is not None and row_num is not None:
        error_msg = f"Device '{row.to_device_pn}' not found in lookup table (TO device)"
        click.echo(f"{Fore.RED}⚠ Row {row_num}: {error_msg}{Style.RESET_ALL}", err=True)
        error = ConversionError(
            error_type="DEVICE_NOT_FOUND",
            row_number=row_num,
            entity_id="TO Device",
            entity_value=str(row.to_device_pn),
            description=error_msg
        )
        errors.append(error)
    
    return (from_converted, to_converted)
