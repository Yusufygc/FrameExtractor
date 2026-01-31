# Frame_Ayirici/ui/backend.py
"""
Python backend for QML interface.
Provides data bindings and operations to the QML frontend.
"""

import os
import cv2
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl

from threads.worker import ProcessingWorker
from utils.formatters import format_duration, format_size


class Backend(QObject):
    """
    Backend class that bridges Python logic with QML UI.
    Exposes properties and methods to QML via Qt's meta-object system.
    """
    
    # Signals for QML data binding
    videoPathChanged = Signal()
    outputDirChanged = Signal()
    videoInfoChanged = Signal()
    progressChanged = Signal()
    statusChanged = Signal()
    processingChanged = Signal()
    timeRangeChanged = Signal()
    showMessage = Signal(str, str, bool)  # title, message, isError
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Private state
        self._video_path: str = ""
        self._output_dir: str = ""
        self._resolution: str = "-"
        self._duration: str = "-"
        self._fps: float = 0.0
        self._frame_count: int = 0
        self._file_size: str = "-"
        self._video_duration: int = 0  # in seconds
        self._progress: int = 0
        self._status_message: str = "Başlamak için bir video seçin."
        self._is_processing: bool = False
        self._start_time: str = "00:00:00"
        self._end_time: str = "00:00:00"
        
        self._worker: Optional[ProcessingWorker] = None
    
    # ============ Video Path Property ============
    @Property(str, notify=videoPathChanged)
    def videoPath(self) -> str:
        return self._video_path
    
    @videoPath.setter
    def videoPath(self, value: str) -> None:
        if self._video_path != value:
            self._video_path = value
            self.videoPathChanged.emit()
    
    # ============ Output Directory Property ============
    @Property(str, notify=outputDirChanged)
    def outputDir(self) -> str:
        return self._output_dir
    
    @outputDir.setter
    def outputDir(self, value: str) -> None:
        if self._output_dir != value:
            self._output_dir = value
            self.outputDirChanged.emit()
    
    # ============ Video Info Properties ============
    @Property(str, notify=videoInfoChanged)
    def resolution(self) -> str:
        return self._resolution
    
    @Property(str, notify=videoInfoChanged)
    def duration(self) -> str:
        return self._duration
    
    @Property(float, notify=videoInfoChanged)
    def fps(self) -> float:
        return self._fps
    
    @Property(int, notify=videoInfoChanged)
    def frameCount(self) -> int:
        return self._frame_count
    
    @Property(str, notify=videoInfoChanged)
    def fileSize(self) -> str:
        return self._file_size
    
    @Property(int, notify=videoInfoChanged)
    def videoDuration(self) -> int:
        return self._video_duration
    
    # ============ Progress Properties ============
    @Property(int, notify=progressChanged)
    def progress(self) -> int:
        return self._progress
    
    @Property(str, notify=statusChanged)
    def statusMessage(self) -> str:
        return self._status_message
    
    @Property(bool, notify=processingChanged)
    def isProcessing(self) -> bool:
        return self._is_processing
    
    # ============ Time Range Properties ============
    @Property(str, notify=timeRangeChanged)
    def startTime(self) -> str:
        return self._start_time
    
    @startTime.setter
    def startTime(self, value: str) -> None:
        if self._start_time != value:
            self._start_time = value
            self.timeRangeChanged.emit()
    
    @Property(str, notify=timeRangeChanged)
    def endTime(self) -> str:
        return self._end_time
    
    @endTime.setter
    def endTime(self, value: str) -> None:
        if self._end_time != value:
            self._end_time = value
            self.timeRangeChanged.emit()
    
    # ============ Slots (Methods callable from QML) ============
    @Slot(QUrl)
    def loadVideo(self, file_url: QUrl) -> None:
        """Load video file and extract metadata."""
        # Convert QUrl to file path
        file_path = file_url.toLocalFile()
        
        if not file_path or not os.path.exists(file_path):
            self.showMessage.emit("Hata", "Dosya bulunamadı.", True)
            return
        
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                raise IOError("Video dosyası açılamadı veya bozuk.")
            
            # Extract video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Validate FPS
            if fps is None or fps <= 0 or fps > 1000:
                fps = 30.0
            
            duration_seconds = frame_count / fps if fps > 0 else 0
            file_size_bytes = os.path.getsize(file_path)
            
            cap.release()
            
            # Update properties
            self._video_path = file_path
            self._resolution = f"{width} × {height} px"
            self._duration = format_duration(duration_seconds)
            self._fps = fps
            self._frame_count = frame_count
            self._file_size = format_size(file_size_bytes)
            self._video_duration = int(duration_seconds)
            self._start_time = "00:00:00"
            self._end_time = format_duration(duration_seconds)
            
            # Emit all signals
            self.videoPathChanged.emit()
            self.videoInfoChanged.emit()
            self.timeRangeChanged.emit()
            
            self._update_status("Video başarıyla yüklendi.")
            
        except Exception as e:
            self.showMessage.emit("Hata", f"Video bilgileri okunurken hata: {e}", True)
    
    @Slot(int, int)
    def setTimeRange(self, low_sec: int, high_sec: int) -> None:
        """Update time range from slider."""
        self._start_time = format_duration(low_sec)
        self._end_time = format_duration(high_sec)
        self.timeRangeChanged.emit()
    
    @Slot(str)
    def startProcessing(self, mode: str) -> None:
        """Start the frame extraction process."""
        if not self._video_path:
            self.showMessage.emit("Uyarı", "Lütfen önce bir video dosyası seçin.", True)
            return
        
        if self._is_processing:
            self.showMessage.emit("Bilgi", "Zaten devam eden bir işlem var.", False)
            return
        
        # Prepare kwargs
        kwargs = {}
        if mode == "range":
            kwargs["start_time"] = self._start_time
            kwargs["end_time"] = self._end_time
        
        # Update UI state
        self._is_processing = True
        self._progress = 0
        self.processingChanged.emit()
        self.progressChanged.emit()
        
        # Create and start worker
        self._worker = ProcessingWorker(
            video_path=self._video_path,
            output_dir=self._output_dir,
            mode=mode,
            **kwargs
        )
        
        # Connect signals
        self._worker.progress_update.connect(self._on_progress_update)
        self._worker.status_update.connect(self._update_status)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        
        self._worker.start()
    
    @Slot()
    def cancelProcessing(self) -> None:
        """Cancel the current processing operation."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()
            self._worker.wait(2000)  # Wait up to 2 seconds
            
            if self._worker.isRunning():
                self._worker.terminate()
                self._worker.wait()
            
            self._is_processing = False
            self._progress = 0
            self.processingChanged.emit()
            self.progressChanged.emit()
            self._update_status("İşlem iptal edildi.")
            self.showMessage.emit("Bilgi", "İşlem kullanıcı tarafından iptal edildi.", False)
    
    # ============ Private Methods ============
    def _update_status(self, message: str) -> None:
        self._status_message = message
        self.statusChanged.emit()
    
    def _on_progress_update(self, value: int) -> None:
        self._progress = value
        self.progressChanged.emit()
    
    def _on_finished(self, message: str) -> None:
        self._is_processing = False
        self._progress = 100
        self.processingChanged.emit()
        self.progressChanged.emit()
        self._update_status(message)
        self.showMessage.emit("Başarılı", message, False)
    
    def _on_error(self, error_message: str) -> None:
        self._is_processing = False
        self._progress = 0
        self.processingChanged.emit()
        self.progressChanged.emit()
        self._update_status("Hata oluştu. Lütfen tekrar deneyin.")
        self.showMessage.emit("Hata", f"İşlem sırasında hata: {error_message}", True)
