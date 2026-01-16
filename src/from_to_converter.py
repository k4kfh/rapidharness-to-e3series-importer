"""CLI entry point for the harness converter."""

import click
from pathlib import Path
from colorama import init, Fore, Style
import csv
import openpyxl

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

from .__version__ import __version__
from .utils import load_wire_lookup_table, load_device_lookup_table
from .input_parsers import RapidHarnessParser
from .converters import convert_device_partnumbers
from .output_writers import write_e3_fromto_list
from .models import ConversionError


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
@click.version_option(version=__version__, prog_name='RapidHarness-to-E3Series-Importer')
def cli_main(input_file, output_file, wire_map_file, device_map_file, verbose, error_log_file):
    """Convert RapidHarness wire harness exports to E3.series From-To List format.
    
    This tool reads connection data from a RapidHarness Excel export and converts it
    to the format required by Zuken E3.series CAD software for import.
    
    For more information, visit: https://github.com/k4kfh/rapidharness-to-e3series-importer
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
    except FileNotFoundError:
        click.echo(f"Error: Wire lookup table not found: {wire_map_file}", err=True)
        raise click.Abort()
    except (KeyError, ValueError) as e:
        click.echo(f"Error: Wire lookup table format invalid: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error loading wire lookup table: {e}", err=True)
        raise click.Abort()
    
    try:
        device_lut = load_device_lookup_table(device_map_file)
        if verbose:
            click.echo(f"Loaded {len(device_lut)} device mappings")
    except FileNotFoundError:
        click.echo(f"Error: Device lookup table not found: {device_map_file}", err=True)
        raise click.Abort()
    except (KeyError, ValueError) as e:
        click.echo(f"Error: Device lookup table format invalid: {e}", err=True)
        raise click.Abort()
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
    except FileNotFoundError:
        click.echo(f"Error: Input file not found: {input_file}", err=True)
        raise click.Abort()
    except openpyxl.utils.exceptions.InvalidFileException:
        click.echo(f"Error: Input file is not a valid Excel file: {input_file}", err=True)
        raise click.Abort()
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
    except PermissionError:
        click.echo(f"Error: Permission denied writing to output file: {output_file}", err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(f"Error: Cannot write to output file: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error writing output file: {e}", err=True)
        raise click.Abort()
    
    # Save error log if requested
    if error_log_file is not None and len(errors) > 0:
        try:
            with open(error_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['severity', 'error_type', 'row_number', 'entity_id', 'entity_value', 'description', 'timestamp']
                )
                writer.writeheader()
                for error in errors:
                    writer.writerow({
                        'severity': error.severity,
                        'error_type': error.error_type,
                        'row_number': error.row_number,
                        'entity_id': error.entity_id,
                        'entity_value': error.entity_value,
                        'description': error.description,
                        'timestamp': error.timestamp
                    })
            click.echo(f"\n{Fore.CYAN}[OK] Issue log saved to: {error_log_file}{Style.RESET_ALL}")
        except PermissionError:
            click.echo(f"{Fore.RED}[ERROR] Permission denied writing to issue log: {error_log_file}{Style.RESET_ALL}", err=True)
        except OSError as e:
            click.echo(f"{Fore.RED}[ERROR] Cannot write issue log: {e}{Style.RESET_ALL}", err=True)
        except Exception as e:
            click.echo(f"{Fore.RED}[ERROR] Failed to write issue log: {e}{Style.RESET_ALL}", err=True)
    elif error_log_file is not None and len(errors) == 0:
        click.echo(f"\n{Fore.GREEN}[OK] No issues encountered - no issue log created{Style.RESET_ALL}")
    
    # Summary output
    total_rows = len(e3_fromto)
    warning_count = sum(1 for e in errors if e.severity == "warning")
    error_count = sum(1 for e in errors if e.severity == "error")
    
    click.echo(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}Conversion Summary{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo(f"Total rows processed:     {total_rows}")
    
    if error_count > 0 or warning_count > 0:
        if error_count > 0:
            click.echo(f"Errors:                   {Fore.RED}{error_count}{Style.RESET_ALL}")
        if warning_count > 0:
            click.echo(f"Warnings:                 {Fore.YELLOW}{warning_count}{Style.RESET_ALL}")
        if error_log_file is None:
            click.echo(f"{Fore.CYAN}→ Use --error-log to save detailed issue information{Style.RESET_ALL}")
    else:
        click.echo(f"Status:                   {Fore.GREEN}No issues{Style.RESET_ALL}")
    
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo(f"Output saved to: {output_file}")


if __name__ == '__main__':
    cli_main()
