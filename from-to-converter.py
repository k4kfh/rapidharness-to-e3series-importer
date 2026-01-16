"""CLI entry point for the harness converter."""

import click
from pathlib import Path
from colorama import init, Fore, Style
import csv

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

from utils import load_wire_lookup_table, load_device_lookup_table
from input_parsers import RapidHarnessParser
from converters import convert_device_partnumbers
from output_writers import write_e3_fromto_list
from models import ConversionError


@click.command()
@click.option(
    '--input', '-i',
    'input_file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help='Path to the RapidHarness Excel export file'
)
@click.option(
    '--output', '-o',
    'output_file',
    required=True,
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help='Path for the output E3.series From-To List Excel file'
)
@click.option(
    '--wire-map', '-w',
    'wire_map_file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help='Path to the wire lookup table CSV file'
)
@click.option(
    '--device-map', '-d',
    'device_map_file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help='Path to the device/connector lookup table CSV file'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
@click.option(
    '--error-log', '-e',
    'error_log_file',
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=None,
    help='Optional: Path to save a CSV file of all errors encountered'
)
def cli_main(input_file, output_file, wire_map_file, device_map_file, verbose, error_log_file):
    """Convert RapidHarness wire harness exports to E3.series From-To List format.
    
    This tool reads connection data from a RapidHarness Excel export and converts it
    to the format required by Zuken E3.series CAD software for import.
    """
    
    errors = []
    
    if verbose:
        click.echo(f"Input file: {input_file}")
        click.echo(f"Output file: {output_file}")
        click.echo(f"Wire map: {wire_map_file}")
        click.echo(f"Device map: {device_map_file}")
        click.echo("Loading lookup tables...")
    
    # Load lookup tables
    try:
        wire_lut = load_wire_lookup_table(wire_map_file)
        if verbose:
            click.echo(f"Loaded {len(wire_lut)} wire mappings")
    except Exception as e:
        click.echo(f"Error loading wire lookup table: {e}", err=True)
        raise click.Abort()
    
    try:
        device_lut = load_device_lookup_table(device_map_file)
        if verbose:
            click.echo(f"Loaded {len(device_lut)} device mappings")
    except Exception as e:
        click.echo(f"Error loading device lookup table: {e}", err=True)
        raise click.Abort()
    
    if verbose:
        click.echo("Starting conversion...")
    
    # Parse input file using RapidHarness parser
    try:
        parser = RapidHarnessParser()
        e3_fromto = parser.parse(input_file, wire_lut, errors, verbose)
    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"Error parsing input file: {e}", err=True)
        raise click.Abort()
    
    # Convert device part numbers for each row
    for idx, row in enumerate(e3_fromto, start=2):
        from_converted, to_converted = convert_device_partnumbers(
            row, device_lut, errors, idx
        )
        row.from_device_pn = from_converted
        row.to_device_pn = to_converted
    
    # Write output
    try:
        write_e3_fromto_list(e3_fromto, output_file)
    except Exception as e:
        click.echo(f"Error writing output file: {e}", err=True)
        raise click.Abort()
    
    # Save error log if requested
    if error_log_file is not None and len(errors) > 0:
        try:
            with open(error_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['error_type', 'row_number', 'entity_id', 'entity_value', 'description', 'timestamp']
                )
                writer.writeheader()
                for error in errors:
                    writer.writerow({
                        'error_type': error.error_type,
                        'row_number': error.row_number,
                        'entity_id': error.entity_id,
                        'entity_value': error.entity_value,
                        'description': error.description,
                        'timestamp': error.timestamp
                    })
            click.echo(f"\n{Fore.YELLOW}✓ Error log saved to: {error_log_file}{Style.RESET_ALL}")
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Failed to write error log: {e}{Style.RESET_ALL}", err=True)
    elif error_log_file is not None and len(errors) == 0:
        click.echo(f"\n{Fore.GREEN}✓ No errors encountered - no error log created{Style.RESET_ALL}")
    
    # Summary output
    if len(errors) > 0:
        click.echo(f"\n{Fore.YELLOW}⚠ {len(errors)} error(s) encountered during conversion{Style.RESET_ALL}")
        if error_log_file is None:
            click.echo(f"{Fore.CYAN}  Use the --error-log flag to save detailed error information to a CSV file{Style.RESET_ALL}")
    
    if verbose:
        click.echo(f"Conversion complete! Output saved to: {output_file}")
    else:
        click.echo(f"Successfully converted {len(e3_fromto)} connections to {output_file}")


if __name__ == '__main__':
    cli_main()

