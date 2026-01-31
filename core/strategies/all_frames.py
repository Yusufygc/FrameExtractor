# Frame_Ayirici/core/strategies/all_frames.py
"""
Strategy for extracting all frames from a video.
"""

import numpy as np
from .base import ExtractionStrategy


class AllFramesStrategy(ExtractionStrategy):
    """
    Strategy that saves every single frame from the video.
    The simplest extraction strategy.
    """
    
    @property
    def name(self) -> str:
        return "All Frames"
    
    def should_save_frame(self, frame: np.ndarray, frame_index: int) -> bool:
        """
        Always returns True - save every frame.
        
        Args:
            frame: The current frame (unused)
            frame_index: The frame index (unused)
            
        Returns:
            Always True
        """
        return True
