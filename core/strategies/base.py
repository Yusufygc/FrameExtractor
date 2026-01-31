# Frame_Ayirici/core/strategies/base.py
"""
Abstract base class for frame extraction strategies.
Part of Strategy Pattern implementation for Open/Closed Principle.
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class ExtractionStrategy(ABC):
    """
    Abstract base class for frame extraction strategies.
    
    Each strategy defines its own logic for deciding whether
    a frame should be saved or not.
    """
    
    def __init__(self, fps: float, total_frames: int, **kwargs):
        """
        Initialize the strategy.
        
        Args:
            fps: Frames per second of the video
            total_frames: Total number of frames in the video
            **kwargs: Additional strategy-specific parameters
        """
        self.fps = fps
        self.total_frames = total_frames
    
    @abstractmethod
    def should_save_frame(self, frame: np.ndarray, frame_index: int) -> bool:
        """
        Determine if the current frame should be saved.
        
        Args:
            frame: The current frame as numpy array
            frame_index: The index of the current frame (0-based)
            
        Returns:
            True if the frame should be saved, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the strategy name for display purposes."""
        pass
    
    def reset(self) -> None:
        """
        Reset any internal state. Called before processing starts.
        Override in subclasses if needed.
        """
        pass
