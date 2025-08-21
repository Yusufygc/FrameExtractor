
---

# Frame Extractor 🎞️

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)![PyQt5](https://img.shields.io/badge/Qt-PyQt5-green.svg)![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-orange.svg)![Lisans](https://img.shields.io/badge/license-MIT-lightgrey.svg)

Modern, duyarlı ve şık bir masaüstü uygulaması olan **Frame Extractor**, video dosyalarından kare (frame) ayıklama işlemini kolaylaştırmak için tasarlanmıştır. Python, PyQt5 ve OpenCV kullanılarak geliştirilmiştir.

A modern, responsive, and sleek desktop application designed to simplify the process of extracting frames from video files, built with Python, PyQt5, and OpenCV.

---

## 🎨 Arayüz Görüntüsü

Uygulamanın glassmorphism'den ilham alan modern ve kullanıcı dostu arayüzü:

*(İPUCU: Aşağıdaki satırdaki `link/to/your/screenshot.png` kısmını, projenizin bir ekran görüntüsünü depoya yükleyip onun linkiyle değiştirin.)*

![Frame Extractor Arayüzü](link/to/your/screenshot.png)

## ✨ Temel Özellikler

*   **🎬 Tüm Kareleri Ayıklama:** Bir videonun başından sonuna kadar tüm kareleri ayrı ayrı `.jpg` dosyaları olarak kaydeder.
*   **⏰ Zaman Aralığı Belirleme:** Sezgisel bir zaman kaydırıcısı (range slider) veya hassas zaman giriş kutuları kullanarak videonun sadece belirli bir bölümündeki kareleri ayıklar.
*   **🎭 Sahne Değişimi Tespiti:** Videodaki sahne geçişlerini otomatik olarak algılar ve her yeni sahnenin yalnızca ilk karesini kaydederek videonun bir özetini çıkarır.
*   **📊 Detaylı Video Analizi:** Bir video yüklendiğinde; çözünürlük, süre, FPS, toplam frame sayısı, dosya boyutu ve en-boy oranı gibi önemli bilgileri şık bir kart üzerinde gösterir.
*   **🚀 Modern ve Duyarlı Arayüz:**
    *   Glassmorphism'den ilham alan yarı saydam ve gölgeli modern tasarım.
    *   Pencere boyutu değiştiğinde içeriği koruyan ve gerektiğinde kaydırma çubuğu sunan esnek yapı.
    *   Tüm platformlarda tutarlı ve profesyonel görünüm.
*   **📁 Otomatik Klasör Yönetimi:** Çıktı dizini belirtilmezse, ayıklanan kareleri masaüstünde video adıyla otomatik olarak oluşturulmuş bir klasöre kaydeder.
*   **🔧 Sağlam Hata Yönetimi:** Bozuk video dosyaları, Türkçe karakter içeren dosya yolları veya yazma izni olmayan klasörler gibi durumlarda kullanıcıya anlaşılır hata mesajları gösterir.

## 🛠️ Kullanılan Teknolojiler

*   **Python 3:** Projenin ana programlama dili.
*   **PyQt5:** Modern ve platformdan bağımsız masaüstü arayüzü için.
*   **OpenCV-Python:** Video okuma, işleme ve kare ayıklama işlemleri için.
*   **NumPy:** Türkçe karakter içeren dosya yollarıyla güvenli bir şekilde çalışmak ve verimli veri işleme için.

## 🚀 Kurulum ve Çalıştırma

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

*   Python 3.7 veya üstü
*   pip (Python paket yöneticisi)

### Adımlar

1.  **Depoyu klonlayın:**
    ```bash
    git clone https://github.com/[KULLANICI_ADINIZ]/FrameExtractor.git
    cd FrameExtractor
    ```

2.  **Sanal bir ortam oluşturun ve aktif edin (Önerilir):**
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı çalıştırın:**
    ```bash
    python main.py
    ```

## 📂 Proje Yapısı

Proje, Sorumlulukların Ayrılığı (Separation of Concerns) ilkesine uygun olarak modüler bir yapıda tasarlanmıştır:

```
FrameExtractor/
├── core/               # Ana iş mantığı (video işleme)
│   └── video_processor.py
├── ui/                 # Kullanıcı arayüzü (pencere tasarımı, widget'lar)
│   ├── main_window.py
│   └── range_slider.py
├── threads/            # Arka plan işlemleri (arayüzün donmasını engellemek için)
│   └── worker.py
├── main.py             # Uygulamayı başlatan ana betik
└── requirements.txt    # Gerekli Python kütüphaneleri
```

## 🤝 Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir "issue" açın veya bir "pull request" gönderin. Tüm katkılara açığım!

1.  Projeyi Fork'layın.
2.  Yeni bir Feature Branch oluşturun (`git checkout -b feature/AmazingFeature`).
3.  Değişikliklerinizi Commit'leyin (`git commit -m 'Add some AmazingFeature'`).
4.  Branch'inizi Push'layın (`git push origin feature/AmazingFeature`).
5.  Bir Pull Request açın.
