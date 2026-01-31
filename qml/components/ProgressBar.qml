// Frame_Ayirici/qml/components/ProgressBar.qml
import QtQuick
import QtQuick.Controls

Item {
    id: root
    
    property real value: 0 // 0.0 to 1.0
    
    implicitHeight: 20
    implicitWidth: 200
    
    // Background track
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0.2)
        border.color: Qt.rgba(1, 1, 1, 0.1)
        border.width: 1
        radius: 8
        
        // Progress fill
        Rectangle {
            id: progressFill
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: 2
            
            width: Math.max(0, (parent.width - 4) * root.value)
            radius: 6
            
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "#00D1FF" }
                GradientStop { position: 1.0; color: "#50E3C2" }
            }
            
            Behavior on width {
                NumberAnimation { 
                    duration: 200
                    easing.type: Easing.OutCubic 
                }
            }
        }
        
        // Percentage text
        Text {
            anchors.centerIn: parent
            text: Math.round(root.value * 100) + "%"
            color: "white"
            font.pixelSize: 10
            font.weight: Font.Medium
        }
    }
}
