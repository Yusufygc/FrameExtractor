// Frame_Ayirici/qml/components/RangeSlider.qml
import QtQuick
import QtQuick.Controls

Item {
    id: root
    
    property real minValue: 0
    property real maxValue: 100
    property real lowValue: 0
    property real highValue: 100
    
    signal rangeChanged(real low, real high)
    
    implicitHeight: 28
    implicitWidth: 300
    
    // Calculate positions
    readonly property real handleRadius: 8
    readonly property real trackPadding: handleRadius
    readonly property real trackWidth: width - (trackPadding * 2)
    
    function valueToPos(value) {
        if (maxValue <= minValue) return trackPadding;
        return trackPadding + (trackWidth * (value - minValue) / (maxValue - minValue));
    }
    
    function posToValue(pos) {
        var normalizedPos = (pos - trackPadding) / trackWidth;
        normalizedPos = Math.max(0, Math.min(1, normalizedPos));
        return minValue + normalizedPos * (maxValue - minValue);
    }
    
    // Background track
    Rectangle {
        anchors.verticalCenter: parent.verticalCenter
        x: root.trackPadding
        width: root.trackWidth
        height: 4
        radius: 2
        color: Qt.rgba(0, 0, 0, 0.4)
        
        // Selected range highlight
        Rectangle {
            x: root.valueToPos(root.lowValue) - root.trackPadding
            width: root.valueToPos(root.highValue) - root.valueToPos(root.lowValue)
            height: parent.height
            radius: 2
            color: "#00D1FF"
        }
    }
    
    // Low handle
    Rectangle {
        id: lowHandle
        x: root.valueToPos(root.lowValue) - handleRadius
        anchors.verticalCenter: parent.verticalCenter
        width: handleRadius * 2
        height: handleRadius * 2
        radius: handleRadius
        color: "#00D1FF"
        border.color: "#E0E0E0"
        border.width: 2
        
        scale: lowMouse.pressed ? 1.2 : (lowMouse.containsMouse ? 1.1 : 1.0)
        Behavior on scale { NumberAnimation { duration: 100 } }
        
        MouseArea {
            id: lowMouse
            anchors.fill: parent
            anchors.margins: -5
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            
            property real startX: 0
            property real startValue: 0
            
            onPressed: (mouse) => {
                startX = mouse.x + lowHandle.x;
                startValue = root.lowValue;
            }
            
            onPositionChanged: (mouse) => {
                if (!pressed) return;
                var newPos = startX + (mouse.x - startX) + lowHandle.x;
                var newValue = root.posToValue(newPos + root.handleRadius);
                newValue = Math.max(root.minValue, Math.min(root.highValue, newValue));
                root.lowValue = Math.round(newValue);
                root.rangeChanged(root.lowValue, root.highValue);
            }
        }
    }
    
    // High handle
    Rectangle {
        id: highHandle
        x: root.valueToPos(root.highValue) - handleRadius
        anchors.verticalCenter: parent.verticalCenter
        width: handleRadius * 2
        height: handleRadius * 2
        radius: handleRadius
        color: "#00D1FF"
        border.color: "#E0E0E0"
        border.width: 2
        
        scale: highMouse.pressed ? 1.2 : (highMouse.containsMouse ? 1.1 : 1.0)
        Behavior on scale { NumberAnimation { duration: 100 } }
        
        MouseArea {
            id: highMouse
            anchors.fill: parent
            anchors.margins: -5
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            
            property real startX: 0
            
            onPressed: (mouse) => {
                startX = mouse.x + highHandle.x;
            }
            
            onPositionChanged: (mouse) => {
                if (!pressed) return;
                var newPos = startX + (mouse.x - startX) + highHandle.x;
                var newValue = root.posToValue(newPos + root.handleRadius);
                newValue = Math.max(root.lowValue, Math.min(root.maxValue, newValue));
                root.highValue = Math.round(newValue);
                root.rangeChanged(root.lowValue, root.highValue);
            }
        }
    }
}
