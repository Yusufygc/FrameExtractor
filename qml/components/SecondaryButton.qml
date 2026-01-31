// Frame_Ayirici/qml/components/SecondaryButton.qml
import QtQuick
import QtQuick.Controls

Button {
    id: root
    
    implicitHeight: 36
    implicitWidth: 40
    
    font.pixelSize: 10
    
    background: Rectangle {
        color: root.pressed ? Qt.rgba(0, 0, 0, 0.05) : 
               root.hovered ? Qt.rgba(1, 1, 1, 0.12) : Qt.rgba(1, 1, 1, 0.08)
        border.color: Qt.rgba(1, 1, 1, 0.15)
        border.width: 1
        radius: 8
        
        Behavior on color {
            ColorAnimation { duration: 150; easing.type: Easing.OutCubic }
        }
    }
    
    contentItem: Text {
        text: root.text
        font: root.font
        color: "#E0E0E0"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.NoButton
    }
}
