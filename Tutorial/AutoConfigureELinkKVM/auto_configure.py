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
        elinkObj = elink.newConnection("10.0.0.1")
    elinkObj.setVncMode(VncMode.VNC_MODE_DUMMY)
    elinkObj.setUsbMode(UsbMode.USB_MODE_KEY | UsbMode.USB_MODE_VNC_HID, 0)
    elinkObj.setKeyMode(KeyMode.KEY_INTF_VNC)
    elinkObj.setMouseMode(PointerMode.POINT_INTF_VNC)
    waitImage(elinkObj, "Tutorial/AutoConfigureELinkKVM/elink_kvm_welcome.png")
    clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/network_tab.png")
    clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_ip_address.png")
    del_all(elinkObj)
    elinkObj.sendString("10.42.0.100")
    clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_apply.png")
    clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_admin_tab.png")
    clickbutton(elinkObj, "Tutorial/AutoConfigureELinkKVM/click_reboot.png")
    pass


if __name__ == "__main__":
    main()
