from PyQt5.QtCore import QThread, pyqtSignal
from core.video_processor import VideoProcessor # core paketimizden VideoProcessor'ı import ediyoruz

class ProcessingWorker(QThread):
    # Arayüzle iletişim kurmak için sinyalleri tanımla
    finished = pyqtSignal(str)          # İşlem bittiğinde (başarıyla)
    error = pyqtSignal(str)             # Hata oluştuğunda
    progress_update = pyqtSignal(int)   # İlerleme çubuğu için (0-100)
    status_update = pyqtSignal(str)     # Durum etiketi için metin

    def __init__(self, video_path, output_dir, mode, **kwargs):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.mode = mode
        self.kwargs = kwargs

    def run(self):
        """QThread başlatıldığında bu metod otomatik olarak çalışır."""
        try:
            # VideoProcessor'ı oluştur ve sinyal nesnesi olarak kendimizi (worker'ı) ver
            processor = VideoProcessor(
                video_path=self.video_path,
                output_dir=self.output_dir,
                mode=self.mode,
                signals=self, # Bu sayede processor sinyallerimizi tetikleyebilir
                **self.kwargs
            )
            # Asıl işi başlat
            result_message = processor.run()
            
            # İş bittiğinde 'finished' sinyalini yayınla
            self.finished.emit(result_message)
            
        except Exception as e:
            # Herhangi bir hata olursa 'error' sinyalini yayınla
            self.error.emit(str(e))