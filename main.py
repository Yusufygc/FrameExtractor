# Frame_Ayirici/main.py
"""
Frame Extractor - Main Application Entry Point
A modern video frame extraction application using PySide6 + QML.
"""

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QtMsgType, qInstallMessageHandler


def qt_message_handler(mode, context, message):
    """Handle Qt messages for debugging."""
    if mode == QtMsgType.QtWarningMsg:
        print(f"QML Warning: {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        print(f"QML Critical: {message}")
    elif mode == QtMsgType.QtFatalMsg:
        print(f"QML Fatal: {message}")
    else:
        print(f"QML Info: {message}")


def main():
    """
    Application entry point.
    Sets up the QML engine and loads the main UI.
    """
    # Install message handler for QML debugging
    qInstallMessageHandler(qt_message_handler)
    
    # Set Qt Quick Controls style to Basic for full customization support
    import os
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
    
    # Create application
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Frame Extractor")
    app.setOrganizationName("FrameExtractor")
    
    # Create QML engine
    engine = QQmlApplicationEngine()
    
    # Import Backend here to avoid circular imports
    from ui.backend import Backend
    
    # Create backend and expose to QML
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    
    # Add QML import paths
    qml_dir = Path(__file__).parent / "qml"
    engine.addImportPath(str(qml_dir))
    engine.addImportPath(str(qml_dir / "components"))
    
    print(f"QML directory: {qml_dir}")
    print(f"Import paths: {engine.importPathList()}")
    
    # Load main QML file
    main_qml = qml_dir / "Main.qml"
    print(f"Loading QML: {main_qml}")
    
    engine.load(QUrl.fromLocalFile(str(main_qml)))
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        print("Error: Could not load QML file")
        sys.exit(-1)
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()