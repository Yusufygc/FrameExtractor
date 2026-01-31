// Frame_Ayirici/qml/Main.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import "components" as Components

ApplicationWindow {
    id: window
    
    visible: true
    width: 980
    height: 780
    minimumWidth: 950
    minimumHeight: 750
    
    title: "Frame Extractor"
    
    // Gradient background
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "#1E1B32" }
            GradientStop { position: 1.0; color: "#342F5C" }
        }
    }
    
    // Main content
    Item {
        id: contentArea
        anchors.fill: parent
        anchors.margins: 24
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 16
            
            // Top row - Video Selection and Output Directory
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                // Video Selection Card
                Components.GlassCard {
                    title: "1. Video Seçimi 🎥"
                    Layout.fillWidth: true
                    Layout.preferredWidth: parent.width * 0.55
                    Layout.preferredHeight: 280
                    
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 12
                        
                        // File path row
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            
                            Components.StyledTextField {
                                id: videoPathField
                                Layout.fillWidth: true
                                placeholderText: "🎥 Lütfen bir video dosyası seçin..."
                                readOnly: true
                                text: backend ? backend.videoPath : ""
                                font.pixelSize: 13
                            }
                            
                            Components.SecondaryButton {
                                text: "..."
                                implicitWidth: 48
                                implicitHeight: 40
                                onClicked: videoFileDialog.open()
                            }
                        }
                        
                        // Video Info Display
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            color: Qt.rgba(0, 0, 0, 0.15)
                            border.color: Qt.rgba(1, 1, 1, 0.1)
                            border.width: 1
                            radius: 8
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 12
                                
                                Text {
                                    text: "📊 Video Analizi"
                                    color: "#E0E0E0"
                                    font.pixelSize: 15
                                    font.bold: true
                                }
                                
                                // Info grid
                                GridLayout {
                                    columns: 4
                                    columnSpacing: 20
                                    rowSpacing: 10
                                    visible: backend ? backend.videoPath !== "" : false
                                    
                                    Text { text: "📏 Çözünürlük:"; color: "#AAAAAA"; font.pixelSize: 14 }
                                    Text { text: backend ? backend.resolution : "-"; color: "#00D1FF"; font.bold: true; font.pixelSize: 14 }
                                    
                                    Text { text: "⏱️ Süre:"; color: "#AAAAAA"; font.pixelSize: 14 }
                                    Text { text: backend ? backend.duration : "-"; color: "#50E3C2"; font.bold: true; font.pixelSize: 14 }
                                    
                                    Text { text: "🎞️ FPS:"; color: "#AAAAAA"; font.pixelSize: 14 }
                                    Text { text: backend ? backend.fps.toFixed(2) : "-"; color: "#FFD600"; font.bold: true; font.pixelSize: 14 }
                                    
                                    Text { text: "📦 Frame:"; color: "#AAAAAA"; font.pixelSize: 14 }
                                    Text { text: backend ? backend.frameCount.toLocaleString() : "-"; color: "#B298DC"; font.bold: true; font.pixelSize: 14 }
                                }
                                
                                Text {
                                    text: "📊 Video yüklendikten sonra bilgiler burada görünecek."
                                    color: "#666666"
                                    font.pixelSize: 14
                                    font.italic: true
                                    visible: backend ? backend.videoPath === "" : true
                                    wrapMode: Text.Wrap
                                    Layout.fillWidth: true
                                }
                                
                                Item { Layout.fillHeight: true }
                            }
                        }
                    }
                }
                
                // Output Directory Card
                Components.GlassCard {
                    title: "2. Çıktı Dizini 📂"
                    Layout.fillWidth: true
                    Layout.preferredWidth: parent.width * 0.45
                    Layout.preferredHeight: 280
                    
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 12
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            
                            Components.StyledTextField {
                                id: outputDirField
                                Layout.fillWidth: true
                                placeholderText: "📂 İsteğe bağlı: Çıktı klasörünü seçin..."
                                text: backend ? backend.outputDir : ""
                                onTextChanged: if (backend) backend.outputDir = text
                                font.pixelSize: 13
                            }
                            
                            Components.SecondaryButton {
                                text: "..."
                                implicitWidth: 48
                                implicitHeight: 40
                                onClicked: folderDialog.open()
                            }
                        }
                        
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            color: Qt.rgba(0, 0, 0, 0.1)
                            border.color: Qt.rgba(1, 1, 1, 0.05)
                            radius: 8
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 16
                                spacing: 10
                                
                                Text {
                                    text: "💡 Bilgi"
                                    color: "#E0E0E0"
                                    font.pixelSize: 15
                                    font.bold: true
                                }
                                
                                Text {
                                    text: "Seçim yapılmazsa, klasör masaüstünde video adıyla otomatik oluşturulur."
                                    color: "#888888"
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    Layout.fillWidth: true
                                }
                                
                                Item { Layout.fillHeight: true }
                            }
                        }
                    }
                }
            }
            
            // Options Card - Expanded height
            Components.GlassCard {
                title: "3. Ayırma Seçenekleri ⚙️"
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 18
                    
                    ButtonGroup { id: modeGroup }
                    
                    // Row 1: All Frames and Scene Change side by side
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 50
                        
                        Components.StyledRadioButton {
                            id: radioAllFrames
                            text: "Videonun tüm framelerini ayır"
                            emoji: "🎬"
                            checked: true
                            ButtonGroup.group: modeGroup
                            font.pixelSize: 14
                        }
                        
                        Components.StyledRadioButton {
                            id: radioSceneChange
                            text: "Sahne değişimlerini algıla ve ayır"
                            emoji: "🎭"
                            ButtonGroup.group: modeGroup
                            font.pixelSize: 14
                        }
                        
                        Item { Layout.fillWidth: true }
                    }
                    
                    // Row 2: Time Range option
                    Components.StyledRadioButton {
                        id: radioTimeRange
                        text: "Belirli bir zaman aralığını ayır"
                        emoji: "⏰"
                        ButtonGroup.group: modeGroup
                        font.pixelSize: 14
                    }
                    
                    // Row 3: Time range controls
                    RowLayout {
                        Layout.fillWidth: true
                        Layout.leftMargin: 35
                        spacing: 14
                        opacity: radioTimeRange.checked ? 1.0 : 0.3
                        enabled: radioTimeRange.checked
                        
                        Behavior on opacity { NumberAnimation { duration: 200 } }
                        
                        Text { text: "Başlangıç:"; color: "#CCCCCC"; font.pixelSize: 14 }
                        
                        Components.StyledTextField {
                            id: startTimeField
                            implicitWidth: 100
                            text: backend ? backend.startTime : "00:00:00"
                            onTextChanged: if (backend) backend.startTime = text
                            font.pixelSize: 13
                        }
                        
                        Components.RangeSlider {
                            id: rangeSlider
                            Layout.fillWidth: true
                            Layout.minimumWidth: 200
                            implicitHeight: 30
                            minValue: 0
                            maxValue: backend ? backend.videoDuration : 100
                            lowValue: 0
                            highValue: backend ? backend.videoDuration : 100
                            
                            onRangeChanged: function(low, high) {
                                if (backend) {
                                    backend.setTimeRange(low, high);
                                }
                            }
                        }
                        
                        Text { text: "Bitiş:"; color: "#CCCCCC"; font.pixelSize: 14 }
                        
                        Components.StyledTextField {
                            id: endTimeField
                            implicitWidth: 100
                            text: backend ? backend.endTime : "00:00:00"
                            onTextChanged: if (backend) backend.endTime = text
                            font.pixelSize: 13
                        }
                    }
                }
            }
            
            // Status Card
            Components.GlassCard {
                title: "4. Bilgilendirme ve Durum 📊"
                Layout.fillWidth: true
                Layout.preferredHeight: 95
                
                RowLayout {
                    anchors.fill: parent
                    spacing: 20
                    
                    Text {
                        id: statusLabel
                        text: backend ? "Durum: " + backend.statusMessage : "Durum: Başlamak için bir video seçin."
                        color: "#E0E0E0"
                        font.pixelSize: 15
                        Layout.fillWidth: true
                    }
                    
                    Components.ProgressBar {
                        id: progressBar
                        Layout.preferredWidth: 240
                        value: backend ? backend.progress / 100.0 : 0
                        visible: backend ? backend.isProcessing : false
                    }
                }
            }
            
            // Action Buttons Row
            RowLayout {
                Layout.fillWidth: true
                spacing: 16
                
                // Start Button
                Components.PrimaryButton {
                    id: startButton
                    text: "🚀 İşlemi Başlat"
                    Layout.preferredWidth: 220
                    Layout.preferredHeight: 48
                    enabled: backend ? !backend.isProcessing && backend.videoPath !== "" : false
                    visible: backend ? !backend.isProcessing : true
                    
                    font.pixelSize: 15
                    
                    onClicked: {
                        if (backend) {
                            var mode = "all";
                            if (radioTimeRange.checked) mode = "range";
                            else if (radioSceneChange.checked) mode = "scene";
                            backend.startProcessing(mode);
                        }
                    }
                }
                
                // Cancel Button - only visible during processing
                Button {
                    id: cancelButton
                    text: "❌ İptal Et"
                    Layout.preferredWidth: 160
                    Layout.preferredHeight: 48
                    visible: backend ? backend.isProcessing : false
                    
                    font.pixelSize: 15
                    font.bold: true
                    
                    background: Rectangle {
                        color: cancelButton.pressed ? "#CC3333" : 
                               cancelButton.hovered ? "#FF5555" : "#FF4444"
                        radius: 8
                        
                        Behavior on color { ColorAnimation { duration: 150 } }
                    }
                    
                    contentItem: Text {
                        text: cancelButton.text
                        font: cancelButton.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (backend) {
                            backend.cancelProcessing();
                        }
                    }
                    
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        acceptedButtons: Qt.NoButton
                    }
                }
                
            }
        }
    }
    
    // File Dialogs
    FileDialog {
        id: videoFileDialog
        title: "Video Dosyası Seç"
        nameFilters: ["Video Dosyaları (*.mp4 *.avi *.mov *.mkv)", "Tüm Dosyalar (*)"]
        onAccepted: {
            if (backend) {
                backend.loadVideo(selectedFile);
            }
        }
    }
    
    FolderDialog {
        id: folderDialog
        title: "Çıktı Klasörü Seç"
        onAccepted: {
            if (backend) {
                backend.outputDir = selectedFolder.toString().replace("file:///", "");
            }
        }
    }
    
    // Message dialogs
    Connections {
        target: backend
        
        function onShowMessage(title, message, isError) {
            messageDialogTitle.text = title;
            messageDialogContent.text = message;
            messageDialog.open();
        }
    }
    
    Dialog {
        id: messageDialog
        
        anchors.centerIn: parent
        modal: true
        width: 450
        padding: 0
        
        background: Rectangle {
            color: "#2A2744"
            border.color: Qt.rgba(1, 1, 1, 0.2)
            border.width: 1
            radius: 12
            implicitHeight: dialogContent.implicitHeight + 40
        }
        
        contentItem: ColumnLayout {
            id: dialogContent
            spacing: 16
            
            Text {
                id: messageDialogTitle
                text: ""
                color: "#00D1FF"
                font.pixelSize: 18
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 24
            }
            
            Text {
                id: messageDialogContent
                text: ""
                color: "#E0E0E0"
                font.pixelSize: 14
                wrapMode: Text.Wrap
                Layout.fillWidth: true
                Layout.leftMargin: 30
                Layout.rightMargin: 30
                horizontalAlignment: Text.AlignHCenter
            }
            
            Item { Layout.preferredHeight: 10 }
            
            Button {
                text: "Tamam"
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 130
                Layout.preferredHeight: 40
                Layout.bottomMargin: 24
                
                font.pixelSize: 14
                
                background: Rectangle {
                    color: parent.pressed ? "#0099CC" : parent.hovered ? "#00BBEE" : "#00D1FF"
                    radius: 8
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
                
                contentItem: Text {
                    text: "Tamam"
                    color: "#1E1B32"
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: messageDialog.close()
            }
        }
    }
}
