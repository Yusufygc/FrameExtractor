# Frame_Ayirici/threads/worker.py
"""
Background worker thread for video processing.
Uses PySide6 and follows Dependency Inversion Principle.
"""

from PySide6.QtCore import QThread, Signal

from core.video_processor import VideoProcessor
from core.protocols import SignalAdapter


class ProcessingWorker(QThread):
    """
    QThread subclass that runs video processing in the background.
    
    Signals:
        finished: Emitted when processing completes successfully (str message)
        error: Emitted when an error occurs (str error message)
        progress_update: Emitted for progress updates (int 0-100)
        status_update: Emitted for status text updates (str message)
    """
    
    # Qt Signals for communication with UI
    finished = Signal(str)
    error = Signal(str)
    progress_update = Signal(int)
    status_update = Signal(str)
    
    def __init__(
        self, 
        video_path: str, 
        output_dir: str, 
        mode: str, 
        **kwargs
    ):
        """
        Initialize the processing worker.
        
        Args:
            video_path: Path to the video file
            output_dir: Output directory for frames
            mode: Extraction mode ('all', 'range', 'scene')
            **kwargs: Additional arguments for the strategy
        """
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.mode = mode
        self.kwargs = kwargs
    
    def run(self) -> None:
        """
        Execute the video processing task.
        This method runs in a separate thread.
        """
        try:
            # Create signal adapter that bridges Qt signals to Protocol
            # This follows Dependency Inversion Principle
            signal_adapter = SignalAdapter(
                progress_signal=self.progress_update,
                status_signal=self.status_update
            )
            
            # Create and run processor
            processor = VideoProcessor(
                video_path=self.video_path,
                output_dir=self.output_dir,
                mode=self.mode,
                signals=signal_adapter,
                **self.kwargs
            )
            
            result_message = processor.run()
            self.finished.emit(result_message)
            
        except Exception as e:
            self.error.emit(str(e))