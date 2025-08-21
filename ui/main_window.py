# FrameExtractor/ui/main_window.py

import sys
import os
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QPushButton, QLineEdit, QLabel, QRadioButton,
                             QProgressBar, QFormLayout, QTimeEdit, QFileDialog, QMessageBox,
                             QGraphicsDropShadowEffect, QScrollArea)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont, QColor
from threads.worker import ProcessingWorker
from ui.range_slider import RangeSlider

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frame Extractor")
        
        self.video_path = None
        self.worker = None

        self.setStyleSheet("""
            /* Ana Pencere ve Arka Plan */
            #MainWindow, QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #1E1B32, stop:1 #342F5C);
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            /* Grup Kutuları (Glassmorphism Etkisi) */
            QGroupBox {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                font-size: 12pt;
                font-weight: bold;
                color: #E0E0E0;
                margin-top: 1ex;
                padding: 20px 15px 15px 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 0 10px; margin-left: 10px; color: #CCCCCC;
            }
            /* Butonlar */
            QPushButton {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px; padding: 8px 12px;
                color: #E0E0E0; font-size: 10pt;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.12); }
            QPushButton:pressed { background-color: rgba(0, 0, 0, 0.05); }
            /* Ana İşlem Butonu */
            QPushButton#StartButton {
                background-color: #00D1FF; color: #1E1B32;
                font-weight: bold; font-size: 12pt; border: none;
            }
            QPushButton#StartButton:hover { background-color: #50E3FF; }
            QPushButton#StartButton:pressed { background-color: #00B4CC; }
            /* Metin Giriş Alanları */
            QLineEdit, QTimeEdit {
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px; padding: 6px;
                color: #E0E0E0; font-size: 10pt;
            }
            QLineEdit:focus, QTimeEdit:focus { border-color: #00D1FF; }
            /* İlerleme Çubuğu */
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px; text-align: center;
                color: white; background-color: rgba(0, 0, 0, 0.2);
            }
            QProgressBar::chunk {
                background-color: #00D1FF; border-radius: 6px; margin: 2px;
            }
            /* Etiketler ve Radyo Butonlar */
            QLabel, QRadioButton {
                background-color: transparent; color: #E0E0E0; font-size: 10pt;
            }
            #InfoLabel {
                color: #AAAAAA; font-size: 9pt; font-style: italic;
                padding-top: 5px; border: none; background: none;
            }
            #VideoInfoLabel {
                background: rgba(0, 0, 0, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px; padding: 15px;
            }
            /* Kaydırma Çubuğu (Scrollbar) Stili */
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none; background-color: rgba(0, 0, 0, 0.15);
                width: 10px; margin: 0px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #00D1FF; min-height: 20px; border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none; background: none; height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }             
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(scroll_area)

        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)
        # --- DÜZELTME: scroll_content_widget'e objectName atandı ---
        scroll_content_widget.setObjectName("MainWindow")

        main_layout = QVBoxLayout(scroll_content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.video_selection_group = self._create_video_selection_group()
        self.output_dir_group = self._create_output_dir_group()
        self.options_group = self._create_options_group()
        self.info_group = self._create_info_group()

        for group_box in [self.video_selection_group, self.output_dir_group, self.options_group, self.info_group]:
            self._apply_shadow_effect(group_box)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        top_layout.addWidget(self.video_selection_group)
        top_layout.addWidget(self.output_dir_group)
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.options_group)
        main_layout.addWidget(self.info_group)

        self.start_button = QPushButton("İşlemi Başlat")
        self.start_button.setObjectName("StartButton")
        self.start_button.setFixedHeight(45)
        self.start_button.setFont(QFont('Segoe UI', 12, QFont.Bold))
        main_layout.addWidget(self.start_button)
        
        main_layout.addStretch()

        self.progress_bar.hide()
        
        self._connect_signals()
        # 1. Makul bir minimum boyut belirle (kullanıcının pencereyi tamamen kaybetmesini önler)
        self.setMinimumSize(850, 650)
        
        # 2. İçeriğin ideal yüksekliğini hesapla ve biraz pay ekle
        ideal_height = main_layout.sizeHint().height() + 30 # 30 piksel estetik pay
        
        # 3. Pencereyi bu ideal boyuta yeniden boyutlandır
        self.resize(850, ideal_height)
    
    def _apply_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(4, 4)
        widget.setGraphicsEffect(shadow)

    # --- BU METODUN VAR OLDUĞUNDAN EMİN OLUN ---
    def _create_video_selection_group(self):
        group_box = QGroupBox("1. Video Seçimi 🎥")
        layout = QVBoxLayout()
        layout.setSpacing(15)

        file_path_layout = QHBoxLayout()
        self.video_path_line = QLineEdit()
        self.video_path_line.setPlaceholderText("🎥 Lütfen bir video dosyası seçin...")
        self.video_path_line.setReadOnly(True)
        self.select_video_button = QPushButton("...")
        file_path_layout.addWidget(self.video_path_line)
        file_path_layout.addWidget(self.select_video_button)
        layout.addLayout(file_path_layout)

        self.video_info_label = QLabel("📊 Video yüklendikten sonra bilgiler burada görünecek.")
        self.video_info_label.setObjectName("VideoInfoLabel")
        self.video_info_label.setWordWrap(True)
        self.video_info_label.setAlignment(Qt.AlignTop)
        self.video_info_label.setMinimumHeight(180) # Yüksekliği biraz artırdık
        layout.addWidget(self.video_info_label)
        
        group_box.setLayout(layout)
        return group_box

    def _create_output_dir_group(self):
        group_box = QGroupBox("2. Çıktı Dizini 🗂️ ")
        layout = QVBoxLayout()
        
        file_path_layout = QHBoxLayout()
        self.output_dir_line = QLineEdit()
        self.output_dir_line.setPlaceholderText("📂 İsteğe bağlı: Çıktı klasörünü seçin...")
        self.select_output_dir_button = QPushButton("...")
        file_path_layout.addWidget(self.output_dir_line)
        file_path_layout.addWidget(self.select_output_dir_button)
        layout.addLayout(file_path_layout)

        info_label = QLabel("📄 Seçim yapılmazsa, klasör masaüstünde video adıyla oluşturulur.")
        info_label.setObjectName("InfoLabel")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addStretch()
        group_box.setLayout(layout)
        return group_box
    
    # --- BU METODUN TEK BİR KOPYASI OLDUĞUNDAN EMİN OLUN ---
    def _create_options_group(self):
        group_box = QGroupBox("3. Ayırma Seçenekleri ⚙️")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        self.radio_all_frames = QRadioButton("🎬 Videonun tüm framelerini ayır")
        self.radio_time_range = QRadioButton("⏰ Belirli bir zaman aralığını ayır")
        self.radio_scene_change = QRadioButton("🎭 Sahne değişimlerini algıla ve ayır")

        self.time_range_widget = QWidget()
        time_range_layout = QHBoxLayout(self.time_range_widget)
        time_range_layout.setContentsMargins(20, 10, 20, 0)
        
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.range_slider = RangeSlider()
        
        time_range_layout.addWidget(QLabel("⏩Başlangıç:"))
        time_range_layout.addWidget(self.start_time_edit)
        time_range_layout.addStretch(1)
        time_range_layout.addWidget(self.range_slider, 10)
        time_range_layout.addStretch(1)
        time_range_layout.addWidget(QLabel("⏹️Bitiş:"))
        time_range_layout.addWidget(self.end_time_edit)
        
        self.time_range_widget.setEnabled(False) 
        
        main_layout.addWidget(self.radio_all_frames)
        main_layout.addWidget(self.radio_time_range)
        main_layout.addWidget(self.time_range_widget)
        main_layout.addWidget(self.radio_scene_change)
        
        self.radio_all_frames.setChecked(True)
        group_box.setLayout(main_layout)
        return group_box

    def _create_info_group(self):
        group_box = QGroupBox("4. Bilgilendirme ve Durum")
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Durum: Başlamak için bir video seçin.")
        self.progress_bar = QProgressBar()
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        
        group_box.setLayout(layout)
        return group_box

    def _connect_signals(self):
        self.select_video_button.clicked.connect(self.select_video_file)
        self.select_output_dir_button.clicked.connect(self.select_output_folder)
        self.start_button.clicked.connect(self.start_processing)
        
        self.radio_time_range.toggled.connect(self.time_range_widget.setEnabled)
        
        self.range_slider.valueChanged.connect(self.update_times_from_slider)
        self.start_time_edit.timeChanged.connect(self.update_slider_from_times)
        self.end_time_edit.timeChanged.connect(self.update_slider_from_times)

    def select_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Video Dosyası Seç", "", "Video Dosyaları (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.video_path = file_path
            self.video_path_line.setText(file_path)
            self.load_video_info()

    def select_output_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Çıktı Klasörü Seç")
        if dir_path:
            self.output_dir_line.setText(dir_path)

    def load_video_info(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise IOError("Video dosyası açılamadı veya bozuk.")

            # Tüm video metriklerini al
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # --- KESİN DÜZELTME: FPS Sağlamlık Kontrolü ---
            # Eğer OpenCV FPS değerini okuyamazsa (0 veya geçersiz bir değer döndürürse),
            # makul bir varsayılan değer kullan. Bu, sürenin 0 olmasını engeller.
            if fps is None or fps <= 0 or fps > 1000:
                fps = 30.0  # Varsayılan değer olarak 30 FPS ata
            # --- DÜZELTME BİTTİ ---
                
            duration_seconds = frame_count / fps if fps > 0 else 0
            file_size_bytes = os.path.getsize(self.video_path)
            cap.release()

            # Verileri formatla ve hesapla
            duration_str = self._format_duration(duration_seconds)
            file_size_str = self._format_size(file_size_bytes)
            from math import gcd
            r = gcd(width, height)
            aspect_ratio = f"{width//r}:{height//r}"
            
            # HTML şablonunu oluştur (ikonlar değiştirildi)
            info_html = f"""
            <h3 style='color: #E0E0E0; margin: 0 0 12px 0; font-size: 14pt;'>📊 Video Analizi</h3>
            <table width='100%' style='font-size: 10pt; border-spacing: 0 8px;'>
                <tr>
                    <td style='color: #CCCCCC;'>📏 <b>Çözünürlük:</b></td>
                    <td style='color: #00D1FF; font-weight: bold; text-align: right;'>{width} × {height} px</td>
                </tr>
                <tr>
                    <td style='color: #CCCCCC;'>⏱️ <b>Süre:</b></td>
                    <td style='color: #50E3C2; font-weight: bold; text-align: right;'>{duration_str}</td>
                </tr>
                <tr>
                    <td style='color: #CCCCCC;'>🎞️ <b>FPS (Kare Hızı):</b></td>
                    <td style='color: #FFD600; font-weight: bold; text-align: right;'>{fps:.2f}</td>
                </tr>
                <tr>
                    <td style='color: #CCCCCC;'>📦 <b>Toplam Frame:</b></td>
                    <td style='color: #B298DC; font-weight: bold; text-align: right;'>{frame_count:,}</td>
                </tr>
                <tr>
                    <td style='color: #CCCCCC;'>💾 <b>Dosya Boyutu:</b></td>
                    <td style='color: #CCCCCC; font-weight: bold; text-align: right;'>{file_size_str}</td>
                </tr>
                <tr>
                    <td style='color: #CCCCCC;'>📐 <b>En-Boy Oranı:</b></td>
                    <td style='color: #9E9E9E; font-weight: bold; text-align: right;'>{aspect_ratio}</td>
                </tr>
            </table>
            """
            self.video_info_label.setText(info_html)

            # Range slider ve zaman editörlerini ayarla
            self.range_slider.setRange(0, int(duration_seconds))
            self.range_slider.setLow(0)
            self.range_slider.setHigh(int(duration_seconds))

            max_time = QTime.fromString(self._format_duration(duration_seconds), "HH:mm:ss")
            self.start_time_edit.setMaximumTime(max_time)
            self.end_time_edit.setMaximumTime(max_time)
            self.end_time_edit.setTime(max_time)
            self.start_time_edit.setTime(QTime(0, 0, 0))

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Video bilgileri okunurken bir hata oluştu:\n{e}")
            self._reset_video_info()

    def start_processing(self):
        if not self.video_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir video dosyası seçin.")
            return

        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "Bilgi", "Zaten devam eden bir işlem var.")
            return
        
        output_dir = self.output_dir_line.text()
        mode = "all"
        kwargs = {}

        if self.radio_time_range.isChecked():
            mode = "range"
            start_sec = self.range_slider.low()
            end_sec = self.range_slider.high()
            kwargs['start_time'] = self._format_duration(start_sec)
            kwargs['end_time'] = self._format_duration(end_sec)
        elif self.radio_scene_change.isChecked():
            mode = "scene"
        
        # --- DÜZELTME: Tekrarlar kaldırıldı ---
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self._toggle_ui_elements(False)

        self.worker = ProcessingWorker(
            video_path=self.video_path, output_dir=output_dir, mode=mode, **kwargs)
        
        self.worker.progress_update.connect(self.update_progress_bar)
        self.worker.status_update.connect(self.update_status_label)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        
        self.worker.start()

    def _reset_video_info(self):
        self.video_path = None
        self.video_path_line.clear()
        self.video_info_label.setText("📊 Video yüklendikten sonra bilgiler burada görünecek.")

    def _format_duration(self, seconds):
        if seconds < 0: return "00:00:00"
        h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _format_size(self, size_bytes):
        if size_bytes == 0: return "0 B"
        import math
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def _toggle_ui_elements(self, enabled):
        self.video_selection_group.setEnabled(enabled)
        self.output_dir_group.setEnabled(enabled)
        self.options_group.setEnabled(enabled)
        self.start_button.setEnabled(enabled)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_status_label(self, message):
        self.status_label.setText(f"Durum: {message}")

    def on_processing_finished(self, message):
        QMessageBox.information(self, "Başarılı", message)
        self.status_label.setText(f"Durum: {message}")
        self._toggle_ui_elements(True)
        self.progress_bar.setValue(100)
        self.progress_bar.hide()

    def on_processing_error(self, error_message):
        QMessageBox.critical(self, "Hata", f"İşlem sırasında bir hata oluştu:\n{error_message}")
        self.status_label.setText("Durum: Hata oluştu. Lütfen tekrar deneyin.")
        self._toggle_ui_elements(True)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

    def update_times_from_slider(self, low_sec, high_sec):
        self.start_time_edit.blockSignals(True)
        self.end_time_edit.blockSignals(True)
        self.start_time_edit.setTime(QTime.fromString(self._format_duration(low_sec), "HH:mm:ss"))
        self.end_time_edit.setTime(QTime.fromString(self._format_duration(high_sec), "HH:mm:ss"))
        self.start_time_edit.blockSignals(False)
        self.end_time_edit.blockSignals(False)

    def update_slider_from_times(self):
        self.range_slider.blockSignals(True)
        start_time = self.start_time_edit.time()
        end_time = self.end_time_edit.time()
        if start_time > end_time:
            self.start_time_edit.setTime(end_time)
            start_time = end_time
        start_sec = QTime(0, 0, 0).secsTo(start_time)
        end_sec = QTime(0, 0, 0).secsTo(end_time)
        self.range_slider.setLow(start_sec)
        self.range_slider.setHigh(end_sec)
        self.range_slider.blockSignals(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())