from eLink.elinkScriptUtils import *


def getCurrentConnection():
    gConn = elink.getConnection()
    if len(gConn) != 0:
        return gConn[0]
    return None


def main():
    vnc = getCurrentConnection()
    if vnc is None:
        vnc = elink.newConnection("10.42.0.100")
    vnc.setUsbMode(0, 0)
    time.sleep(2)
    vnc.setUsbMode(UsbMode.USB_MODE_KEY | UsbMode.USB_MODE_VNC_HID, 0, ["A:\\floppy.hddx"])
    vnc.setKeyMode(KeyMode.KEY_INTF_HID)
    vnc.setKeyIdle(50)
    waitKeyReady(vnc)
    vnc.setVncMode(VncMode.VNC_MODE_BOOSTER)
    print("send trigger command")
    time.sleep(1)
    vnc.sendKeyEx(["LeftGUI", "R"])
    time.sleep(1)
    vnc.sendString("A:\\elinkme")
    vnc.sendKey("Enter")
    print("wait for hipconnect")
    ev = vnc.getEvent()
    print("event code ", ev.getIdCode(), " ", ev.getData("Test"))
    while ev.getIdCode() != 22:
        ev = vnc.getEvent()
        print("event code ", ev.getIdCode(), " ", ev.getData("Test"))
    print("connect done")
    vnc.setMouseMode(2)
    vnc.setKeyMode(2)


def waitKeyReady(vnc):
    print("waitKeyboard")
    key_state = -1

    while True:
        ev = vnc.getEvent()
        print("get event ", ev.getIdCode())
        if ev.getIdCode() == 2:
            break

    ev = vnc.getEvent(2000)

    while True:
        if ev.getIdCode() == 6:
            key_state = ev.getData("Test") & 0x04
            break
        elif ev.getIdCode() == -1:
            break
        else:
            ev = vnc.getEvent(2000)

    if key_state == -1:
        key_state = 0
        vnc.sendKey("ScrollLock")

    count_send = 0
    while True:
        ev = vnc.getEvent(2000)
        if ev.getIdCode() == -1:
            count_send = count_send + 1
            if count_send < 3:
                vnc.sendKey("ScrollLock")
                continue
            else:
                print("Keyboard is not ready")
                assert 0
        elif ev.getIdCode() == 6:
            key_state2 = ev.getData("Test") & 0x04
        else:
            continue

        if key_state2 == key_state:
            print("Keyboard is ready")
            break


if __name__ == "__main__":
    import time

    main()
