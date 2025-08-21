# FrameExtractor/ui/range_slider.py

from PyQt5.QtWidgets import QWidget, QStyle, QSlider, QStyleOptionSlider
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush

class RangeSlider(QWidget):
    """Görsel olarak iyileştirilmiş çift taraflı kaydırıcı."""
    
    valueChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(28) # Yüksekliği ayarladık
        self._min = 0
        self._max = 100
        self._low = 0
        self._high = 100
        
        self._low_handle_pressed = False
        self._high_handle_pressed = False
        self.handle_radius = 8 # Tutamaç yarıçapı

    # ... (setRange, setLow, setHigh, low, high metodları aynı kalacak) ...
    def setRange(self, mini, maxi):
        self._min = mini
        self._max = maxi
        if self._max <= self._min: self._max = self._min + 1
        self.update()

    def setLow(self, val):
        val = round(val)
        if val < self._min: val = self._min
        if val > self._high: val = self._high
        self._low = val
        self.update()

    def setHigh(self, val):
        val = round(val)
        if val > self._max: val = self._max
        if val < self._low: val = self._low
        self._high = val
        self.update()

    def low(self): return self._low
    def high(self): return self._high


    # YENİ VE İYİLEŞTİRİLMİŞ ÇİZİM METODU
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect().adjusted(self.handle_radius, 0, -self.handle_radius, 0)
        center_y = rect.center().y()
        
        # 1. Arka plan çubuğu (yeni renk)
        painter.setPen(QPen(QColor(0, 0, 0, 60), 3, Qt.SolidLine, Qt.RoundCap)) # Yarı saydam siyah
        painter.drawLine(rect.left(), center_y, rect.right(), center_y)
        
        low_pos = self._value_to_pos(self._low, rect)
        high_pos = self._value_to_pos(self._high, rect)

        # 2. Seçili aralık (yeni vurgu rengi)
        painter.setPen(QPen(QColor("#00D1FF"), 4, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(low_pos), center_y, int(high_pos), center_y)

        # 3. Başlangıç ve bitiş tutamaçları
        self._draw_handle(painter, int(low_pos), center_y)
        self._draw_handle(painter, int(high_pos), center_y)

    # YENİ TUTAMAÇ ÇİZİM METODU
    def _draw_handle(self, painter, pos_x, pos_y):
        # Dış çerçeve (yeni renk)
        painter.setPen(QPen(QColor("#E0E0E0"), 2))
        # İç dolgu (yeni vurgu rengi)
        painter.setBrush(QBrush(QColor("#00D1FF")))
        painter.drawEllipse(QPoint(pos_x, pos_y), self.handle_radius - 1, self.handle_radius - 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = self.rect().adjusted(self.handle_radius, 0, -self.handle_radius, 0)
            low_pos = self._value_to_pos(self._low, rect)
            high_pos = self._value_to_pos(self._high, rect)

            dist_low = abs(event.pos().x() - low_pos)
            dist_high = abs(event.pos().x() - high_pos)
            
            # Hangi tutamaç daha yakınsa onu aktif et
            if dist_low <= self.handle_radius and dist_low < dist_high:
                self._low_handle_pressed = True
            elif dist_high <= self.handle_radius:
                self._high_handle_pressed = True
    
    # ... (_value_to_pos, _pos_to_value, mouseMoveEvent, mouseReleaseEvent aynı kalacak) ...
    def _value_to_pos(self, value, rect):
        span = self._max - self._min
        if span == 0: return float(rect.left())
        return float(rect.left() + rect.width() * (value - self._min) / span)

    def _pos_to_value(self, pos_x, rect):
        span = self._max - self._min
        offset = float(pos_x - rect.left())
        if rect.width() == 0: return self._min
        return self._min + span * max(0.0, min(1.0, offset / rect.width()))

    def mouseMoveEvent(self, event):
        if self._low_handle_pressed or self._high_handle_pressed:
            rect = self.rect().adjusted(self.handle_radius, 0, -self.handle_radius, 0)
            new_val = self._pos_to_value(event.pos().x(), rect)

            if self._low_handle_pressed: self.setLow(new_val)
            elif self._high_handle_pressed: self.setHigh(new_val)
            
            self.valueChanged.emit(self._low, self._high)

    def mouseReleaseEvent(self, event):
        self._low_handle_pressed = False
        self._high_handle_pressed = False