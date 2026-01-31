// Frame_Ayirici/qml/components/StyledRadioButton.qml
import QtQuick
import QtQuick.Controls

RadioButton {
    id: root
    
    property string emoji: ""
    
    font.pixelSize: 14
    
    indicator: Rectangle {
        implicitWidth: 18
        implicitHeight: 18
        x: root.leftPadding
        y: parent.height / 2 - height / 2
        radius: 9
        color: "transparent"
        border.color: root.checked ? "#00D1FF" : Qt.rgba(1, 1, 1, 0.3)
        border.width: 2
        
        Behavior on border.color {
            ColorAnimation { duration: 150 }
        }
        
        Rectangle {
            width: 10
            height: 10
            anchors.centerIn: parent
            radius: 5
            color: "#00D1FF"
            visible: root.checked
            
            scale: root.checked ? 1.0 : 0.0
            Behavior on scale {
                NumberAnimation { duration: 150; easing.type: Easing.OutBack }
            }
        }
    }
    
    contentItem: Text {
        text: root.emoji + " " + root.text
        font: root.font
        color: "#E0E0E0"
        verticalAlignment: Text.AlignVCenter
        leftPadding: root.indicator.width + root.spacing + 4
    }
    
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.NoButton
    }
}
