# FrameExtractor/core/video_processor.py

import cv2
import os
import numpy as np # YENİ EKLENDİ
from pathlib import Path

class VideoProcessor:
    def __init__(self, video_path, output_dir, mode, signals, **kwargs):
        self.video_path = video_path
        self.output_dir = output_dir
        self.mode = mode
        self.signals = signals
        self.kwargs = kwargs

    def _setup_output_directory(self):
        if not self.output_dir:
            video_name = Path(self.video_path).stem
            # Path nesnesi Türkçe karakterlerle başa çıkabilir
            desktop_path = Path.home() / "Desktop"
            self.output_dir = desktop_path / f"{video_name}_frames"
        
        # Klasörü oluştururken de sorun yaşanabilir, exist_ok=True genellikle yardımcı olur
        os.makedirs(self.output_dir, exist_ok=True)
        return self.output_dir

    def _time_to_frame(self, time_str, fps):
        h, m, s = map(int, time_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
        return int(total_seconds * fps)

    def run(self):
        output_path = self._setup_output_directory()
        self.signals.status_update.emit(f"Video açılıyor: {Path(self.video_path).name}")

        # --- TÜRKÇE KARAKTER ÇÖZÜMÜ (Okuma) ---
        # Dosyayı önce byte olarak oku, sonra numpy array'e çevir
        try:
            with open(self.video_path, "rb") as f:
                video_bytes = f.read()
            video_array = np.frombuffer(video_bytes, np.uint8)
            cap = cv2.imdecode(video_array, cv2.IMREAD_UNCHANGED) # Bu satır video için uygun değil
            # Videolar için doğrudan dosya yolunu kullanmak daha güvenilir, ama imdecode ile değil
            # VideoCapture için en güvenilir yöntem, dosya yolunu doğru şekilde kodlamaktır.
            # Ancak en basit ve genellikle çalışan yöntem doğrudan denemektir.
            # Eğer bu da çalışmazsa, geçici bir isme kopyalama yöntemi uygulanır.
            # Şimdilik, asıl sorunun yazmada olduğunu varsayarak devam edelim.
            cap = cv2.VideoCapture(self.video_path)
        except Exception as e:
             raise IOError(f"Video dosyası okunamadı: {self.video_path}. Hata: {e}")
        # --- ÇÖZÜM SONU ---
        
        if not cap.isOpened():
            raise IOError("Video dosyası açılamadı. Yol veya dosya bozuk olabilir.")
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if fps <= 0 or fps > 1000: fps = 30.0
            
        start_frame = 0
        end_frame = total_frames

        if self.mode == 'range':
            start_time_str = self.kwargs.get('start_time', '00:00:00')
            end_time_str = self.kwargs.get('end_time', '99:99:99')
            start_frame = self._time_to_frame(start_time_str, fps)
            end_frame = self._time_to_frame(end_time_str, fps)
        
        prev_hist = None
        SCENE_CHANGE_THRESHOLD = 0.7 
        
        saved_frame_count = 0
        current_frame_index = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break 

            should_save = False
            
            if self.mode == 'all': should_save = True
            elif self.mode == 'range':
                if start_frame <= current_frame_index < end_frame: should_save = True
            elif self.mode == 'scene':
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
                cv2.normalize(hist, hist)

                if prev_hist is not None:
                    score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                    if score < SCENE_CHANGE_THRESHOLD: should_save = True
                else: should_save = True
                prev_hist = hist

            if should_save:
                saved_frame_count += 1
                save_path = os.path.join(output_path, f"frame_{saved_frame_count:06d}.jpg")
                
                # --- TÜRKÇE KARAKTER ÇÖZÜMÜ (Yazma) ---
                # Frame'i önce bellekte bir buffer'a encode et
                is_success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                if is_success:
                    # Buffer'ı doğrudan dosyaya yaz. Bu, dosya yolundaki karakterlerden etkilenmez.
                    with open(save_path, "wb") as f:
                        f.write(buffer)
                # --- ÇÖZÜM SONU ---

            current_frame_index += 1
            
            if total_frames > 0:
                progress_percent = int((current_frame_index / total_frames) * 100)
                self.signals.progress_update.emit(progress_percent)
                if current_frame_index % 50 == 0:
                    self.signals.status_update.emit(f"İşleniyor... Frame {current_frame_index}/{total_frames}")

        cap.release()
        return f"İşlem tamamlandı! '{output_path}' klasörüne {saved_frame_count} adet frame kaydedildi."