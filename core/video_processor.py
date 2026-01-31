# Frame_Ayirici/core/video_processor.py
"""
Core video processing module.
Refactored to follow SOLID principles:
- Single Responsibility: Only handles video reading and frame saving
- Open/Closed: New extraction modes can be added via Strategy pattern
- Dependency Inversion: Uses SignalProtocol abstraction
"""

import os
import cv2
from pathlib import Path
from typing import Dict, Type

from core.protocols import SignalProtocol
from core.strategies import (
    ExtractionStrategy,
    AllFramesStrategy,
    TimeRangeStrategy,
    SceneChangeStrategy
)


class VideoProcessor:
    """
    Processes video files and extracts frames based on a given strategy.
    
    Attributes:
        video_path: Path to the video file
        output_dir: Directory for output frames
        strategy: The extraction strategy to use
        signals: Signal protocol for progress/status updates
    """
    
    # Strategy registry - maps mode names to strategy classes
    # Following Open/Closed Principle: add new strategies here without modifying run()
    STRATEGIES: Dict[str, Type[ExtractionStrategy]] = {
        'all': AllFramesStrategy,
        'range': TimeRangeStrategy,
        'scene': SceneChangeStrategy,
    }
    
    # JPEG quality for saved frames
    JPEG_QUALITY = 95
    
    # Status update interval (frames)
    STATUS_UPDATE_INTERVAL = 50
    
    def __init__(
        self, 
        video_path: str, 
        output_dir: str, 
        mode: str, 
        signals: SignalProtocol,
        **kwargs
    ):
        """
        Initialize VideoProcessor.
        
        Args:
            video_path: Path to the video file
            output_dir: Output directory (empty string for auto-desktop)
            mode: Extraction mode ('all', 'range', 'scene')
            signals: Object implementing SignalProtocol for updates
            **kwargs: Additional parameters for the strategy
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.mode = mode
        self.signals = signals
        self.kwargs = kwargs
    
    def _setup_output_directory(self) -> Path:
        """
        Create output directory if not specified.
        
        Returns:
            Path object pointing to the output directory
        """
        if not self.output_dir:
            video_name = Path(self.video_path).stem
            desktop_path = Path.home() / "Desktop"
            output_path = desktop_path / f"{video_name}_frames"
        else:
            output_path = Path(self.output_dir)
        
        os.makedirs(output_path, exist_ok=True)
        return output_path
    
    def _create_strategy(self, fps: float, total_frames: int) -> ExtractionStrategy:
        """
        Factory method to create the appropriate strategy.
        
        Args:
            fps: Video frames per second
            total_frames: Total number of frames
            
        Returns:
            ExtractionStrategy instance
            
        Raises:
            ValueError: If mode is not recognized
        """
        strategy_class = self.STRATEGIES.get(self.mode)
        
        if strategy_class is None:
            available = ', '.join(self.STRATEGIES.keys())
            raise ValueError(
                f"Unknown mode: '{self.mode}'. Available modes: {available}"
            )
        
        return strategy_class(fps=fps, total_frames=total_frames, **self.kwargs)
    
    def _save_frame(self, frame, save_path: str) -> bool:
        """
        Save a frame to disk using binary write for Unicode path support.
        
        Args:
            frame: OpenCV frame (numpy array)
            save_path: Path where to save the frame
            
        Returns:
            True if save was successful, False otherwise
        """
        # Encode frame to JPEG in memory
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, self.JPEG_QUALITY]
        is_success, buffer = cv2.imencode(".jpg", frame, encode_params)
        
        if not is_success:
            return False
        
        # Write buffer to file (handles Unicode paths correctly)
        with open(save_path, "wb") as f:
            f.write(buffer)
        
        return True
    
    def run(self) -> str:
        """
        Execute the frame extraction process.
        
        Returns:
            Success message with extraction details
            
        Raises:
            IOError: If video cannot be opened
        """
        output_path = self._setup_output_directory()
        video_name = Path(self.video_path).name
        
        self.signals.emit_status(f"Video açılıyor: {video_name}")
        
        # Open video file
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise IOError(
                "Video dosyası açılamadı. Dosya yolu veya format bozuk olabilir."
            )
        
        try:
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Validate FPS (some videos report invalid values)
            if fps is None or fps <= 0 or fps > 1000:
                fps = 30.0
            
            # Create extraction strategy
            strategy = self._create_strategy(fps, total_frames)
            strategy.reset()
            
            self.signals.emit_status(f"Strateji: {strategy.name}")
            
            # For time range mode, optimize by seeking to start frame
            start_frame = 0
            end_frame = total_frames
            
            if isinstance(strategy, TimeRangeStrategy):
                start_frame = strategy.start_frame
                end_frame = strategy.end_frame
                
                # Seek to start frame
                if start_frame > 0:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                    self.signals.emit_status(
                        f"Zaman aralığı: Frame {start_frame} - {end_frame}"
                    )
            
            # Calculate frames to process for accurate progress
            frames_to_process = end_frame - start_frame
            
            saved_count = 0
            frame_index = start_frame
            processed_count = 0
            
            while frame_index < end_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Ask strategy if this frame should be saved
                if strategy.should_save_frame(frame, frame_index):
                    saved_count += 1
                    save_path = str(output_path / f"frame_{saved_count:06d}.jpg")
                    self._save_frame(frame, save_path)
                
                frame_index += 1
                processed_count += 1
                
                # Update progress based on frames to process, not total
                if frames_to_process > 0:
                    progress = int((processed_count / frames_to_process) * 100)
                    self.signals.emit_progress(progress)
                    
                    if processed_count % self.STATUS_UPDATE_INTERVAL == 0:
                        self.signals.emit_status(
                            f"İşleniyor... Frame {processed_count}/{frames_to_process}"
                        )
        
        finally:
            cap.release()
        
        return (
            f"İşlem tamamlandı! '{output_path}' klasörüne "
            f"{saved_count} adet frame kaydedildi."
        )