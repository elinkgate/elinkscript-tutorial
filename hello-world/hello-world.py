from elinkScriptUtils import *


def getCurrentConnection():
    gConn = elink.getConnection()
    if len(gConn) != 0:
        return gConn[0]
    return None


def main():
    elinkObj = getCurrentConnection()
    if elinkObj is None:
        elinkObj = elink.newConnection("10.42.0.2")
    elinkObj.setVncMode("MODE_VNC_RGB")
    elinkObj.setUsbMode("USB_MODE_KEY|USB_MODE_VNC_HID|USB_MODE_MOUSE_ABS", 0)
    elinkObj.setKeyMode("KEY_INTF_HID")
    elinkObj.setMouseMode("POINT_INTF_HID_ABS")
    waitImage(elinkObj, "hello-world/notepad_icon.png")
    clickbutton(elinkObj, "hello-world/notepad_icon.png")
    clickbutton(elinkObj, "hello-world/click_maximum.png")
    elinkObj.sendString("Hello World")
    pass


if __name__ == "__main__":
    main()
