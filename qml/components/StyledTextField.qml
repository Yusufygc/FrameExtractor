// Frame_Ayirici/qml/components/StyledTextField.qml
import QtQuick
import QtQuick.Controls

TextField {
    id: root
    
    implicitHeight: 40
    
    color: "#E0E0E0"
    placeholderTextColor: "#888888"
    font.pixelSize: 10
    
    background: Rectangle {
        color: Qt.rgba(0, 0, 0, 0.2)
        border.color: root.activeFocus ? "#00D1FF" : Qt.rgba(1, 1, 1, 0.1)
        border.width: 1
        radius: 8
        
        Behavior on border.color {
            ColorAnimation { duration: 150 }
        }
    }
    
    leftPadding: 12
    rightPadding: 12
}
