// Frame_Ayirici/qml/components/GlassCard.qml
import QtQuick

Rectangle {
    id: root
    
    // Properties
    property string title: ""
    default property alias content: contentArea.data
    
    // Glassmorphism styling
    color: Qt.rgba(1, 1, 1, 0.05)
    border.color: Qt.rgba(1, 1, 1, 0.1)
    border.width: 1
    radius: 12
    
    Behavior on border.color {
        ColorAnimation { duration: 200 }
    }
    
    // Title
    Text {
        id: titleText
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 16
        anchors.leftMargin: 20
        
        text: root.title
        color: "#E0E0E0"
        font.pixelSize: 17
        font.weight: Font.Bold
        visible: root.title !== ""
    }
    
    // Content area
    Item {
        id: contentArea
        anchors.top: titleText.visible ? titleText.bottom : parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 20
        anchors.topMargin: titleText.visible ? 16 : 20
    }
}
