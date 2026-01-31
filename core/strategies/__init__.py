# Frame_Ayirici/core/strategies/__init__.py
"""
Strategy pattern implementations for frame extraction.
Following Open/Closed Principle - new modes can be added without modifying existing code.
"""

from .base import ExtractionStrategy
from .all_frames import AllFramesStrategy
from .time_range import TimeRangeStrategy
from .scene_change import SceneChangeStrategy

__all__ = [
    'ExtractionStrategy',
    'AllFramesStrategy', 
    'TimeRangeStrategy',
    'SceneChangeStrategy'
]
