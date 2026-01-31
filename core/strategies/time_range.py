# Frame_Ayirici/core/strategies/time_range.py
"""
Strategy for extracting frames within a specific time range.
"""

import numpy as np
from .base import ExtractionStrategy
from utils.formatters import time_str_to_frame


class TimeRangeStrategy(ExtractionStrategy):
    """
    Strategy that saves frames only within a specified time range.
    Uses start_time and end_time parameters in HH:MM:SS format.
    """
    
    def __init__(self, fps: float, total_frames: int, **kwargs):
        """
        Initialize TimeRangeStrategy.
        
        Args:
            fps: Frames per second
            total_frames: Total frame count
            **kwargs: Must include 'start_time' and 'end_time' in HH:MM:SS format
        """
        super().__init__(fps, total_frames, **kwargs)
        
        start_time_str = kwargs.get('start_time', '00:00:00')
        end_time_str = kwargs.get('end_time', '99:99:99')
        
        self.start_frame = time_str_to_frame(start_time_str, fps)
        self.end_frame = time_str_to_frame(end_time_str, fps)
        
        # Clamp end_frame to total_frames
        self.end_frame = min(self.end_frame, total_frames)
    
    @property
    def name(self) -> str:
        return "Time Range"
    
    def should_save_frame(self, frame: np.ndarray, frame_index: int) -> bool:
        """
        Check if frame is within the specified time range.
        
        Args:
            frame: The current frame (unused)
            frame_index: The 0-based frame index
            
        Returns:
            True if frame is within range, False otherwise
        """
        return self.start_frame <= frame_index < self.end_frame
