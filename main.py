import sys
from PyQt5.QtWidgets import QApplication

# Proje yapımıza göre ui paketinden MainWindow sınıfını import ediyoruz.
# Bu satırın çalışabilmesi için main.py'nin FrameExtractor klasörünün içinde olması gerekir.
from ui.main_window import MainWindow

def main():
    """
    Uygulamanın ana başlangıç fonksiyonu.
    """
    # 1. Her PyQt5 uygulaması bir QApplication nesnesine ihtiyaç duyar.
    # sys.argv, komut satırı argümanlarının uygulamaya geçilmesini sağlar.
    app = QApplication(sys.argv)

    # 2. Ana penceremizin bir örneğini (instance) oluşturuyoruz.
    # Bu, ui/main_window.py dosyasındaki MainWindow sınıfıdır.
    window = MainWindow()

    # 3. Pencereyi görünür hale getiriyoruz.
    window.show()

    # 4. Uygulamanın olay döngüsünü (event loop) başlatıyoruz.
    # Bu, pencere kapatılana kadar programın çalışmasını sağlar.
    # sys.exit, programın temiz bir şekilde kapanmasını garanti eder.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()