"""Data models for harness conversion."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversionError:
    """Represents an error or warning encountered during conversion."""
    severity: str  # "warning" or "error"
    error_type: str
    row_number: int
    entity_id: str
    entity_value: str
    description: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass(frozen=True)
class E3WireComponent:
    """Represents a valid individual wire type in the E3 database.
    
    For example, 14AWG Brown TXL.
    """
    wire_group: str
    """Wire Group, for example `TXL-BROWN`."""
    
    wire_type: str
    """Wire Type, for example `12-AWG-BRN`."""
    
    cross_section_awg: int
    """Wire Cross-Section in AWG. For example, `12`."""
    
    color: str
    """Wire Color. E3 seems to like 3-letter color codes like `PNK`, `RED`, `BRN`."""


@dataclass(frozen=True)
class RapidHarnessEndpoint:
    """Represents a specific pin on a specific connector or device in RapidHarness."""
    
    raw_string: str
    """The raw reference designator, unmodified."""

    def get_device_des(self) -> str:
        """Return only the device/connector portion (strip away pin designation if present)."""
        return self.raw_string.split(".")[0]
    
    def get_pin_des(self) -> str:
        """Return only the pin designation (strip away device designation).
        
        Returns None for pinless devices like Ring Terminals.
        """
        split_raw_str = self.raw_string.split(".")
        if len(split_raw_str) == 1:
            return None
        return split_raw_str[1]


@dataclass
class E3FromToListRow:
    """Represents a single connection in the E3 From-To List.
    
    This is the intermediate format produced by all input parsers.
    """
    # FROM RefDes
    from_device_name: str = None
    from_device_pn: str = None
    from_pin: str = None
    
    # TO RefDes
    to_device_name: str = None
    to_device_pn: str = None
    to_pin: str = None
    
    # Conductor/Signal Info
    wire: E3WireComponent = None
    signal_name: str = None
    wire_index: str = None
