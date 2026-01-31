// Frame_Ayirici/qml/components/PrimaryButton.qml
import QtQuick
import QtQuick.Controls

Button {
    id: root
    
    // Properties
    property color baseColor: "#00D1FF"
    property color hoverColor: "#50E3FF"
    property color pressedColor: "#00A8CC"
    property color textColor: "#1E1B32"
    
    implicitHeight: 45
    implicitWidth: 200
    
    font.pixelSize: 12
    font.weight: Font.Bold
    
    background: Rectangle {
        color: root.pressed ? root.pressedColor : 
               root.hovered ? root.hoverColor : root.baseColor
        radius: 8
        
        Behavior on color {
            ColorAnimation { duration: 150; easing.type: Easing.OutCubic }
        }
        
        // Scale animation on press
        scale: root.pressed ? 0.98 : 1.0
        Behavior on scale {
            NumberAnimation { duration: 100; easing.type: Easing.OutCubic }
        }
    }
    
    contentItem: Text {
        text: root.text
        font: root.font
        color: root.textColor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    // Cursor change on hover
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.NoButton
    }
}
