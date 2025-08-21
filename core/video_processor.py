import cv2
import os
from pathlib import Path

class VideoProcessor:
    """Video işleme ile ilgili tüm mantığı içeren sınıf."""
    
    def __init__(self, video_path, output_dir, mode, signals, **kwargs):
        self.video_path = video_path
        self.output_dir = output_dir
        self.mode = mode
        self.signals = signals  # İletişim için worker'dan gelen sinyal nesnesi
        self.kwargs = kwargs    # 'range' modu için başlangıç/bitiş zamanları gibi ek argümanlar

    def _setup_output_directory(self):
        """Çıktı dizinini hazırlar. Belirtilmemişse varsayılan bir tane oluşturur."""
        if not self.output_dir:
            # Eğer kullanıcı bir dizin seçmediyse, masaüstünde video adıyla bir klasör oluştur
            video_name = Path(self.video_path).stem
            desktop_path = Path.home() / "Desktop"
            self.output_dir = desktop_path / video_name
        
        # Klasörün var olduğundan emin ol
        os.makedirs(self.output_dir, exist_ok=True)
        return self.output_dir

    def _time_to_frame(self, time_str, fps):
        """'HH:mm:ss' formatındaki zamanı frame numarasına çevirir."""
        h, m, s = map(int, time_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
        return int(total_seconds * fps)

    def run(self):
        """Ana video işleme döngüsünü çalıştırır."""
        output_path = self._setup_output_directory()
        self.signals.status_update.emit(f"Video açılıyor: {Path(self.video_path).name}")

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError("Video dosyası açılamadı. Dosya yolunu veya formatını kontrol edin.")
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        start_frame = 0
        end_frame = total_frames

        if self.mode == 'range':
            start_frame = self._time_to_frame(self.kwargs.get('start_time', '00:00:00'), fps)
            end_frame = self._time_to_frame(self.kwargs.get('end_time', '99:99:99'), fps)
        
        # --- Sahne Değişimi Tespiti için İlk Ayarlar ---
        prev_hist = None
        # Bu eşik değeri, iki frame arasındaki farkın ne kadar olması gerektiğini belirtir.
        # Düşük değerler daha hassas, yüksek değerler daha az hassas tespit yapar.
        SCENE_CHANGE_THRESHOLD = 0.7 
        
        saved_frame_count = 0
        current_frame = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break # Video bitti veya okuma hatası

            if current_frame >= start_frame and current_frame < end_frame:
                should_save = False
                if self.mode == 'all':
                    should_save = True

                elif self.mode == 'range':
                    should_save = True
                
                elif self.mode == 'scene':
                    # Frame'i gri tonlamaya çevirip histogramını hesapla
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
                    cv2.normalize(hist, hist) # Histogramı normalize et

                    if prev_hist is not None:
                        # İki histogram arasındaki korelasyonu (benzerliği) ölç
                        score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                        if score < SCENE_CHANGE_THRESHOLD:
                            should_save = True # Benzerlik eşik değerinin altındaysa, bu bir sahne değişimidir.
                    else:
                        # Her zaman ilk frame'i kaydet
                        should_save = True
                    
                    prev_hist = hist

                if should_save:
                    saved_frame_count += 1
                    save_path = os.path.join(output_path, f"frame_{saved_frame_count:06d}.jpg")
                    cv2.imwrite(save_path, frame)

            current_frame += 1
            
            # Arayüze ilerleme durumunu gönder
            progress_percent = int((current_frame / total_frames) * 100)
            self.signals.progress_update.emit(progress_percent)
            self.signals.status_update.emit(f"İşleniyor... Frame {current_frame}/{total_frames}")

        cap.release()
        return f"İşlem tamamlandı! '{output_path}' klasörüne {saved_frame_count} adet frame kaydedildi."