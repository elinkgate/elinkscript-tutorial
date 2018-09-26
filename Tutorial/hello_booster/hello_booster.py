from eLink.elinkScriptUtils import *
from time import sleep

elinkObj = None


def getCurrentConnection():
    gConn = elink.getConnection()
    if len(gConn) != 0:
        return gConn[0]
    return None


def del_all(elinkObj):
    sleep(2)
    elinkObj.sendKey("End")
    sleep(1)
    elinkObj.sendKeyEx(["LeftShift", "Home"])
    sleep(1)
    elinkObj.sendKey("Delete")
    sleep(1)


def main():
    elinkObj = getCurrentConnection()
    if elinkObj is None:
        elinkObj = elink.newConnection("10.42.0.100")
    elinkObj.setKeyIdle(10)
    elinkObj.setVncMode(VncMode.VNC_MODE_BOOSTER)
    elinkObj.setUsbMode(UsbMode.USB_MODE_KEY | UsbMode.USB_MODE_VNC_HID, 0, ["A:/winpe.hdd2"])
    elinkObj.setKeyMode(KeyMode.KEY_INTF_HID)
    elinkObj.setMouseMode(PointerMode.POINT_INTF_VNC)
    waitImage(elinkObj, "tmp6.png")
    elinkObj.sendKeyEx(["LeftControl", "LeftAlt", "DeleteForward"])
    waitImage(elinkObj, "Tutorial/hello_booster/admin_login.png")
    elinkObj.sendString("Abcdef12345")
    elinkObj.sendKey("Enter")
    waitImage(elinkObj, "Tutorial/hello_booster/wellcome_server.png")
    elinkObj.sendKeyEx(["LeftGUI", "R"])
    elinkObj.sendString("notepad")
    sleep(1)
    elinkObj.sendKey("Enter")
    # clickbutton(elinkObj, "Tutorial/hello_booster/click_notepad.png")
    clickbutton(elinkObj, "Tutorial/hello_booster/click_notepad_icon.png")
    elinkObj.sendString("hello world")

    #
    # waitImage(elinkObj, "Tutorial/AutoConfigureELinkKVM/elink_kvm_welcome.png")
    # clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/network_tab.png")
    # clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_ip_address.png")
    # del_all(elinkObj)
    # clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_apply.png")
    # clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_admin_tab.png")
    # clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_reboot.png")
    pass


if __name__ == "__main__":
    main()
