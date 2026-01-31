# Frame_Ayirici/core/protocols.py
"""
Protocol definitions for Dependency Inversion Principle.
Abstracts signal interfaces to decouple VideoProcessor from Qt-specific implementations.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SignalProtocol(Protocol):
    """
    Protocol for progress signaling.
    Any class implementing these methods can be used as a signal provider.
    This follows the Dependency Inversion Principle - high-level modules
    should not depend on low-level modules, both should depend on abstractions.
    """
    
    def emit_progress(self, value: int) -> None:
        """Emit progress update (0-100)."""
        ...
    
    def emit_status(self, message: str) -> None:
        """Emit status message update."""
        ...


class SignalAdapter:
    """
    Adapter class to bridge Qt signals with the SignalProtocol.
    This allows VideoProcessor to remain decoupled from Qt.
    """
    
    def __init__(self, progress_signal, status_signal):
        """
        Initialize adapter with Qt signals.
        
        Args:
            progress_signal: Qt signal for progress updates (int)
            status_signal: Qt signal for status updates (str)
        """
        self._progress_signal = progress_signal
        self._status_signal = status_signal
    
    def emit_progress(self, value: int) -> None:
        """Emit progress update through Qt signal."""
        self._progress_signal.emit(value)
    
    def emit_status(self, message: str) -> None:
        """Emit status message through Qt signal."""
        self._status_signal.emit(message)
