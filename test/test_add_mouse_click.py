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
    print("test {}".format(__file__))
    elinkObj = getCurrentConnection()
    if elinkObj is None:
        elinkObj = elink.newConnection("10.42.0.100")
    elinkObj.setKeyIdle(10)
    elinkObj.setVncMode(VncMode.VNC_MODE_BOOSTER)
    elinkObj.setUsbMode(UsbMode.USB_MODE_KEY | UsbMode.USB_MODE_VNC_HID, 0, ["A:/floppy.hddx"])
    elinkObj.setKeyMode(KeyMode.KEY_INTF_HID)
    elinkObj.setMouseMode(PointerMode.POINT_INTF_VNC)

