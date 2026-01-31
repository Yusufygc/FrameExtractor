# Frame_Ayirici/utils/formatters.py
"""
Utility functions for formatting data.
Extracted from MainWindow to follow Single Responsibility Principle.
"""

import math


def format_duration(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS string format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted time string (e.g., "01:30:45")
    """
    if seconds < 0:
        return "00:00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_size(size_bytes: int) -> str:
    """
    Format byte size into human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 GB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ("B", "KB", "MB", "GB", "TB")
    
    # Calculate the appropriate unit index
    i = int(math.floor(math.log(size_bytes, 1024)))
    i = min(i, len(size_names) - 1)  # Prevent index out of range
    
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    
    return f"{size} {size_names[i]}"


def time_str_to_seconds(time_str: str) -> int:
    """
    Convert HH:MM:SS string to total seconds.
    
    Args:
        time_str: Time string in HH:MM:SS format
        
    Returns:
        Total seconds as integer
    """
    parts = time_str.split(':')
    if len(parts) != 3:
        raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM:SS")
    
    hours, minutes, seconds = map(int, parts)
    return hours * 3600 + minutes * 60 + seconds


def time_str_to_frame(time_str: str, fps: float) -> int:
    """
    Convert HH:MM:SS string to frame number.
    
    Args:
        time_str: Time string in HH:MM:SS format
        fps: Frames per second
        
    Returns:
        Frame number as integer
    """
    total_seconds = time_str_to_seconds(time_str)
    return int(total_seconds * fps)
