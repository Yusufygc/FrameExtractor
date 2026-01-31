# 🎬 Frame Extractor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-6.5+-green.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/OpenCV-4.0+-red.svg" alt="OpenCV">
</p>

<p align="center">
  <strong>Modern, hızlı ve kullanıcı dostu video frame ayırma uygulaması</strong>
</p>

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Mimari](#-mimari)
- [Geliştirme](#-geliştirme)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 🎯 Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| **🎬 Tüm Frame'leri Ayır** | Videonun her karesini JPEG olarak kaydet |
| **⏰ Zaman Aralığı** | Belirli bir zaman dilimindeki frame'leri çıkar |
| **🎭 Sahne Değişimi Algılama** | Histogram tabanlı sahne geçişlerini otomatik tespit et |
| **❌ İptal Desteği** | İşlem sırasında istediğiniz zaman iptal edin |

### 🎨 Modern Arayüz

- **Glassmorphism tasarım** - Yarı şeffaf, modern görünüm
- **Gradient arka plan** - Göz yormayan mor tonları
- **Hover animasyonları** - Etkileşimli butonlar
- **Gerçek zamanlı ilerleme** - Frame bazında progress takibi

### ⚡ Performans

- **Doğrudan seek** - Zaman aralığında gereksiz frame okumaz
- **Optimized JPEG** - %95 kaliteli sıkıştırma
- **Unicode yol desteği** - Türkçe karakter içeren klasörler sorunsuz çalışır
- **Arka plan işleme** - UI donmadan çalışır

---

## 📸 Ekran Görüntüleri

```
<p align="center">
  <img src="https://raw.githubusercontent.com/Yusufygc/FrameExtractor/main/resources/image.png" width="700">
</p>
<p align="center"><b>Frame Extractor – Modern QML Arayüz</b></p>

```

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- Windows 10/11 (macOS ve Linux test edilmedi)

### Adımlar

1. **Depoyu klonlayın**
   ```bash
   git clone https://github.com/Yusufygc/FrameExtractor.git
   cd FrameExtractor
   ```

2. **Sanal ortam oluşturun (önerilen)**
   ```bash
   # Conda ile
   conda create -n FrameAyirici python=3.11
   conda activate FrameAyirici
   
   # veya venv ile
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **Uygulamayı çalıştırın**
   ```bash
   python main.py
   ```

---

## 📖 Kullanım

### 1. Video Seçimi
- `...` butonuna tıklayarak video dosyası seçin
- Desteklenen formatlar: MP4, AVI, MOV, MKV

### 2. Çıktı Dizini (İsteğe Bağlı)
- Boş bırakılırsa: `Masaüstü/[video_adı]_frames/` oluşturulur

### 3. Ayırma Modu Seçin

| Mod | Kullanım Durumu |
|-----|-----------------|
| **Tüm Frameler** | Her kareyi kaydetmek istediğinizde |
| **Zaman Aralığı** | Belirli bir sahneyi çıkarmak için |
| **Sahne Değişimi** | Otomatik sahne algılama için |

### 4. İşlemi Başlatın
- `🚀 İşlemi Başlat` butonuna tıklayın
- İlerlemeyi takip edin
- Gerekirse `❌ İptal Et` ile durdurun

---

## 📁 Proje Yapısı

```
Frame_Ayirici/
├── main.py                 # Uygulama giriş noktası
├── requirements.txt        # Python bağımlılıkları
│
├── core/                   # İş mantığı katmanı
│   ├── __init__.py
│   ├── protocols.py        # SignalProtocol (DIP)
│   ├── video_processor.py  # Ana işleyici
│   └── strategies/         # Strateji deseni
│       ├── __init__.py
│       ├── base.py         # Soyut strateji
│       ├── all_frames.py   # Tüm frameler
│       ├── time_range.py   # Zaman aralığı
│       └── scene_change.py # Sahne algılama
│
├── ui/                     # Kullanıcı arayüzü
│   ├── __init__.py
│   └── backend.py          # Python-QML köprüsü
│
├── qml/                    # QML arayüz dosyaları
│   ├── Main.qml            # Ana pencere
│   └── components/         # Yeniden kullanılabilir bileşenler
│       ├── qmldir
│       ├── GlassCard.qml
│       ├── PrimaryButton.qml
│       ├── SecondaryButton.qml
│       ├── StyledTextField.qml
│       ├── StyledRadioButton.qml
│       ├── ProgressBar.qml
│       └── RangeSlider.qml
│
├── threads/                # Arka plan işleme
│   ├── __init__.py
│   └── worker.py           # QThread işçisi
│
├── utils/                  # Yardımcı fonksiyonlar
│   ├── __init__.py
│   └── formatters.py       # Süre, boyut formatlama
│
└── styles/                 # Tema yapılandırması
    ├── __init__.py
    └── theme.py            # Renk, boyut sabitleri
```

---

## 🏗️ Mimari

### SOLID Prensipleri

| Prensip | Uygulama |
|---------|----------|
| **Single Responsibility** | Her sınıf tek bir işe odaklı |
| **Open/Closed** | Yeni stratejiler kolayca eklenebilir |
| **Dependency Inversion** | `SignalProtocol` ile bağımlılık tersine çevrildi |

### Tasarım Desenleri

```
┌─────────────────┐     ┌───────────────────┐
│   QML Frontend  │◄───►│  Backend (Python) │
└─────────────────┘     └─────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              ┌─────▼─────┐              ┌──────▼──────┐
              │  Worker   │              │ VideoProc.  │
              │ (QThread) │─────────────►│             │
              └───────────┘              └──────┬──────┘
                                               │
                          ┌────────────────────┼────────────────────┐
                          │                    │                    │
                   ┌──────▼──────┐     ┌───────▼───────┐    ┌───────▼───────┐
                   │ AllFrames   │     │  TimeRange    │    │ SceneChange   │
                   │  Strategy   │     │   Strategy    │    │   Strategy    │
                   └─────────────┘     └───────────────┘    └───────────────┘
```

---

## 🛠️ Geliştirme

### Yeni Strateji Ekleme

1. `core/strategies/` altında yeni dosya oluşturun
2. `ExtractionStrategy` sınıfından türetin
3. `should_save_frame()` metodunu uygulayın
4. `video_processor.py`'deki `STRATEGIES` sözlüğüne ekleyin

```python
# core/strategies/my_strategy.py
from .base import ExtractionStrategy

class MyStrategy(ExtractionStrategy):
    @property
    def name(self) -> str:
        return "My Custom Strategy"
    
    def should_save_frame(self, frame, frame_index) -> bool:
        # Özel mantığınız
        return frame_index % 10 == 0  # Her 10. kare
```


<p align="center">
  ⭐ Beğendiyseniz yıldız vermeyi unutmayın!
</p>
