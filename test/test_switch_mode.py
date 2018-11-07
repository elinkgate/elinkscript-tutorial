from eLink.elinkScriptUtils import *
from time import sleep

elinkObj = None
default_elinkvkm = "10.42.0.100"


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
        elinkObj = elink.newConnection(default_elinkvkm)
    # filemnger: FileManager = FileManager(elinkObj)
    # floppyfile = filemnger.is_file_exist_regress("floppy.hddx")
    # if floppyfile is None:
    #     print("not found")
    #     return
    elinkObj.setKeyIdle(10)
    elinkObj.setVncMode(VncModeVNC_MODE_BOOSTER)
    elinkObj.setUsbMode(UsbMode.USB_MODE_KEY | UsbMode.USB_MODE_VNC_HID,
                        0,
                        ["A:/floppy.hddx"])
    elinkObj.setKeyMode(KeyMode.KEY_INTF_HID)
    elinkObj.setMouseMode(PointjrMode.POINT_INTF_VNC)
    # for mode in VncMode:
    #     elinkObj.setVncMode(mode)
    #     pass
