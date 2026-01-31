# Frame_Ayirici/core/strategies/scene_change.py
"""
Strategy for detecting and extracting scene change frames.
"""

import cv2
import numpy as np
from typing import Optional
from .base import ExtractionStrategy


class SceneChangeStrategy(ExtractionStrategy):
    """
    Strategy that detects scene changes using histogram comparison.
    Saves frames where significant visual changes are detected.
    """
    
    # Correlation threshold - lower values mean more sensitivity
    DEFAULT_THRESHOLD = 0.7
    
    def __init__(self, fps: float, total_frames: int, **kwargs):
        """
        Initialize SceneChangeStrategy.
        
        Args:
            fps: Frames per second
            total_frames: Total frame count
            **kwargs: Optional 'threshold' for scene change sensitivity (0.0-1.0)
        """
        super().__init__(fps, total_frames, **kwargs)
        
        self.threshold = kwargs.get('threshold', self.DEFAULT_THRESHOLD)
        self._prev_histogram: Optional[np.ndarray] = None
    
    @property
    def name(self) -> str:
        return "Scene Change Detection"
    
    def reset(self) -> None:
        """Reset the previous histogram for a new processing run."""
        self._prev_histogram = None
    
    def _compute_histogram(self, frame: np.ndarray) -> np.ndarray:
        """
        Compute normalized grayscale histogram of a frame.
        
        Args:
            frame: BGR frame from OpenCV
            
        Returns:
            Normalized histogram array
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        cv2.normalize(hist, hist)
        return hist
    
    def should_save_frame(self, frame: np.ndarray, frame_index: int) -> bool:
        """
        Detect scene change by comparing frame histograms.
        
        Args:
            frame: The current BGR frame
            frame_index: The frame index (unused but part of interface)
            
        Returns:
            True if scene change detected, False otherwise
        """
        current_hist = self._compute_histogram(frame)
        
        if self._prev_histogram is None:
            # First frame - always save
            self._prev_histogram = current_hist
            return True
        
        # Compare histograms using correlation method
        correlation = cv2.compareHist(
            self._prev_histogram, 
            current_hist, 
            cv2.HISTCMP_CORREL
        )
        
        # Update previous histogram
        self._prev_histogram = current_hist
        
        # If correlation is below threshold, it's a scene change
        return correlation < self.threshold
